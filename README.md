# Polymarket MCP

MCP server that exposes read-only Polymarket prediction market data to AI agents. Tools wrap Polymarket's public **Gamma** (market discovery) and **Data** (positions, portfolio, leaderboard) APIs. There is no CLOB integration — this server cannot place trades or read order books.

<!-- mcp-name: io.github.0xChron/polymarket-mcp -->

## Tools

| Tool | Description |
|------|-------------|
| `search_markets` | Search markets by title or description |
| `get_market_details` | Full details for a single market (by slug or Polymarket URL) |
| `get_trending_markets` | Trending events ranked by volume, liquidity, or competitiveness |
| `get_market_holders` | Top holders per outcome for a market (by condition ID, slug, or URL) |
| `get_leaderboard` | Top traders ranked by P&L or volume |
| `get_user_positions` | Open positions for a wallet address |
| `get_user_performance` | Portfolio value, P&L, volume, and leaderboard rank for one wallet |

All tools return markdown formatted for agent consumption. No API keys or wallet signing are required.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (recommended) or Docker
- [Node.js](https://nodejs.org/) (optional, only for MCP Inspector)

## Quick start

This server uses **streamable HTTP** at `http://127.0.0.1:8000/mcp`. Start the server first, then connect your MCP client to that URL.

```bash
git clone https://github.com/0xChron/polymarket-mcp.git
cd polymarket-mcp
uv sync
uv run polymarket-mcp
```

On Windows, use the same commands in **PowerShell**, **Command Prompt**, or **Git Bash**. Leave the terminal open while your MCP client is connected.

### Docker

Works the same on all platforms if Docker Desktop is installed:

```bash
git clone https://github.com/0xChron/polymarket-mcp.git
cd polymarket-mcp
docker build -t polymarket-mcp .
docker run --rm -p 8000:8000 -e FASTMCP_HOST=0.0.0.0 polymarket-mcp
```

`FASTMCP_HOST=0.0.0.0` lets the server accept connections from outside the container.

### Verify the server

Open [MCP Inspector](https://github.com/modelcontextprotocol/inspector) in another terminal:

```bash
npx -y @modelcontextprotocol/inspector
```

Connect to `http://localhost:8000/mcp` using the **Streamable HTTP** transport.

## Connect from an MCP client

This server uses the **streamable-http** transport (not stdio). **Start the server first** (see [Quick start](#quick-start)), then add the config below to your MCP client.

### Claude Desktop

Go to **Claude → Settings → Developer → Edit Config** to open `claude_desktop_config.json`, then include the following:

```json
{
  "mcpServers": {
    "polymarket": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

If you already have other MCP servers configured, add the `"polymarket"` entry inside your existing `mcpServers` object instead of replacing the whole file.

Config file location if you prefer to edit it manually:

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

Save the file and **fully quit and restart Claude Desktop**. The server must be running in a terminal before you start a new chat.

### Cursor

Go to **Settings → Tools & MCP → New MCP Server** to open `~/.cursor/mcp.json` (Windows: `%USERPROFILE%\.cursor\mcp.json`), then add the same `polymarket` entry:

```json
{
  "mcpServers": {
    "polymarket": {
      "url": "http://localhost:8000/mcp"
    }
  }
}
```

Restart Cursor after saving.

### Example agent prompts

Once connected, an agent can call tools naturally:

- "Search Polymarket for active markets about Bitcoin ETFs"
- "What are the trending markets right now?"
- "Who are the top holders of the Trump election market?"
- "Show the all-time P&L leaderboard for crypto traders"
- "Get details for https://polymarket.com/event/will-bitcoin-hit-100k"
- "Show open positions for wallet `0x…`"
- "What is the all-time P&L and leaderboard rank for `0x…`?"

## Configuration

Optional environment variables override API endpoints and server settings.

**macOS / Linux / Git Bash**

```bash
export FASTMCP_HOST=0.0.0.0
export FASTMCP_PORT=8000
uv run polymarket-mcp
```

**Windows (PowerShell)**

```powershell
$env:FASTMCP_HOST = "0.0.0.0"
$env:FASTMCP_PORT = "8000"
uv run polymarket-mcp
```

| Variable | Default | Description |
|----------|---------|-------------|
| `GAMMA_URL` | `https://gamma-api.polymarket.com` | Gamma API base URL |
| `DATA_URL` | `https://data-api.polymarket.com` | Data API base URL |
| `DEFAULT_TIMEOUT` | `15` | HTTP request timeout (seconds) |
| `FASTMCP_HOST` | `127.0.0.1` | Bind address (`0.0.0.0` for Docker) |
| `FASTMCP_PORT` | `8000` | Listen port |

## Development

```bash
uv run polymarket-mcp          # Start the server
uv run pytest                  # Run tests
npx -y @modelcontextprotocol/inspector   # Open MCP Inspector
docker build -t polymarket-mcp .         # Build Docker image
```

On macOS/Linux, `make run`, `make test`, and similar shortcuts in the [Makefile](Makefile) wrap the same commands.

See [`docs/PROJECT_KNOWLEDGE_BASE.md`](docs/PROJECT_KNOWLEDGE_BASE.md) for architecture, conventions, and how to add new tools.

## License

MIT — see [LICENSE](LICENSE).
