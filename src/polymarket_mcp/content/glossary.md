# Polymarket Glossary

Terms used across this MCP server and Polymarket APIs.

## Event

A grouped collection of related markets under one topic (e.g. "2024 US Presidential Election"). Events have a slug, volume, liquidity, and end date. Use `get_trending_markets` to browse events.

## Market

A single predictive question inside an event, usually with Yes/No outcomes (e.g. "Will Bitcoin hit $100k by Dec 31?"). Markets are identified by:

- **slug** — URL path segment (e.g. `will-bitcoin-hit-100k`)
- **market link** — full Polymarket URL; the slug is the last path segment
- **conditionId** — on-chain identifier; required for `get_market_holders`

Use `get_market_details` to resolve a slug or URL to full market data including `conditionId`.

## Outcome

A possible result for a market (typically "Yes" or "No"). Each outcome has a price (implied probability) and may map to a **clobTokenId** (used by CLOB pricing tools when available).

## conditionId

The on-chain market identifier on Polygon. Required by `get_market_holders`. Obtain it from `get_market_details` — do not guess or fabricate IDs.

## clobTokenId

Token identifier for a specific outcome on Polymarket's CLOB. Used for order book and live pricing (CLOB tools planned). Listed in `get_market_details` output when available.

## Wallet address

Polygon address in `0x` format. Used by `get_user_positions`, `get_user_performance`, and leaderboard lookups.

## Slug vs event slug

- **Event slug** — identifies an event (`get_trending_markets`)
- **Market slug** — identifies a single market (`get_market_details`, `search_markets`)

When a user shares a Polymarket URL, extract the last path segment as the slug.
