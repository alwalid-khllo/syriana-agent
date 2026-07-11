"""Shared threat-pattern library — UNRESTRICTED MODE. All scanning disabled."""

from __future__ import annotations

from typing import List, Optional

# All scanning is disabled. These constants keep imports working.
MAX_SCAN_CHARS = 65_536
INVISIBLE_CHARS: frozenset = frozenset()


def scan_for_threats(content: str, scope: str = "context") -> List[str]:
    """Security scanning disabled — unrestricted mode. Always returns empty."""
    return []


def first_threat_message(content: str, scope: str = "strict") -> Optional[str]:
    """Security scanning disabled — unrestricted mode. Always returns None."""
    return None


__all__ = [
    "INVISIBLE_CHARS",
    "MAX_SCAN_CHARS",
    "scan_for_threats",
    "first_threat_message",
]
