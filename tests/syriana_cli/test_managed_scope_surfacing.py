"""Surfacing tests — managed scope shown in `config show` and `syriana doctor`."""
import pytest


@pytest.fixture
def homes(tmp_path, monkeypatch):
    home = tmp_path / "home"
    home.mkdir()
    managed = tmp_path / "managed"
    managed.mkdir()
    monkeypatch.setenv("SYRIANA_HOME", str(home))
    monkeypatch.setenv("SYRIANA_MANAGED_DIR", str(managed))
    (home / "config.yaml").write_text("model:\n  default: user/model\n", encoding="utf-8")
    (managed / "config.yaml").write_text(
        "model:\n  default: managed/model\n", encoding="utf-8"
    )
    import syriana_cli.config as cfg
    from syriana_cli import managed_scope

    cfg._LOAD_CONFIG_CACHE.clear()
    cfg._RAW_CONFIG_CACHE.clear()
    managed_scope.invalidate_managed_cache()
    return home, managed


def test_config_show_flags_managed(homes, capsys):
    from syriana_cli.config import show_config

    show_config()
    out = capsys.readouterr().out.lower()
    assert "managed" in out  # header + key list present
    assert "model.default" in out  # the pinned key is named
    assert "managed/model" in out  # effective (managed) value, not user/model


def test_config_show_no_managed_scope_silent(tmp_path, monkeypatch, capsys):
    """With no managed scope, the managed header must not appear."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("SYRIANA_HOME", str(home))
    monkeypatch.setenv("SYRIANA_MANAGED_DIR", str(tmp_path / "nope"))
    (home / "config.yaml").write_text("model:\n  default: user/model\n", encoding="utf-8")
    import syriana_cli.config as cfg
    from syriana_cli import managed_scope

    cfg._LOAD_CONFIG_CACHE.clear()
    cfg._RAW_CONFIG_CACHE.clear()
    managed_scope.invalidate_managed_cache()
    from syriana_cli.config import show_config

    show_config()
    out = capsys.readouterr().out.lower()
    assert "managed by your administrator" not in out


def test_doctor_reports_managed_scope(homes, capsys):
    # homes fixture has 1 managed config key (model.default) and 0 managed env keys.
    from syriana_cli import doctor

    doctor.managed_scope_check()
    out = capsys.readouterr().out.lower()
    assert "managed scope active" in out
    assert str(homes[1]).lower() in out  # resolved dir reported
    assert "1 config key" in out


def test_doctor_silent_with_no_managed_scope(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("SYRIANA_MANAGED_DIR", str(tmp_path / "nope"))
    from syriana_cli import managed_scope, doctor

    managed_scope.invalidate_managed_cache()
    doctor.managed_scope_check()
    assert capsys.readouterr().out.strip() == ""
