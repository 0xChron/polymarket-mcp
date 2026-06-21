# Polymarket MCP

MCP server that exposes read-only Polymarket prediction market data to AI agents. Tools wrap Polymarket's public **Gamma** (market discovery) and **Data** (positions, portfolio, leaderboard) APIs. There is no CLOB integration — this server cannot place trades or read order books.

<!-- mcp-name: io.github.0xChron/polymarket-mcp -->

## Tools

| Tool | Description |
|------|-------------|
| `search_markets` | Search markets by title or description |
| `get_market_details` | Full details for a single market (by slug or Polymarket URL) |
| `get_user_positions` | Open positions for a wallet address |
| `get_user_performance` | Portfolio value, P&L, volume, and leaderboard rank |

All tools return markdown formatted for agent consumption. No API keys or wallet signing are required.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or Docker

## Quick start

Clone the repo, install dependencies, and start the server:

```bash
git clone https://github.com/0xChron/polymarket-mcp.git
cd polymarket-mcp
uv sync
make run
```

The server listens on **streamable HTTP** at `http://127.0.0.1:8000/mcp`.

Verify it is running with the [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
make inspector
```

Connect the inspector to `http://localhost:8000/mcp` using the **Streamable HTTP** transport.

## Connect from an MCP client

This server uses the **streamable-http** transport (not stdio). Start the server first, then point your client at the `/mcp` endpoint.

### Cursor

Add to `~/.cursor/mcp.json` (global) or `.cursor/mcp.json` (project-scoped):

```json
{
  "mcpServers": {
    "polymarket": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Restart Cursor (or reload the window) after saving. The server must be running before the client connects.

### Claude Desktop / other HTTP clients

Any MCP client that supports streamable HTTP can connect to the same URL. Refer to your client's documentation for remote server configuration.

### Example agent prompts

Once connected, an agent can call tools naturally:

- "Search Polymarket for active markets about Bitcoin ETFs"
- "Get details for https://polymarket.com/event/will-bitcoin-hit-100k"
- "Show open positions for wallet `0x…`"
- "What is the all-time P&L and leaderboard rank for `0x…`?"

## Docker

Build and run the container:

```bash
make build
docker run --rm -p 8000:8000 -e FASTMCP_HOST=0.0.0.0 polymarket-mcp
```

`FASTMCP_HOST=0.0.0.0` is required so the server accepts connections from outside the container. Then connect your MCP client to `http://localhost:8000/mcp`.

## Configuration

Optional environment variables override API endpoints and server settings:

| Variable | Default | Description |
|----------|---------|-------------|
| `GAMMA_URL` | `https://gamma-api.polymarket.com` | Gamma API base URL |
| `DATA_URL` | `https://data-api.polymarket.com` | Data API base URL |
| `DEFAULT_TIMEOUT` | `15` | HTTP request timeout (seconds) |
| `FASTMCP_HOST` | `127.0.0.1` | Bind address (`0.0.0.0` for Docker) |
| `FASTMCP_PORT` | `8000` | Listen port |

## Development

```bash
make run        # Start the server
make test       # Run tests
make inspector  # Open MCP Inspector
make build      # Build Docker image
```

See [`docs/PROJECT_KNOWLEDGE_BASE.md`](docs/PROJECT_KNOWLEDGE_BASE.md) for architecture, conventions, and how to add new tools.

## License

MIT — see [LICENSE](LICENSE).
