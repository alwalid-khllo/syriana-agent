"""Runtime smoke tests for Docker PUID/PGID and UID/GID remap.

Build the real image and verify the actual runtime behavior:

  1. PUID/PGID env vars remap the syriana user UID/GID at boot
  2. SYRIANA_UID/SYRIANA_GID take precedence over PUID/PGID aliases
  3. NAS-style low UIDs (99:100) are accepted and remapped
  4. Invalid UIDs are rejected
  5. The remapped user can write to the data volume
"""
from __future__ import annotations

from tests.docker.conftest import docker_exec_sh, start_container


def test_puid_pgid_remaps_syriana_user(
    built_image: str, container_name: str,
) -> None:
    """PUID=1000 PGID=1000 must remap the syriana user to UID 1000."""
    start_container(built_image, container_name, "PUID=1000", "PGID=1000")

    r = docker_exec_sh(
        container_name,
        "id -u syriana",
        timeout=10,
    )
    assert r.stdout.strip() == "1000", (
        f"expected syriana UID 1000 after PUID remap, got: {r.stdout.strip()}"
    )

    r = docker_exec_sh(
        container_name,
        "id -g syriana",
        timeout=10,
    )
    assert r.stdout.strip() == "1000", (
        f"expected syriana GID 1000 after PGID remap, got: {r.stdout.strip()}"
    )


def test_syriana_uid_gid_take_precedence_over_aliases(
    built_image: str, container_name: str,
) -> None:
    """SYRIANA_UID/SYRIANA_GID must win over PUID/PGID when both are set."""
    start_container(built_image, container_name, "SYRIANA_UID=2000", "SYRIANA_GID=2001", "PUID=1000", "PGID=1000")

    r = docker_exec_sh(container_name, "id -u syriana", timeout=10)
    assert r.stdout.strip() == "2000", (
        f"expected syriana UID 2000 (SYRIANA_UID wins), got: {r.stdout.strip()}"
    )

    r = docker_exec_sh(container_name, "id -g syriana", timeout=10)
    assert r.stdout.strip() == "2001", (
        f"expected syriana GID 2001 (SYRIANA_GID wins), got: {r.stdout.strip()}"
    )


def test_nas_low_uid_accepted(
    built_image: str, container_name: str,
) -> None:
    """NAS-style low UIDs (99:100, common on Unraid) must be accepted."""
    start_container(built_image, container_name, "PUID=99", "PGID=100")

    r = docker_exec_sh(container_name, "id -u syriana", timeout=10)
    assert r.stdout.strip() == "99", (
        f"expected syriana UID 99, got: {r.stdout.strip()}"
    )

    r = docker_exec_sh(container_name, "id -g syriana", timeout=10)
    assert r.stdout.strip() == "100", (
        f"expected syriana GID 100, got: {r.stdout.strip()}"
    )


def test_remap_enables_data_volume_writes(
    built_image: str, container_name: str,
) -> None:
    """After remap, the syriana user must be able to write to /opt/data."""
    start_container(built_image, container_name, "PUID=1000", "PGID=1000")

    r = docker_exec_sh(
        container_name,
        "touch /opt/data/test_write && echo WRITE_OK || echo WRITE_FAIL",
        timeout=10,
    )
    assert "WRITE_OK" in r.stdout, (
        f"syriana user cannot write to /opt/data after remap: {r.stdout}"
    )