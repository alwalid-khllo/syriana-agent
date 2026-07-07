#!/usr/bin/env bash
# ============================================================================
# scripts/lib/node-bootstrap.sh
# ----------------------------------------------------------------------------
# Sourceable helper: ensure Node.js >= MIN_VERSION is available for the TUI
# (React + Ink), browser tools, and the WhatsApp bridge.
#
# Strategy (first hit wins — respects the user's existing tooling):
#   1. modern `node` already on PATH
#   2. ~/.syriana/node/ from a prior Syriana-managed install
#   3. fnm, proto, nvm (in that order) if the user already uses a version manager
#   4. Termux `pkg`, macOS Homebrew
#   5. pinned nodejs.org tarball into ~/.syriana/node/ (always works, zero shell rc edits)
#
# Usage:
#   source scripts/lib/node-bootstrap.sh
#   ensure_node   # returns 0 on success, non-zero on failure
#   if [ "$SYRIANA_NODE_AVAILABLE" = true ]; then ...; fi
#
# Env inputs (set before sourcing to override defaults):
#   SYRIANA_NODE_MIN_VERSION   (default: 20)   — accepted on PATH
#   SYRIANA_NODE_TARGET_MAJOR  (default: 22)   — installed when we install
#   SYRIANA_HOME               (default: $HOME/.syriana)
# ============================================================================

SYRIANA_NODE_MIN_VERSION="${SYRIANA_NODE_MIN_VERSION:-20}"
SYRIANA_NODE_TARGET_MAJOR="${SYRIANA_NODE_TARGET_MAJOR:-22}"
SYRIANA_HOME="${SYRIANA_HOME:-$HOME/.syriana}"
SYRIANA_NODE_AVAILABLE=false

# ---------------------------------------------------------------------------
# Logging — prefer the host script's log_* helpers when present
# ---------------------------------------------------------------------------

_nb_log()  { declare -F log_info    >/dev/null 2>&1 && log_info    "$*" || printf '→ %s\n' "$*" >&2; }
_nb_ok()   { declare -F log_success >/dev/null 2>&1 && log_success "$*" || printf '✓ %s\n' "$*" >&2; }
_nb_warn() { declare -F log_warn    >/dev/null 2>&1 && log_warn    "$*" || printf '⚠ %s\n' "$*" >&2; }

# ---------------------------------------------------------------------------
# Platform + version helpers
# ---------------------------------------------------------------------------

_nb_is_termux() {
    [ -n "${TERMUX_VERSION:-}" ] || [[ "${PREFIX:-}" == *"com.termux/files/usr"* ]]
}

# Where to symlink node/npm/npx so they land on PATH.
# Mirrors get_command_link_dir() from install.sh: root FHS → /usr/local/bin,
# Termux → $PREFIX/bin, otherwise ~/.local/bin.
_nb_get_link_dir() {
    if _nb_is_termux && [ -n "${PREFIX:-}" ]; then
        echo "$PREFIX/bin"
    elif [ "$(id -u)" = 0 ] && [ "$(uname -s)" = "Linux" ]; then
        echo "/usr/local/bin"
    else
        echo "$HOME/.local/bin"
    fi
}

# Redirect a Syriana-managed Node's `npm install -g` to the command link dir
# (already on PATH) instead of the default $SYRIANA_HOME/node/bin, which is off
# PATH and wiped on every Node upgrade. Scoped to the managed Node via its
# prefix-local global npmrc; the user's other Node installs / ~/.npmrc are
# untouched. Idempotent no-op when there's no managed npm.
_nb_configure_npm_prefix() {
    [ -x "$SYRIANA_HOME/node/bin/npm" ] || return 0
    local _link_dir
    _link_dir="$(_nb_get_link_dir)"
    mkdir -p "$SYRIANA_HOME/node/etc"
    printf 'prefix=%s\n' "$(dirname "$_link_dir")" > "$SYRIANA_HOME/node/etc/npmrc"
}

_nb_node_major() {
    local v
    v=$(node --version 2>/dev/null | sed 's/^v//' | cut -d. -f1)
    [[ "$v" =~ ^[0-9]+$ ]] && echo "$v" || echo 0
}

_nb_have_modern_node() {
    command -v node >/dev/null 2>&1 || return 1
    [ "$(_nb_node_major)" -ge "$SYRIANA_NODE_MIN_VERSION" ]
}

# ---------------------------------------------------------------------------
# Version-manager paths — respect what the user already uses
# ---------------------------------------------------------------------------

_nb_try_fnm() {
    command -v fnm >/dev/null 2>&1 || return 1
    _nb_log "fnm detected — installing Node $SYRIANA_NODE_TARGET_MAJOR..."
    eval "$(fnm env 2>/dev/null)" || true
    fnm install "$SYRIANA_NODE_TARGET_MAJOR" >/dev/null 2>&1 || return 1
    fnm use     "$SYRIANA_NODE_TARGET_MAJOR" >/dev/null 2>&1 || return 1
    _nb_have_modern_node || return 1
    _nb_ok "Node $(node --version) activated via fnm"
    return 0
}

_nb_try_proto() {
    command -v proto >/dev/null 2>&1 || return 1
    _nb_log "proto detected — installing Node $SYRIANA_NODE_TARGET_MAJOR..."
    proto install node "$SYRIANA_NODE_TARGET_MAJOR" >/dev/null 2>&1 || return 1
    _nb_have_modern_node || return 1
    _nb_ok "Node $(node --version) activated via proto"
    return 0
}

_nb_try_nvm() {
    local nvm_sh="${NVM_DIR:-$HOME/.nvm}/nvm.sh"
    [ -s "$nvm_sh" ] || return 1
    # shellcheck source=/dev/null
    \. "$nvm_sh" >/dev/null 2>&1 || return 1
    _nb_log "nvm detected — installing Node $SYRIANA_NODE_TARGET_MAJOR..."
    nvm install "$SYRIANA_NODE_TARGET_MAJOR" >/dev/null 2>&1 || return 1
    nvm use     "$SYRIANA_NODE_TARGET_MAJOR" >/dev/null 2>&1 || return 1
    _nb_have_modern_node || return 1
    _nb_ok "Node $(node --version) activated via nvm"
    return 0
}

# ---------------------------------------------------------------------------
# Platform package managers
# ---------------------------------------------------------------------------

_nb_try_termux_pkg() {
    _nb_is_termux || return 1
    _nb_log "Installing Node.js via pkg..."
    pkg install -y nodejs >/dev/null 2>&1 || return 1
    _nb_have_modern_node || return 1
    _nb_ok "Node $(node --version) installed via pkg"
    return 0
}

_nb_try_brew() {
    [ "$(uname -s)" = "Darwin" ] || return 1
    command -v brew >/dev/null 2>&1 || return 1
    _nb_log "Installing Node via Homebrew..."
    brew install "node@${SYRIANA_NODE_TARGET_MAJOR}" >/dev/null 2>&1 \
        || brew install node >/dev/null 2>&1 \
        || return 1
    brew link --overwrite --force "node@${SYRIANA_NODE_TARGET_MAJOR}" >/dev/null 2>&1 || true
    _nb_have_modern_node || return 1
    _nb_ok "Node $(node --version) installed via Homebrew"
    return 0
}

# ---------------------------------------------------------------------------
# Bundled binary fallback — always works, no shell rc edits
# ---------------------------------------------------------------------------

_nb_install_bundled_node() {
    local arch node_arch os_name node_os
    arch=$(uname -m)
    case "$arch" in
        x86_64)        node_arch="x64"    ;;
        aarch64|arm64) node_arch="arm64"  ;;
        armv7l)        node_arch="armv7l" ;;
        *)
            _nb_warn "Unsupported arch ($arch) — install Node.js manually: https://nodejs.org/"
            return 1
            ;;
    esac

    os_name=$(uname -s)
    case "$os_name" in
        Linux*)  node_os="linux"  ;;
        Darwin*) node_os="darwin" ;;
        *)
            _nb_warn "Unsupported OS ($os_name) — install Node.js manually: https://nodejs.org/"
            return 1
            ;;
    esac

    local index_url="https://nodejs.org/dist/latest-v${SYRIANA_NODE_TARGET_MAJOR}.x/"
    local tarball
    tarball=$(curl -fsSL "$index_url" \
        | grep -oE "node-v${SYRIANA_NODE_TARGET_MAJOR}\.[0-9]+\.[0-9]+-${node_os}-${node_arch}\.tar\.xz" \
        | head -1)
    if [ -z "$tarball" ]; then
        tarball=$(curl -fsSL "$index_url" \
            | grep -oE "node-v${SYRIANA_NODE_TARGET_MAJOR}\.[0-9]+\.[0-9]+-${node_os}-${node_arch}\.tar\.gz" \
            | head -1)
    fi
    if [ -z "$tarball" ]; then
        _nb_warn "Could not resolve Node $SYRIANA_NODE_TARGET_MAJOR binary for $node_os-$node_arch"
        return 1
    fi

    local tmp
    tmp=$(mktemp -d)
    _nb_log "Downloading $tarball..."
    curl -fsSL "${index_url}${tarball}" -o "$tmp/$tarball" || {
        _nb_warn "Download failed"; rm -rf "$tmp"; return 1
    }

    _nb_log "Extracting to $SYRIANA_HOME/node/..."
    if [[ "$tarball" == *.tar.xz ]]; then
        tar xf  "$tmp/$tarball" -C "$tmp" || { rm -rf "$tmp"; return 1; }
    else
        tar xzf "$tmp/$tarball" -C "$tmp" || { rm -rf "$tmp"; return 1; }
    fi

    local extracted
    extracted=$(find "$tmp" -maxdepth 1 -type d -name 'node-v*' 2>/dev/null | head -1)
    if [ ! -d "$extracted" ]; then
        _nb_warn "Extraction produced no node-v* directory"
        rm -rf "$tmp"
        return 1
    fi

    mkdir -p "$SYRIANA_HOME"
    rm -rf "$SYRIANA_HOME/node"
    mv "$extracted" "$SYRIANA_HOME/node"
    rm -rf "$tmp"

    local _link_dir
    _link_dir="$(_nb_get_link_dir)"
    mkdir -p "$_link_dir"
    ln -sf "$SYRIANA_HOME/node/bin/node" "$_link_dir/node"
    ln -sf "$SYRIANA_HOME/node/bin/npm"  "$_link_dir/npm"
    ln -sf "$SYRIANA_HOME/node/bin/npx"  "$_link_dir/npx"

    _nb_configure_npm_prefix

    export PATH="$SYRIANA_HOME/node/bin:$PATH"

    _nb_have_modern_node || return 1
    _nb_ok "Node $(node --version) installed to $SYRIANA_HOME/node/"
    return 0
}

# ---------------------------------------------------------------------------
# Heal a broken Syriana-managed Node tree (partial upgrade / missing lib/)
# ---------------------------------------------------------------------------

_nb_managed_tool_broken() {
    local tool="$1"
    local probe
    for probe in \
        "$SYRIANA_HOME/node/bin/$tool" \
        "$SYRIANA_HOME/node/${tool}.exe" \
        "$SYRIANA_HOME/node/$tool"; do
        if [ -x "$probe" ] || [ -f "$probe" ]; then
            if ! "$probe" --version >/dev/null 2>&1; then
                return 0
            fi
        fi
    done
    return 1
}

_nb_managed_node_needs_heal() {
    local tool
    for tool in node npm npx; do
        if _nb_managed_tool_broken "$tool"; then
            return 0
        fi
    done
    return 1
}

# Redownload the pinned nodejs.org tarball when a managed tree exists but
# node/npm/npx fail a --version probe. No-op when the tree is healthy or
# absent. Used by syriana_constants.find_syriana_node_executable() and safe
# to call from install reruns.
heal_managed_node() {
    [ -d "$SYRIANA_HOME/node" ] || return 1
    if ! _nb_managed_node_needs_heal; then
        return 0
    fi
    _nb_log "Syriana-managed Node is broken — redownloading to $SYRIANA_HOME/node/..."
    _nb_install_bundled_node
}

# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------

ensure_node() {
    SYRIANA_NODE_AVAILABLE=false

    # Repair pre-existing managed installs where `npm install -g` lands off
    # PATH. No-op when there's no managed Node, so it's safe to run first.
    _nb_configure_npm_prefix

    if _nb_have_modern_node; then
        _nb_ok "Node $(node --version) found"
        SYRIANA_NODE_AVAILABLE=true
        return 0
    fi

    if [ -x "$SYRIANA_HOME/node/bin/node" ]; then
        export PATH="$SYRIANA_HOME/node/bin:$PATH"
        if _nb_have_modern_node; then
            _nb_ok "Node $(node --version) found (Syriana-managed)"
            SYRIANA_NODE_AVAILABLE=true
            return 0
        fi
    fi

    # Version managers first — respect the user's existing setup.
    _nb_try_fnm   && { SYRIANA_NODE_AVAILABLE=true; return 0; }
    _nb_try_proto && { SYRIANA_NODE_AVAILABLE=true; return 0; }
    _nb_try_nvm   && { SYRIANA_NODE_AVAILABLE=true; return 0; }

    # Platform package managers.
    _nb_try_termux_pkg && { SYRIANA_NODE_AVAILABLE=true; return 0; }
    _nb_try_brew       && { SYRIANA_NODE_AVAILABLE=true; return 0; }

    # Last resort: pinned nodejs.org tarball.
    _nb_install_bundled_node && { SYRIANA_NODE_AVAILABLE=true; return 0; }

    _nb_warn "Node.js install failed — TUI and browser tools will be unavailable."
    _nb_warn "Install manually: https://nodejs.org/en/download/  (or: \`brew install node\`, \`fnm install $SYRIANA_NODE_TARGET_MAJOR\`, etc.)"
    return 1
}
