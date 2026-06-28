# Polymarket MCP — Project Knowledge Base

Onboarding reference for engineers joining `polymarket-mcp`.

## Project at a Glance

**Polymarket MCP** is a Python MCP server that lets AI agents query Polymarket prediction market data through a standard tool-calling interface. It wraps Polymarket's public **Gamma** (market metadata) and **Data** (user/portfolio) APIs. It does not place trades or access the CLOB order book.

**Maturity:** Early prototype. 7 tools, 3 resources, and 3 prompts implemented. Test suite covers formatters, helpers, config, and server registration.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Client (Cursor, Inspector)            │
└────────────────────────────┬────────────────────────────────┘
                             │ streamable-http :8000
┌────────────────────────────▼────────────────────────────────┐
│                      polymarket-mcp                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  server.py   │→ │  helpers.py  │→ │  Polymarket APIs     │ │
│  │ tools        │  │  (HTTP)      │  │  gamma + data        │ │
│  │ resources    │  └──────────────┘  └──────────────────────┘ │
│  │ prompts      │                                            │
│  └──────┬───────┘                                            │
│         │                                                    │
│         ▼                                                    │
│  ┌──────────────┐     ┌──────────────┐                       │
│  │ formatters.py│     │ content/*.md │  static resources     │
│  └──────────────┘     └──────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### API Boundaries

| API | Base URL | Used For |
|-----|----------|----------|
| **Gamma** | `https://gamma-api.polymarket.com` | Market search, market details by slug |
| **Data** | `https://data-api.polymarket.com` | User positions, portfolio value, leaderboard |

No **CLOB** (order book / trading) integration exists yet — read-only only.

### Transport & Deployment

- **Transport:** `streamable-http` (HTTP-based MCP, not stdio)
- **Port:** 8000
- **Runtime:** Python 3.12, managed with `uv`
- **Container:** Slim Python 3.12 Docker image

---

## Folder Structure

```
polymarket-mcp/
├── src/
│   └── polymarket_mcp/          # Main Python package
│       ├── __init__.py          # Package marker
│       ├── server.py            # MCP server: tools, resources, prompts
│       ├── config.py            # Pydantic settings (API URLs, timeout)
│       ├── content/             # Static markdown for MCP resources
│       │   ├── glossary.md
│       │   ├── categories.md
│       │   └── tool-guide.md
│       └── utils/
│           ├── helpers.py       # HTTP client + MCP response wrappers
│           └── formatters.py    # API JSON → markdown formatters
├── docs/
│   └── PROJECT_KNOWLEDGE_BASE.md
├── pyproject.toml               # Project metadata & dependencies
├── uv.lock                      # Locked dependency versions
├── Makefile                     # Dev shortcuts (run, inspector, docker)
├── Dockerfile                   # Container build & run config
└── README.md
```

| File | Role |
|------|------|
| `server.py` | Creates `FastMCP` instance; registers tools, resources, prompts; runs the server |
| `content/` | Static markdown served as MCP resources (`polymarket://glossary`, etc.) |
| `config.py` | `Settings` via `pydantic_settings.BaseSettings` — API URLs and timeout |
| `utils/helpers.py` | Async `get()` via httpx; `text()` and `err()` for MCP responses |
| `utils/formatters.py` | Pure functions: API dicts → markdown strings |

---

## Tool Inventory

| Tool | Status | APIs Called |
|------|--------|-------------|
| `get_user_positions` | Implemented | `data /positions` |
| `search_markets` | Implemented | `gamma /public-search` |
| `get_market_details` | Implemented | `gamma /markets/slug/{slug}` |
| `get_user_performance` | Implemented | `data /value` + `data /v1/leaderboard` (parallel) |
| `get_trending_markets` | Implemented | `gamma /events` |
| `get_leaderboard` | Implemented | `data /v1/leaderboard` |
| `get_market_holders` | Implemented | `gamma /markets/slug/{slug}` + `data /holders` |
| `get_orderbook` | Planned | CLOB |
| `get_recent_trades` | Planned | CLOB |

## Resources

| URI | Source |
|-----|--------|
| `polymarket://glossary` | `content/glossary.md` |
| `polymarket://categories` | `content/categories.md` |
| `polymarket://tool-guide` | `content/tool-guide.md` |

## Prompts

| Prompt | Purpose |
|--------|---------|
| `research_market` | Details → holders → summary |
| `compare_traders` | Compare two wallets |
| `scan_trending` | Trending scan with optional tag filter |

---

## Request Flow

```
Agent calls tool (e.g. search_markets)
    ↓
server.py builds API params
    ↓
helpers.get() → httpx GET → Polymarket API
    ↓
formatters.format_*() → markdown string
    ↓
helpers.text() → MCP TextContent (JSON-encoded)
    ↓
Agent receives formatted result
```

For `get_user_performance`, two API calls run in parallel via `asyncio.gather` before formatting.

---

## Polymarket API Map

| Tool | HTTP Call |
|------|-----------|
| `search_markets` | `GET gamma/public-search?q=...&limit_per_type=...&events_status=active` |
| `get_market_details` | `GET gamma/markets/slug/{slug}` |
| `get_user_positions` | `GET data/positions?user=...&limit=...&offset=...` |
| `get_user_performance` | `GET data/value?user=...` + `GET data/v1/leaderboard?user=...&category=...&timePeriod=...` |

**Slug extraction:** `get_market_details` accepts a `market_link` and extracts the last path segment as the slug.

---

## Design Patterns

| Pattern | Where | Description |
|---------|-------|-------------|
| MCP Tool Handler | `server.py` | Async functions with `@mcp.tool()`; docstrings become agent-facing descriptions |
| Settings Object | `config.py` | Pydantic `BaseSettings` centralizes external service URLs |
| Thin HTTP Gateway | `helpers.get()` | Single async GET wrapper; filters `None` params, raises on HTTP errors |
| Formatter / Presenter | `formatters.py` | Separates API response shape from agent-facing output |
| Parallel Fan-out | `get_user_performance` | `asyncio.gather(..., return_exceptions=True)` with per-call error handling |
| Literal Types | `server.py` | `Category` and `TimePeriod` constrain MCP client option sets |

---

## Coding Conventions

| Convention | Detail |
|------------|--------|
| Python | 3.12+ |
| Package manager | `uv` only — `uv add`, `uv run --frozen`, `uv sync` |
| Type hints | Required; use modern syntax (`str \| None`, `list[dict]`) |
| Async | All tools and HTTP calls are `async` |
| Tool docstrings | Describe what the tool returns, not just parameters |
| Response format | Markdown with `#` / `##` headers; returned via `text(formatter(data))` |
| Error handling | Input validation returns plain strings; API failures use `err()` or `return_exceptions=True` |
| Null params | Filter `None` values before sending to APIs |
| Imports | Flat style: `from config import Settings` (requires `PYTHONPATH` including `src/`) |

---

## Quick Start

```bash
uv sync
make run          # streamable-http on port 8000
make inspector    # MCP Inspector for manual testing
make build        # Docker image
make start        # Run container on localhost:8000
```

Connect an MCP client to `http://localhost:8000` using the `streamable-http` transport.

---

## Adding a New Tool

1. Add a formatter in `utils/formatters.py` — pure function, API dict → markdown string.
2. Add a tool in `server.py`:

```python
@mcp.tool()
async def my_new_tool(param: str, limit: int = 10):
    """Clear description for the agent."""
    data = await get(f"{gamma_url}/some-endpoint", params={"key": param})
    return text(format_my_new_tool(data))
```

3. Test with `make inspector` or your MCP client.
4. Update README when the tool is stable.

For multi-API tools, follow the `get_user_performance` pattern: build tasks, `asyncio.gather`, handle exceptions per call.

---

## Configuration

```python
class Settings(BaseSettings):
    gamma_url: str = "https://gamma-api.polymarket.com"
    data_url: str = "https://data-api.polymarket.com"
    default_timeout: int = 15
```

Override via environment variables (`GAMMA_URL`, `DATA_URL`, etc.) — supported by Pydantic `BaseSettings`.

---

## Response Contract

All tools return `list[types.TextContent]` where `text` is a JSON-encoded string of markdown:

```python
def text(data: str) -> list[types.TextContent]:
    return [types.TextContent(type="text", text=json.dumps(data, indent=2))]
```

---

## Key Dependencies

| Package | Role |
|---------|------|
| `mcp` | MCP SDK; `FastMCP` server framework |
| `httpx` | Async HTTP client for Polymarket APIs |
| `pydantic-settings` | Configuration management |
| `dotenv` | Environment variable loading |

---

## Gotchas

1. **Flat imports** — `from config import Settings`, not `from polymarket_mcp.config import Settings`. Requires `PYTHONPATH` to include `src/`.
2. **No tests** — Manual testing via MCP Inspector is the current workflow.
3. **Transitive dependencies** — `httpx` and `pydantic-settings` should be declared in `pyproject.toml` if used directly.
4. **Timeout mismatch** — `Settings.default_timeout` exists but `helpers.get()` hardcodes 15s.
5. **Read-only scope** — No wallet signing, no CLOB. Trading tools need new API integration and likely auth.

---

## Suggested Evolution Path

```
src/polymarket_mcp/
├── server.py              # FastMCP init + tool registration only
├── config.py
├── clients/
│   ├── gamma.py
│   └── data.py
├── tools/
│   ├── discovery.py
│   ├── portfolio.py
│   └── trading.py
├── formatters/
│   └── ...
└── utils/
    └── helpers.py
```

This aligns with the separation-of-concerns goal without changing the fundamental MCP adapter pattern.
