//! Filesystem paths + logging setup.
//!
//! Mirrors `syriana_constants.get_syriana_home()` from the Python CLI:
//!   Windows: %LOCALAPPDATA%\syriana
//!   macOS:   ~/.syriana
//!   Linux:   ~/.syriana  (override via $SYRIANA_HOME)
//!
//! NOTE (macOS): Python's get_syriana_home(), scripts/install.sh, and the
//! Electron desktop's resolveHermesHome() ALL use ~/.syriana on macOS — there
//! is no ~/Library/Application Support branch anywhere else. An earlier
//! version of this file used Application Support, which drifted from every
//! other component: the installer wrote the install to one dir and the
//! desktop looked for it in another, so first launch never found the backend.
//!
//! IMPORTANT: this must match exactly. Drift here means install.ps1
//! writes to one place and the installer reads from another, breaking
//! the bootstrap-complete check.

use std::path::{Path, PathBuf};
#[cfg(target_os = "macos")]
use std::process::Command;
use tracing_appender::non_blocking::WorkerGuard;

/// Returns the canonical Syriana home directory, respecting $SYRIANA_HOME if set.
pub fn syriana_home() -> PathBuf {
    if let Ok(override_path) = std::env::var("SYRIANA_HOME") {
        if !override_path.trim().is_empty() {
            return PathBuf::from(override_path);
        }
    }

    #[cfg(target_os = "windows")]
    {
        // %LOCALAPPDATA%\syriana — matches scripts/install.ps1's $SyrianaHome.
        if let Some(local_app_data) = dirs::data_local_dir() {
            return local_app_data.join("syriana");
        }
    }

    // macOS + Linux + fallback: ~/.syriana (matches Python get_syriana_home(),
    // install.sh, and the Electron desktop's resolveHermesHome()).
    if let Some(home) = dirs::home_dir() {
        return home.join(".syriana");
    }

    // Last resort — current dir, almost certainly wrong but at least
    // doesn't panic.
    PathBuf::from(".syriana")
}

pub fn log_dir() -> PathBuf {
    syriana_home().join("logs")
}

pub fn log_path() -> PathBuf {
    log_dir().join("bootstrap-installer.log")
}

pub fn bootstrap_cache_dir() -> PathBuf {
    syriana_home().join("bootstrap-cache")
}

/// Stable location the installer copies itself to after a successful install.
/// The desktop app re-invokes this with `--update`, and the start-menu /
/// desktop shortcuts can point users back to it. Lives directly under
/// SYRIANA_HOME so it survives repo checkout deletion (unlike anything under
/// syriana-agent/).
///
/// On Windows this is `%LOCALAPPDATA%\syriana\syriana-setup.exe`; on other
/// platforms the extension differs but the directory is the same.
pub fn installer_dest() -> PathBuf {
    let name = if cfg!(target_os = "windows") {
        "syriana-setup.exe"
    } else {
        "syriana-setup"
    };
    syriana_home().join(name)
}

/// Marker the updater writes for the duration of an in-app update and removes
/// when it finishes (see update.rs `UpdateMarkerGuard`). A freshly-launched
/// desktop checks this before spawning its own local backend: spawning one
/// mid-update re-locks the venv shim and triggers `force_kill_other_hermes`,
/// which then kills that legitimate backend in a respawn loop (#50238).
///
/// Lives directly under SYRIANA_HOME (same rationale as `installer_dest`) so the
/// Electron desktop — which resolves SYRIANA_HOME identically and pins it into
/// the updater's env — agrees on the exact path.
pub fn update_in_progress_marker() -> PathBuf {
    syriana_home().join(".syriana-update-in-progress")
}

/// Copy the currently-running installer binary to `installer_dest()` so it's
/// available for future `--update` runs and shortcut launches.
///
/// No-ops (returns Ok) when the running exe is ALREADY the destination — which
/// is exactly the case during an `--update` run (the desktop launched us FROM
/// that path), where copying onto ourselves would be a Windows sharing
/// violation. Best-effort: a failure here must not fail the install, so the
/// caller logs and continues.
pub fn copy_self_to_syriana_home() -> std::io::Result<()> {
    let src = std::env::current_exe()?;
    let dest = installer_dest();

    // Skip if we're already running from the destination (update re-invocation
    // or a prior copy). canonicalize both so symlinks / 8.3 short paths / case
    // differences don't trick us into a self-copy.
    let same = match (src.canonicalize(), dest.canonicalize()) {
        (Ok(a), Ok(b)) => a == b,
        _ => src == dest,
    };
    if same {
        tracing::info!(?dest, "installer already at destination; skipping self-copy");
        return Ok(());
    }

    if let Some(parent) = dest.parent() {
        std::fs::create_dir_all(parent)?;
    }
    std::fs::copy(&src, &dest)?;
    repair_macos_installer_helper(&dest);
    tracing::info!(?src, ?dest, "copied installer to SYRIANA_HOME");
    Ok(())
}

#[cfg(target_os = "macos")]
fn repair_macos_installer_helper(path: &Path) {
    // The staged helper may inherit quarantine from the downloaded installer.
    // Desktop later launches this exact file for in-app updates, so make it
    // executable before the update handoff reaches LaunchServices/Gatekeeper.
    let _ = Command::new("/usr/bin/xattr")
        .args(["-cr"])
        .arg(path)
        .status();

    let verify = Command::new("/usr/bin/codesign")
        .arg("--verify")
        .arg(path)
        .status();

    if !matches!(verify, Ok(status) if status.success()) {
        let _ = Command::new("/usr/bin/codesign")
            .args(["--force", "--sign", "-"])
            .arg(path)
            .status();
    }
}

#[cfg(not(target_os = "macos"))]
fn repair_macos_installer_helper(_path: &Path) {}

/// Where install.ps1 writes the bootstrap-complete marker (existence-only file
/// the Electron app also checks). Per main.cjs:
///   const BOOTSTRAP_COMPLETE_MARKER = path.join(ACTIVE_HERMES_ROOT, '.syriana-bootstrap-complete')
/// We don't always know ACTIVE_HERMES_ROOT until install.ps1 reports it, so
/// this is a probe helper, not a definitive path.
pub fn likely_bootstrap_marker(install_root: &Path) -> PathBuf {
    install_root.join(".syriana-bootstrap-complete")
}

/// Initializes tracing to bootstrap-installer.log under SYRIANA_HOME/logs/.
/// Returns a guard that flushes the appender on drop — keep it alive for
/// the lifetime of the process.
pub fn init_logging() -> Option<WorkerGuard> {
    let dir = log_dir();
    if let Err(err) = std::fs::create_dir_all(&dir) {
        // No log dir → log to stderr only. Don't panic; the installer
        // should still be usable on an exotic filesystem.
        eprintln!("[syriana-setup] could not create log dir {dir:?}: {err}");
        return None;
    }

    let file_appender = tracing_appender::rolling::never(&dir, "bootstrap-installer.log");
    let (non_blocking, guard) = tracing_appender::non_blocking(file_appender);

    let env_filter = tracing_subscriber::EnvFilter::try_from_env("SYRIANA_BOOTSTRAP_LOG")
        .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new("info"));

    tracing_subscriber::fmt()
        .with_env_filter(env_filter)
        .with_writer(non_blocking)
        .with_ansi(false)
        .with_target(true)
        .init();

    Some(guard)
}

// ---------------------------------------------------------------------------
// Tauri commands
// ---------------------------------------------------------------------------

#[tauri::command]
pub fn get_log_path() -> String {
    log_path().to_string_lossy().into_owned()
}

#[tauri::command]
pub fn get_syriana_home() -> String {
    syriana_home().to_string_lossy().into_owned()
}

#[tauri::command]
pub fn open_log_dir(app: tauri::AppHandle) -> Result<(), String> {
    use tauri_plugin_opener::OpenerExt;
    let path = log_dir();
    app.opener()
        .open_path(path.to_string_lossy(), None::<&str>)
        .map_err(|e| e.to_string())
}
