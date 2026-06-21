import asyncio
from typing import Literal

from mcp.server.fastmcp import FastMCP

from polymarket_mcp.config import Settings
from polymarket_mcp.utils.helpers import err, get, text
from polymarket_mcp.utils.formatters import (
    format_user_positions,
    format_search_markets,
    format_market_details,
    format_user_performance,
)

data_url = Settings().data_url
gamma_url = Settings().gamma_url

Category = Literal[
    "OVERALL", "POLITICS", "SPORTS", "CRYPTO",
    "CULTURE", "MENTIONS", "WEATHER",
    "ECONOMICS", "TECH", "FINANCE"
]
TimePeriod = Literal["DAY", "WEEK", "MONTH", "ALL"]

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
    if not slug and not market_link:
        return err("provide a slug or market link")
    
    if market_link:
        slug = market_link.rstrip("/").split("/")[-1]

    data = await get(f"{gamma_url}/markets/slug/{slug}") 
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


def main() -> None:
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()