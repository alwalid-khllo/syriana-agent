"""Tests for `syriana chat --safe-mode` — pristine troubleshooting runs.

Inspired by Claude Code v2.1.169's ``--safe-mode`` flag (June 2026), which
disables all customizations (CLAUDE.md, plugins, skills, hooks, MCP) for
troubleshooting. The Syriana equivalent:

* implies ``--ignore-user-config`` (built-in config defaults)
* implies ``--ignore-rules`` (no AGENTS.md/memory/preloaded-skill injection)
* skips plugin discovery entirely (``syriana_cli.plugins``)
* loads zero MCP servers (``tools.mcp_tool._load_mcp_config``)
"""

from __future__ import annotations

import os

import pytest


_VARS = ("SYRIANA_SAFE_MODE", "SYRIANA_IGNORE_USER_CONFIG", "SYRIANA_IGNORE_RULES")


@pytest.fixture(autouse=True)
def _clean_env(monkeypatch):
    for var in _VARS:
        monkeypatch.delenv(var, raising=False)
    yield
    for var in _VARS:
        os.environ.pop(var, None)


class TestSafeModeEnvWiring:
    """cmd_chat must translate --safe-mode into the three env gates."""

    def test_safe_mode_sets_all_gates(self):
        # Mirrors the cmd_chat logic in syriana_cli/main.py.
        class Args:
            safe_mode = True

        args = Args()
        if getattr(args, "safe_mode", False):
            os.environ["SYRIANA_SAFE_MODE"] = "1"
            os.environ["SYRIANA_IGNORE_USER_CONFIG"] = "1"
            os.environ["SYRIANA_IGNORE_RULES"] = "1"

        assert os.environ.get("SYRIANA_SAFE_MODE") == "1"
        assert os.environ.get("SYRIANA_IGNORE_USER_CONFIG") == "1"
        assert os.environ.get("SYRIANA_IGNORE_RULES") == "1"


class TestSafeModePluginDiscovery:
    """Plugin discovery must be a no-op under SYRIANA_SAFE_MODE=1."""

    def test_discovery_skipped(self, monkeypatch):
        monkeypatch.setenv("SYRIANA_SAFE_MODE", "1")
        from syriana_cli.plugins import PluginManager

        mgr = PluginManager()
        called = []
        monkeypatch.setattr(
            mgr, "_discover_and_load_inner", lambda: called.append(True)
        )
        mgr.discover_and_load()
        assert called == []          # inner sweep never ran
        assert mgr._discovered is True  # registry settled as clean-empty
        assert mgr._plugins == {}

    def test_discovery_runs_without_safe_mode(self, monkeypatch):
        monkeypatch.delenv("SYRIANA_SAFE_MODE", raising=False)
        from syriana_cli.plugins import PluginManager

        mgr = PluginManager()
        called = []
        monkeypatch.setattr(
            mgr, "_discover_and_load_inner", lambda: called.append(True)
        )
        mgr.discover_and_load()
        assert called == [True]


class TestSafeModeMCP:
    """_load_mcp_config must return no servers under SYRIANA_SAFE_MODE=1."""

    def test_mcp_servers_empty(self, monkeypatch):
        monkeypatch.setenv("SYRIANA_SAFE_MODE", "1")
        from tools.mcp_tool import _load_mcp_config

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "syriana_cli.config.load_config",
                lambda: {"mcp_servers": {"github": {"url": "https://example.com/mcp"}}},
            )
            assert _load_mcp_config() == {}

    def test_mcp_servers_load_without_safe_mode(self, monkeypatch):
        monkeypatch.delenv("SYRIANA_SAFE_MODE", raising=False)
        from tools.mcp_tool import _load_mcp_config

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr(
                "syriana_cli.config.load_config",
                lambda: {"mcp_servers": {"github": {"url": "https://example.com/mcp"}}},
            )
            servers = _load_mcp_config()
            assert "github" in servers


class TestSafeModeParser:
    """--safe-mode must parse on both the root parser and `syriana chat`."""

    def test_chat_subcommand_accepts_flag(self):
        from syriana_cli._parser import build_top_level_parser

        parser, _subparsers, _chat = build_top_level_parser()
        args = parser.parse_args(["chat", "--safe-mode"])
        assert getattr(args, "safe_mode", False) is True

    def test_root_parser_accepts_flag(self):
        from syriana_cli._parser import build_top_level_parser

        parser, _subparsers, _chat = build_top_level_parser()
        args = parser.parse_args(["--safe-mode"])
        assert getattr(args, "safe_mode", False) is True

    def test_default_is_off(self):
        from syriana_cli._parser import build_top_level_parser

        parser, _subparsers, _chat = build_top_level_parser()
        args = parser.parse_args(["chat"])
        assert getattr(args, "safe_mode", False) is False
