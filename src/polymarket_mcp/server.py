import asyncio
import json
from typing import Literal

from mcp.server.fastmcp import FastMCP

from polymarket_mcp.config import Settings
from polymarket_mcp.utils.helpers import err, get, parse_market_slug, text
from polymarket_mcp.utils.formatters import (
    format_user_positions,
    format_search_markets,
    format_market_details,
    format_user_performance,
    format_trending_markets,
    format_leaderboard,
    format_market_holders,
)

data_url = Settings().data_url
gamma_url = Settings().gamma_url

Category = Literal[
    "OVERALL", "POLITICS", "SPORTS", "ESPORTS", "CRYPTO",
    "CULTURE", "MENTIONS", "WEATHER",
    "ECONOMICS", "TECH", "FINANCE"
]
TimePeriod = Literal["DAY", "WEEK", "MONTH", "ALL"]
LeaderboardOrderBy = Literal["PNL", "VOL"]
TrendingOrderBy = Literal["volume24hr", "volume", "liquidity", "competitive"]

mcp = FastMCP("polymarket-mcp")

@mcp.tool()
async def get_user_positions(
    user_address: str,
    limit: int = 10,
    offset: int = 0
):
    """
    Get current positions for a Polymarket wallet address.
    Returns each position with: current price, position size,
    average entry price, current value, and the market it belongs to.
    """

    params = {
        "user": user_address,
        "limit": limit,
        "offset": offset,
    }

    data = await get(f"{data_url}/positions", params=params)
    return text(format_user_positions(data))

@mcp.tool()
async def search_markets(
    query: str,
    limit: int = 5,
    active_only: bool = True
):
    """
    Search Polymarket markets by title or description.
    Returns matching markets with: current price, liquidity, volume,
    end date, and active status.
    """

    params = {
        "q": query,
        "limit_per_type": limit,
        "events_status": "active" if active_only else None,
    }

    data = await get(f"{gamma_url}/public-search", params=params)
    return text(format_search_markets(data))

@mcp.tool()
async def get_market_details(
    slug: str | None = None,
    market_link: str | None = None
):
    """
    Get full details for a single market — outcomes, prices, volume,
    liquidity, resolution source, token IDs, and trading parameters.
    A 'market' is an individual Yes/No question inside an event.
    """
    resolved_slug = parse_market_slug(slug=slug, market_link=market_link)
    if not resolved_slug:
        return err("provide a slug or market link")

    data = await get(f"{gamma_url}/markets/slug/{resolved_slug}")
    return text(format_market_details(data))

@mcp.tool()
async def get_user_performance(
    user_address: str,
    category: Category = "OVERALL",
    time_period: TimePeriod = "ALL"
):
    """
    Get a user's trading performance summary: total positions value, volume,
    P&L across all positions, and their rank on the Polymarket leaderboard.
    Combines /value (portfolio worth) and /v1/leaderboard (rank + PnL stats).
    """

    portfolio_params = {
        "user": user_address
    }

    rank_params = {
        "user": user_address,
        "category": category,
        "timePeriod": time_period,
        "orderBy": "PNL"
    }

    portfolio_task = get(
        f"{data_url}/value",
        params=portfolio_params
    )

    rank_task = get(
        f"{data_url}/v1/leaderboard",
        params=rank_params
    )

    portfolio_data, rank_data = await asyncio.gather(portfolio_task, rank_task, return_exceptions=True)

    if isinstance(portfolio_data, Exception):
        return err(str(portfolio_data))

    if isinstance(rank_data, Exception):
        return err(str(rank_data))

    return text(format_user_performance(portfolio_data, rank_data))

@mcp.tool()
async def get_trending_markets(
    limit: int = 10,
    tag_slug: str | None = None,
    featured_only: bool = False,
    order_by: TrendingOrderBy = "volume24hr",
):
    """
    Get trending Polymarket events ranked by trading activity.
    Returns active events with: slug, 24h volume, total volume, liquidity,
    end date, and active status. Use tag_slug to filter by category
    (e.g. politics, crypto, sports).
    """

    params = {
        "active": True,
        "closed": False,
        "order": order_by,
        "ascending": False,
        "limit": limit,
        "tag_slug": tag_slug,
        "featured": True if featured_only else None,
    }

    data = await get(f"{gamma_url}/events", params=params)
    return text(format_trending_markets(data))

@mcp.tool()
async def get_leaderboard(
    category: Category = "OVERALL",
    time_period: TimePeriod = "ALL",
    order_by: LeaderboardOrderBy = "PNL",
    limit: int = 25,
    offset: int = 0,
):
    """
    Get top Polymarket traders ranked by P&L or volume.
    Returns rank, username, wallet address, P&L, and trading volume.
    Distinct from get_user_performance, which looks up a single wallet.
    """

    params = {
        "category": category,
        "timePeriod": time_period,
        "orderBy": order_by,
        "limit": limit,
        "offset": offset,
    }

    data = await get(f"{data_url}/v1/leaderboard", params=params)
    return text(format_leaderboard(data))

@mcp.tool()
async def get_market_holders(
    condition_id: str | None = None,
    slug: str | None = None,
    market_link: str | None = None,
    limit: int = 20,
):
    """
    Get the top holders for a Polymarket market, grouped by outcome (Yes/No).
    Provide a condition_id, slug, or Polymarket market URL.
    Use get_market_details to find the condition_id for a market.
    """

    market_title: str | None = None
    outcome_labels: list[str] | None = None

    if not condition_id:
        resolved_slug = parse_market_slug(slug=slug, market_link=market_link)
        if not resolved_slug:
            return err("provide a condition_id, slug, or market link")

        market = await get(f"{gamma_url}/markets/slug/{resolved_slug}")
        condition_id = market.get("conditionId")
        market_title = market.get("question")
        raw_outcomes = market.get("outcomes")
        if isinstance(raw_outcomes, str):
            try:
                outcome_labels = json.loads(raw_outcomes)
            except json.JSONDecodeError:
                outcome_labels = None
        elif isinstance(raw_outcomes, list):
            outcome_labels = raw_outcomes

        if not condition_id:
            return err("could not resolve condition_id for this market")

    params = {
        "market": condition_id,
        "limit": min(limit, 20),
    }

    data = await get(f"{data_url}/holders", params=params)
    return text(format_market_holders(data, market_title=market_title, outcome_labels=outcome_labels))


def main() -> None:
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
