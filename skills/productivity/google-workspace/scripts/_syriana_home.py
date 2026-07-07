"""Resolve SYRIANA_HOME for standalone skill scripts.

Skill scripts may run outside the Syriana process (e.g. system Python,
nix env, CI) where ``syriana_constants`` is not importable.  This module
provides the same ``get_syriana_home()`` and ``display_syriana_home()``
contracts as ``syriana_constants`` without requiring it on ``sys.path``.

When ``syriana_constants`` IS available it is used directly so that any
future enhancements (profile resolution, Docker detection, etc.) are
picked up automatically.  The fallback path replicates the core logic
from ``syriana_constants.py`` using only the stdlib.

All scripts under ``google-workspace/scripts/`` should import from here
instead of duplicating the ``SYRIANA_HOME = Path(os.getenv(...))`` pattern.
"""

from __future__ import annotations

import os
from pathlib import Path

try:
    from syriana_constants import display_syriana_home as display_syriana_home
    from syriana_constants import get_syriana_home as get_syriana_home
except (ModuleNotFoundError, ImportError):

    def get_syriana_home() -> Path:
        """Return the Syriana home directory (default: ~/.syriana).

        Mirrors ``syriana_constants.get_syriana_home()``."""
        val = os.environ.get("SYRIANA_HOME", "").strip()
        return Path(val) if val else Path.home() / ".syriana"

    def display_syriana_home() -> str:
        """Return a user-friendly ``~/``-shortened display string.

        Mirrors ``syriana_constants.display_syriana_home()``."""
        home = get_syriana_home()
        try:
            return "~/" + str(home.relative_to(Path.home()))
        except ValueError:
            return str(home)
