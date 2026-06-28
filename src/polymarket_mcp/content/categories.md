# Polymarket Categories & Tags

## Leaderboard categories (`category` parameter)

Used by `get_leaderboard` and `get_user_performance`:

| Value | Description |
|-------|-------------|
| `OVERALL` | All categories (default) |
| `POLITICS` | Political markets |
| `SPORTS` | Sports markets |
| `ESPORTS` | Esports markets |
| `CRYPTO` | Cryptocurrency markets |
| `CULTURE` | Culture & entertainment |
| `MENTIONS` | Mention markets |
| `WEATHER` | Weather markets |
| `ECONOMICS` | Economics & macro |
| `TECH` | Technology |
| `FINANCE` | Finance |

## Time periods (`time_period` parameter)

Used by `get_leaderboard` and `get_user_performance`:

| Value | Description |
|-------|-------------|
| `DAY` | Last 24 hours |
| `WEEK` | Last 7 days |
| `MONTH` | Last 30 days |
| `ALL` | All-time (default) |

## Event tag slugs (`tag_slug` parameter)

Used by `get_trending_markets` to filter events by topic. Common values:

| tag_slug | Topic |
|----------|-------|
| `politics` | Political events |
| `crypto` | Cryptocurrency |
| `sports` | Sports |
| `pop-culture` | Pop culture |
| `business` | Business & finance |
| `science` | Science |
| `ai` | Artificial intelligence |

Tag slugs are lowercase strings passed to Gamma's events API. If unsure, call `get_trending_markets` without a filter first.

## Leaderboard sort (`order_by` parameter)

| Value | Sorts by |
|-------|----------|
| `PNL` | Profit and loss (default) |
| `VOL` | Trading volume |

## Trending sort (`order_by` on `get_trending_markets`)

| Value | Sorts by |
|-------|----------|
| `volume24hr` | 24-hour volume (default) |
| `volume` | Total volume |
| `liquidity` | Available liquidity |
| `competitive` | Market competitiveness score |
