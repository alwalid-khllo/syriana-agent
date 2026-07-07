#!/command/with-contenv sh
# shellcheck shell=sh
# /opt/syriana/docker/main-wrapper.sh — wraps the container's CMD with
# the same argument-routing logic the pre-s6 entrypoint.sh used. Runs
# as /init's "main program" (Docker CMD) so it inherits stdin/stdout/
# stderr from the container.
#
# Shebang note: /init scrubs env before invoking CMD, so a plain
# `#!/bin/sh` wrapper sees an empty environ and `ENV SYRIANA_HOME=/opt/data`
# from the Dockerfile never reaches `syriana`. with-contenv repopulates
# the env from /run/s6/container_environment before exec'ing, which is
# what s6-supervised services use too (see main-syriana/run).
#
# Routing:
#   no args                       → exec `syriana` (the default)
#   first arg is an executable    → exec it directly (sleep, bash, sh, …)
#   first arg is anything else    → exec `syriana <args>` (subcommand passthrough)
#
# Drop to syriana via s6-setuidgid, but skip it when already non-root.
set -e

drop() { [ "$(id -u)" = 0 ] && set -- s6-setuidgid syriana "$@"; exec "$@"; }

# --- Reject the unsupported `docker run --user <uid>:<gid>` start ---
# Mirror the guard in stage2-hook.sh (cont-init). This is the surface the
# user actually sees in `docker run` output: when the container is pinned to
# an arbitrary non-root, non-syriana UID, the bootstrap was skipped and the
# baked image dirs (owned by the syriana build UID) are unwritable, so fail
# fast here with actionable guidance rather than crashing on `cd`/EACCES
# further down. See stage2-hook.sh for the full rationale.
cur_uid="$(id -u)"
if [ "$cur_uid" != 0 ] && [ "$cur_uid" != "$(id -u syriana)" ]; then
    cat >&2 <<EOF
[syriana] ERROR: container started with --user $cur_uid (an arbitrary, non-syriana UID) — not supported.

To make container-written files match your HOST user, don't use --user.
Start as root (the default) and pass your host UID/GID instead:

    docker run -e SYRIANA_UID=\$(id -u) -e SYRIANA_GID=\$(id -g) ...

NAS users (Synology / unRAID / UGOS) can use the PUID/PGID aliases:

    docker run -e PUID=\$(id -u) -e PGID=\$(id -g) ...

The image remaps the syriana user to that UID/GID at boot and chowns the data
volume, so files land owned by your host user — the same outcome --user gave,
without breaking the s6 supervision tree.
EOF
    exit 1
fi

# HOME comes through with-contenv as /root (the /init context). Override
# to the syriana user's home before dropping privileges so libraries that
# resolve paths via $HOME (e.g. discord lockfile under XDG_STATE_HOME)
# don't try to write to /root.
export HOME=/opt/data

# Save the Docker -w (or default) working directory before init
# scripts cd to /opt/data, so the container starts in the
# directory the user requested.
_syriana_orig_cwd="${SYRIANA_ORIG_CWD:-$PWD}"

cd /opt/data
# shellcheck disable=SC1091
. /opt/syriana/.venv/bin/activate

# Restore the original working directory before handing off to
# the user's command so `syriana chat` starts in the Docker -w
# directory, not /opt/data.
cd "$_syriana_orig_cwd"

if [ $# -eq 0 ]; then
    drop syriana
fi

if command -v "$1" >/dev/null 2>&1; then
    # Bare executable — pass through directly.
    drop "$@"
fi

# Syriana subcommand pass-through.
drop syriana "$@"
