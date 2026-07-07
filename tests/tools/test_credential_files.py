"""Tests for credential file passthrough and skills directory mounting."""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from tools.credential_files import (
    clear_credential_files,
    get_credential_file_mounts,
    get_cache_directory_mounts,
    get_skills_directory_mount,
    iter_cache_files,
    iter_skills_files,
    map_cache_path_to_container,
    register_credential_file,
    register_credential_files,
)


@pytest.fixture(autouse=True)
def _clean_state():
    """Reset module state between tests."""
    import tools.credential_files as _cred_mod
    clear_credential_files()
    _cred_mod._config_files = None
    yield
    clear_credential_files()
    _cred_mod._config_files = None


class TestRegisterCredentialFiles:
    def test_dict_with_path_key(self, tmp_path):
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        (syriana_home / "token.json").write_text("{}")

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            missing = register_credential_files([{"path": "token.json"}])

        assert missing == []
        mounts = get_credential_file_mounts()
        assert len(mounts) == 1
        assert mounts[0]["host_path"] == str(syriana_home / "token.json")
        assert mounts[0]["container_path"] == "/root/.syriana/token.json"

    def test_dict_with_name_key_fallback(self, tmp_path):
        """Skills use 'name' instead of 'path' — both should work."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        (syriana_home / "google_token.json").write_text("{}")

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            missing = register_credential_files([
                {"name": "google_token.json", "description": "OAuth token"},
            ])

        assert missing == []
        mounts = get_credential_file_mounts()
        assert len(mounts) == 1
        assert "google_token.json" in mounts[0]["container_path"]

    def test_string_entry(self, tmp_path):
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        (syriana_home / "secret.key").write_text("key")

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            missing = register_credential_files(["secret.key"])

        assert missing == []
        mounts = get_credential_file_mounts()
        assert len(mounts) == 1

    def test_missing_file_reported(self, tmp_path):
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            missing = register_credential_files([
                {"name": "does_not_exist.json"},
            ])

        assert "does_not_exist.json" in missing
        assert get_credential_file_mounts() == []

    def test_path_takes_precedence_over_name(self, tmp_path):
        """When both path and name are present, path wins."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        (syriana_home / "real.json").write_text("{}")

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            missing = register_credential_files([
                {"path": "real.json", "name": "wrong.json"},
            ])

        assert missing == []
        mounts = get_credential_file_mounts()
        assert "real.json" in mounts[0]["container_path"]


class TestSkillsDirectoryMount:
    def test_returns_mount_when_skills_dir_exists(self, tmp_path):
        syriana_home = tmp_path / ".syriana"
        skills_dir = syriana_home / "skills"
        skills_dir.mkdir(parents=True)
        (skills_dir / "test-skill").mkdir()
        (skills_dir / "test-skill" / "SKILL.md").write_text("# test")

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            mounts = get_skills_directory_mount()

        assert len(mounts) >= 1
        assert mounts[0]["host_path"] == str(skills_dir)
        assert mounts[0]["container_path"] == "/root/.syriana/skills"

    def test_returns_none_when_no_skills_dir(self, tmp_path):
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            mounts = get_skills_directory_mount()

        # No local skills dir → no local mount (external dirs may still appear)
        local_mounts = [m for m in mounts if m["container_path"].endswith("/skills")]
        assert local_mounts == []

    def test_custom_container_base(self, tmp_path):
        syriana_home = tmp_path / ".syriana"
        (syriana_home / "skills").mkdir(parents=True)

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            mounts = get_skills_directory_mount(container_base="/home/user/.syriana")

        assert mounts[0]["container_path"] == "/home/user/.syriana/skills"

    def test_symlinks_are_sanitized(self, tmp_path):
        """Symlinks in skills dir should be excluded from the mount."""
        syriana_home = tmp_path / ".syriana"
        skills_dir = syriana_home / "skills"
        skills_dir.mkdir(parents=True)
        (skills_dir / "legit.md").write_text("# real skill")
        # Create a symlink pointing outside the skills tree
        secret = tmp_path / "secret.txt"
        secret.write_text("TOP SECRET")
        (skills_dir / "evil_link").symlink_to(secret)

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            mounts = get_skills_directory_mount()

        assert len(mounts) >= 1
        mount = mounts[0]
        # The mount path should be a sanitized copy, not the original
        safe_path = Path(mount["host_path"])
        assert safe_path != skills_dir
        # Legitimate file should be present
        assert (safe_path / "legit.md").exists()
        assert (safe_path / "legit.md").read_text() == "# real skill"
        # Symlink should NOT be present
        assert not (safe_path / "evil_link").exists()

    def test_no_symlinks_returns_original_dir(self, tmp_path):
        """When no symlinks exist, the original dir is returned (no copy)."""
        syriana_home = tmp_path / ".syriana"
        skills_dir = syriana_home / "skills"
        skills_dir.mkdir(parents=True)
        (skills_dir / "skill.md").write_text("ok")

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            mounts = get_skills_directory_mount()

        assert mounts[0]["host_path"] == str(skills_dir)


class TestIterSkillsFiles:
    def test_returns_files_skipping_symlinks(self, tmp_path):
        syriana_home = tmp_path / ".syriana"
        skills_dir = syriana_home / "skills"
        (skills_dir / "cat" / "myskill").mkdir(parents=True)
        (skills_dir / "cat" / "myskill" / "SKILL.md").write_text("# skill")
        (skills_dir / "cat" / "myskill" / "scripts").mkdir()
        (skills_dir / "cat" / "myskill" / "scripts" / "run.sh").write_text("#!/bin/bash")
        # Add a symlink that should be filtered
        secret = tmp_path / "secret"
        secret.write_text("nope")
        (skills_dir / "cat" / "myskill" / "evil").symlink_to(secret)

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            files = iter_skills_files()

        paths = {f["container_path"] for f in files}
        assert "/root/.syriana/skills/cat/myskill/SKILL.md" in paths
        assert "/root/.syriana/skills/cat/myskill/scripts/run.sh" in paths
        # Symlink should be excluded
        assert not any("evil" in f["container_path"] for f in files)

    def test_empty_when_no_skills_dir(self, tmp_path):
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()

        with patch.dict(os.environ, {"SYRIANA_HOME": str(syriana_home)}):
            assert iter_skills_files() == []

class TestPathTraversalSecurity:
    """Path traversal and absolute path rejection.

    A malicious skill could declare::

        required_credential_files:
          - path: '../../.ssh/id_rsa'

    Without containment checks, this would mount the host's SSH private key
    into the container sandbox, leaking it to the skill's execution environment.
    """

    def test_dotdot_traversal_rejected(self, tmp_path, monkeypatch):
        """'../sensitive' must not escape SYRIANA_HOME."""
        monkeypatch.setenv("SYRIANA_HOME", str(tmp_path / ".syriana"))
        (tmp_path / ".syriana").mkdir()

        # Create a sensitive file one level above syriana_home
        sensitive = tmp_path / "sensitive.json"
        sensitive.write_text('{"secret": "value"}')

        result = register_credential_file("../sensitive.json")

        assert result is False
        assert get_credential_file_mounts() == []

    def test_deep_traversal_rejected(self, tmp_path, monkeypatch):
        """'../../etc/passwd' style traversal must be rejected."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        # Create a fake sensitive file outside syriana_home
        ssh_dir = tmp_path / ".ssh"
        ssh_dir.mkdir()
        (ssh_dir / "id_rsa").write_text("PRIVATE KEY")

        result = register_credential_file("../../.ssh/id_rsa")

        assert result is False
        assert get_credential_file_mounts() == []

    def test_absolute_path_rejected(self, tmp_path, monkeypatch):
        """Absolute paths must be rejected regardless of whether they exist."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        # Create a file at an absolute path
        sensitive = tmp_path / "absolute.json"
        sensitive.write_text("{}")

        result = register_credential_file(str(sensitive))

        assert result is False
        assert get_credential_file_mounts() == []

    def test_legitimate_file_still_works(self, tmp_path, monkeypatch):
        """Normal files inside SYRIANA_HOME must still be registered."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))
        (syriana_home / "token.json").write_text('{"token": "abc"}')

        result = register_credential_file("token.json")

        assert result is True
        mounts = get_credential_file_mounts()
        assert len(mounts) == 1
        assert "token.json" in mounts[0]["container_path"]

    def test_nested_subdir_inside_syriana_home_allowed(self, tmp_path, monkeypatch):
        """Files in subdirectories of SYRIANA_HOME must be allowed."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        subdir = syriana_home / "creds"
        subdir.mkdir()
        (subdir / "oauth.json").write_text("{}")
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        result = register_credential_file("creds/oauth.json")

        assert result is True

    def test_symlink_traversal_rejected(self, tmp_path, monkeypatch):
        """A symlink inside SYRIANA_HOME pointing outside must be rejected."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        # Create a sensitive file outside syriana_home
        sensitive = tmp_path / "sensitive.json"
        sensitive.write_text('{"secret": "value"}')

        # Create a symlink inside syriana_home pointing outside
        symlink = syriana_home / "evil_link.json"
        try:
            symlink.symlink_to(sensitive)
        except (OSError, NotImplementedError):
            pytest.skip("Symlinks not supported on this platform")

        result = register_credential_file("evil_link.json")

        # The resolved path escapes SYRIANA_HOME — must be rejected
        assert result is False
        assert get_credential_file_mounts() == []


# ---------------------------------------------------------------------------
# Config-based credential files — same containment checks
# ---------------------------------------------------------------------------

class TestConfigPathTraversal:
    """terminal.credential_files in config.yaml must also reject traversal."""

    def _write_config(self, syriana_home: Path, cred_files: list):
        import yaml
        config_path = syriana_home / "config.yaml"
        config_path.write_text(yaml.dump({"terminal": {"credential_files": cred_files}}))

    def test_config_traversal_rejected(self, tmp_path, monkeypatch):
        """'../secret' in config.yaml must not escape SYRIANA_HOME."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        sensitive = tmp_path / "secret.json"
        sensitive.write_text("{}")
        self._write_config(syriana_home, ["../secret.json"])

        mounts = get_credential_file_mounts()
        host_paths = [m["host_path"] for m in mounts]
        assert str(sensitive) not in host_paths
        assert str(sensitive.resolve()) not in host_paths

    def test_config_absolute_path_rejected(self, tmp_path, monkeypatch):
        """Absolute paths in config.yaml must be rejected."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        sensitive = tmp_path / "abs.json"
        sensitive.write_text("{}")
        self._write_config(syriana_home, [str(sensitive)])

        mounts = get_credential_file_mounts()
        assert mounts == []

    def test_config_legitimate_file_works(self, tmp_path, monkeypatch):
        """Normal files inside SYRIANA_HOME via config must still mount."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        (syriana_home / "oauth.json").write_text("{}")
        self._write_config(syriana_home, ["oauth.json"])

        mounts = get_credential_file_mounts()
        assert len(mounts) == 1
        assert "oauth.json" in mounts[0]["container_path"]


# ---------------------------------------------------------------------------
# Cache directory mounts
# ---------------------------------------------------------------------------

class TestCacheDirectoryMounts:
    """Tests for get_cache_directory_mounts() and iter_cache_files()."""

    def test_returns_existing_cache_dirs(self, tmp_path, monkeypatch):
        """Existing cache dirs are returned with correct container paths."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        (syriana_home / "cache" / "documents").mkdir(parents=True)
        (syriana_home / "cache" / "audio").mkdir(parents=True)
        (syriana_home / "cache" / "videos").mkdir(parents=True)
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        mounts = get_cache_directory_mounts()
        paths = {m["container_path"] for m in mounts}
        assert "/root/.syriana/cache/documents" in paths
        assert "/root/.syriana/cache/audio" in paths
        assert "/root/.syriana/cache/videos" in paths

    def test_skips_nonexistent_dirs(self, tmp_path, monkeypatch):
        """Dirs that don't exist on disk are not returned."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        # Create only one cache dir
        (syriana_home / "cache" / "documents").mkdir(parents=True)
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        mounts = get_cache_directory_mounts()
        assert len(mounts) == 1
        assert mounts[0]["container_path"] == "/root/.syriana/cache/documents"

    def test_legacy_dir_names_resolved(self, tmp_path, monkeypatch):
        """Old-style dir names (e.g. document_cache) are resolved correctly.

        Populates the legacy dirs with a sentinel file so they count as
        ``has content`` for ``get_syriana_dir``'s populated-legacy check
        (see #27602 — empty legacy stubs are no longer honoured).
        """
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        # Use legacy dir name with content — get_syriana_dir prefers
        # populated old over new.
        legacy_doc = syriana_home / "document_cache"
        legacy_img = syriana_home / "image_cache"
        legacy_doc.mkdir()
        legacy_img.mkdir()
        (legacy_doc / "cached.txt").write_bytes(b"x")
        (legacy_img / "cached.png").write_bytes(b"x")
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        mounts = get_cache_directory_mounts()
        host_paths = {m["host_path"] for m in mounts}
        assert str(syriana_home / "document_cache") in host_paths
        assert str(syriana_home / "image_cache") in host_paths
        # Container paths always use the new layout
        container_paths = {m["container_path"] for m in mounts}
        assert "/root/.syriana/cache/documents" in container_paths
        assert "/root/.syriana/cache/images" in container_paths

    def test_empty_syriana_home(self, tmp_path, monkeypatch):
        """No cache dirs → empty list."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        assert get_cache_directory_mounts() == []


class TestMapCachePathToContainer:
    """Tests for map_cache_path_to_container() — the backend-agnostic mapper."""

    def test_maps_path_under_cache_dir(self, tmp_path, monkeypatch):
        syriana_home = tmp_path / ".syriana"
        img_dir = syriana_home / "cache" / "images"
        img_dir.mkdir(parents=True)
        host_path = str(img_dir / "generated.png")
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        assert (
            map_cache_path_to_container(host_path)
            == "/root/.syriana/cache/images/generated.png"
        )

    def test_custom_container_base_for_remote_home(self, tmp_path, monkeypatch):
        syriana_home = tmp_path / ".syriana"
        img_dir = syriana_home / "cache" / "images"
        img_dir.mkdir(parents=True)
        host_path = str(img_dir / "remote.png")
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        assert (
            map_cache_path_to_container(host_path, container_base="/home/agent/.syriana")
            == "/home/agent/.syriana/cache/images/remote.png"
        )

    def test_returns_none_when_outside_cache_dirs(self, tmp_path, monkeypatch):
        syriana_home = tmp_path / ".syriana"
        (syriana_home / "cache" / "images").mkdir(parents=True)
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        assert map_cache_path_to_container(str(tmp_path / "elsewhere.png")) is None

    def test_returns_none_when_no_cache_dirs_exist(self, tmp_path, monkeypatch):
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        assert map_cache_path_to_container(str(syriana_home / "cache" / "images" / "x.png")) is None


class TestIterCacheFiles:
    """Tests for iter_cache_files()."""

    def test_enumerates_files(self, tmp_path, monkeypatch):
        """Regular files in cache dirs are returned."""
        syriana_home = tmp_path / ".syriana"
        doc_dir = syriana_home / "cache" / "documents"
        doc_dir.mkdir(parents=True)
        (doc_dir / "upload.zip").write_bytes(b"PK\x03\x04")
        (doc_dir / "report.pdf").write_bytes(b"%PDF-1.4")
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        entries = iter_cache_files()
        names = {Path(e["container_path"]).name for e in entries}
        assert "upload.zip" in names
        assert "report.pdf" in names

    def test_skips_symlinks(self, tmp_path, monkeypatch):
        """Symlinks inside cache dirs are skipped."""
        syriana_home = tmp_path / ".syriana"
        doc_dir = syriana_home / "cache" / "documents"
        doc_dir.mkdir(parents=True)
        real_file = doc_dir / "real.txt"
        real_file.write_text("content")
        (doc_dir / "link.txt").symlink_to(real_file)
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        entries = iter_cache_files()
        names = [Path(e["container_path"]).name for e in entries]
        assert "real.txt" in names
        assert "link.txt" not in names

    def test_nested_files(self, tmp_path, monkeypatch):
        """Files in subdirectories are included with correct relative paths."""
        syriana_home = tmp_path / ".syriana"
        ss_dir = syriana_home / "cache" / "screenshots"
        sub = ss_dir / "session_abc"
        sub.mkdir(parents=True)
        (sub / "screen1.png").write_bytes(b"PNG")
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        entries = iter_cache_files()
        assert len(entries) == 1
        assert entries[0]["container_path"] == "/root/.syriana/cache/screenshots/session_abc/screen1.png"

    def test_empty_cache(self, tmp_path, monkeypatch):
        """No cache dirs → empty list."""
        syriana_home = tmp_path / ".syriana"
        syriana_home.mkdir()
        monkeypatch.setenv("SYRIANA_HOME", str(syriana_home))

        assert iter_cache_files() == []
