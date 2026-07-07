from pathlib import Path


def test_windows_native_install_path_docs_match_installer() -> None:
    doc = Path("website/docs/user-guide/windows-native.md").read_text()
    install = Path("scripts/install.ps1").read_text()

    assert "%LOCALAPPDATA%\\syriana\\syriana-agent\\venv\\Scripts" in doc
    assert "Get-Command syriana        # should print C:\\Users\\<you>\\AppData\\Local\\syriana\\syriana-agent\\venv\\Scripts\\syriana.exe" in doc
    assert '$syrianaBin = "$InstallDir\\venv\\Scripts"' in install
