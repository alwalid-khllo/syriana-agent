# Mem0 Memory Provider

Server-side LLM fact extraction with semantic search and hybrid multi-signal retrieval via the Mem0 Platform v3 API.

## Requirements

- `pip install mem0ai`
- Mem0 API key from [app.mem0.ai](https://app.mem0.ai)

## Setup

```bash
syriana memory setup    # select "mem0"
```

Or manually:
```bash
syriana config set memory.provider mem0
echo "MEM0_API_KEY=your-key" >> ~/.syriana/.env
```

## Config

Behavioral settings live in `$SYRIANA_HOME/mem0.json` (set them via `syriana memory setup`). Only the secret `MEM0_API_KEY` belongs in `~/.syriana/.env`.

| Key | Default | Description |
|-----|---------|-------------|
| `mode` | `platform` | `platform` (Mem0 Cloud) or `oss` (self-hosted) |
| `user_id` | `syriana-user` | User identifier on Mem0 |
| `agent_id` | `syriana` | Agent identifier |
| `rerank` | `true` | Rerank search results for relevance (platform mode only) |

## OSS (Self-Hosted) Mode

Run Mem0 locally with your own LLM, embedder, and vector store.

### Interactive Setup

```bash
syriana memory setup
# Select "mem0" → "Open Source (self-hosted)"
# Follow prompts for LLM, embedder, and vector store
```

### Agent-Driven Setup (Flags)

```bash
syriana memory setup mem0 --mode oss \
  --oss-llm openai --oss-llm-key sk-... \
  --oss-vector qdrant
```

### Supported Providers

| Component | Providers |
|-----------|-----------|
| LLM | openai, ollama |
| Embedder | openai, ollama |
| Vector Store | qdrant (local/server), pgvector |

### Flags Reference

| Flag | Description |
|------|-------------|
| `--mode` | `platform` or `oss` |
| `--oss-llm` | LLM provider (default: openai) |
| `--oss-llm-key` | LLM API key |
| `--oss-embedder` | Embedder provider (default: openai) |
| `--oss-vector` | Vector store (default: qdrant) |
| `--oss-vector-path` | Qdrant local path |
| `--user-id` | User identifier |

## Switching Modes

### Platform to OSS

```bash
syriana memory setup mem0 --mode oss --oss-llm-key sk-...
```

Or edit `$SYRIANA_HOME/mem0.json` directly:
```json
{
  "mode": "oss",
  "oss": {
    "llm": {"provider": "openai", "config": {"model": "gpt-5-mini"}},
    "embedder": {"provider": "openai", "config": {"model": "text-embedding-3-small"}},
    "vector_store": {"provider": "qdrant", "config": {"path": "~/.syriana/mem0_qdrant"}}
  }
}
```

### OSS to Platform

```bash
syriana memory setup mem0 --mode platform --api-key sk-...
```

### Dry Run (preview without writing)

```bash
syriana memory setup mem0 --mode oss --oss-llm-key sk-... --dry-run
```

## Tools

| Tool | Description |
|------|-------------|
| `mem0_list` | List all stored memories (paginated) |
| `mem0_search` | Semantic search by meaning |
| `mem0_add` | Store a fact verbatim (no LLM extraction) |
| `mem0_update` | Update a memory's text by ID |
| `mem0_delete` | Delete a memory by ID |

## Troubleshooting

### "Mem0 temporarily unavailable"

Circuit breaker tripped after 5 consecutive failures. Resets after 2 minutes.

- **Platform mode**: Check API key and internet connectivity.
- **OSS mode**: Check that your vector store (qdrant/pgvector) is running.

### OSS: Qdrant connection refused

```bash
# If using local Qdrant, check the storage path is writable:
ls -la ~/.syriana/mem0_qdrant

# If using Qdrant server, check it's reachable:
curl http://localhost:6333/healthz
```

### OSS: PGVector connection refused

```bash
# Verify PostgreSQL is running and accepting connections:
pg_isready -h localhost -p 5432
```

### OSS: Ollama not reachable

```bash
# Check Ollama is running:
curl http://localhost:11434/api/tags
```

### Memories not appearing

- `mem0_add` stores verbatim (no extraction). Use `sync_turn` for LLM extraction.
- Search uses semantic matching — try broader queries.
- Check `user_id` matches between sessions (`$SYRIANA_HOME/mem0.json`).
