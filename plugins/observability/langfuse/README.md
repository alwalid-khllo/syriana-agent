# Langfuse Observability Plugin

This plugin ships bundled with Syriana but is **opt-in** — it only loads when
you explicitly enable it.

## Enable

Pick one:

```bash
# Interactive: walks you through credentials + SDK install + enable
syriana tools  # → Langfuse Observability

# Manual
pip install langfuse
syriana plugins enable observability/langfuse
```

## Required credentials

Set these in `~/.syriana/.env` (or via `syriana tools`):

```bash
SYRIANA_LANGFUSE_PUBLIC_KEY=pk-lf-...
SYRIANA_LANGFUSE_SECRET_KEY=sk-lf-...
SYRIANA_LANGFUSE_BASE_URL=https://cloud.langfuse.com   # or your self-hosted URL
```

Without the SDK or credentials the hooks no-op silently — the plugin fails
open.

## Verify

```bash
syriana plugins list                 # observability/langfuse should show "enabled"
syriana chat -q "hello"              # then check Langfuse for a "Syriana turn" trace
```

## Optional tuning

```bash
SYRIANA_LANGFUSE_ENV=production       # environment tag
SYRIANA_LANGFUSE_RELEASE=v1.0.0       # release tag
SYRIANA_LANGFUSE_SAMPLE_RATE=0.5      # sample 50% of traces
SYRIANA_LANGFUSE_MAX_CHARS=12000      # max chars per field (default: 12000)
SYRIANA_LANGFUSE_DEBUG=true           # verbose plugin logging
```

## Disable

```bash
syriana plugins disable observability/langfuse
```
