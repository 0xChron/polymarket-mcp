# Polymarket MCP Tool Guide

When to use each tool and how to chain them for common research workflows.

## Tool reference

| Tool | Use when |
|------|----------|
| `search_markets` | User mentions a topic; find markets by keyword |
| `get_trending_markets` | User wants hot/active markets; no specific query |
| `get_market_details` | User has a slug, URL, or needs full market context |
| `get_market_holders` | User asks who holds a position; needs `conditionId` or slug |
| `get_leaderboard` | User wants top traders globally or by category |
| `get_user_performance` | User provides one wallet; wants P&L, rank, portfolio value |
| `get_user_positions` | User wants open positions for a specific wallet |

## Discovery workflows

### Find a market by topic

```
search_markets(query="bitcoin ETF") → get_market_details(slug=...)
```

### Browse what's active now

```
get_trending_markets(limit=10, tag_slug="crypto")
```

## Market research workflow

```
get_market_details(slug or market_link)
  → get_market_holders(slug or condition_id from details)
  → summarize findings for the user
```

`get_market_details` returns prices, volume, liquidity, `conditionId`, and outcome labels. Pass the slug or `conditionId` directly to `get_market_holders`.

## Trader research workflow

### Single wallet

```
get_user_performance(user_address)
  → get_user_positions(user_address)
```

### Compare top traders

```
get_leaderboard(category="CRYPTO", time_period="MONTH", limit=10)
  → get_user_performance for wallets of interest
```

## Input tips

- **Slug from URL:** `https://polymarket.com/event/my-market-slug` → slug is `my-market-slug`
- **Wallet:** must be a `0x`-prefixed Polygon address
- **Holders limit:** API caps at 20 per outcome

## Resources vs tools

- **Resources** (`polymarket://glossary`, etc.) — static reference context; read-only, no API calls
- **Tools** — live data from Polymarket APIs; use for current prices, positions, and rankings
