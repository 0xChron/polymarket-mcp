import asyncio

from polymarket_mcp.config import READ_ONLY_ANNOTATIONS, data_url
from polymarket_mcp.server import mcp
from polymarket_mcp.types import Category, LeaderboardOrderBy, TimePeriod
from polymarket_mcp.utils.formatters import (
    format_leaderboard,
    format_user_performance,
    format_user_positions,
)
from polymarket_mcp.utils.helpers import err, get, text


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
async def get_user_positions(
    user_address: str,
    limit: int = 10,
    offset: int = 0,
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


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
async def get_user_performance(
    user_address: str,
    category: Category = "OVERALL",
    time_period: TimePeriod = "ALL",
):
    """
    Get a user's trading performance summary: total positions value, volume,
    P&L across all positions, and their rank on the Polymarket leaderboard.
    Combines /value (portfolio worth) and /v1/leaderboard (rank + PnL stats).
    """

    portfolio_params = {
        "user": user_address,
    }

    rank_params = {
        "user": user_address,
        "category": category,
        "timePeriod": time_period,
        "orderBy": "PNL",
    }

    portfolio_task = get(
        f"{data_url}/value",
        params=portfolio_params,
    )

    rank_task = get(
        f"{data_url}/v1/leaderboard",
        params=rank_params,
    )

    portfolio_data, rank_data = await asyncio.gather(
        portfolio_task, rank_task, return_exceptions=True,
    )

    if isinstance(portfolio_data, Exception):
        return err(str(portfolio_data))

    if isinstance(rank_data, Exception):
        return err(str(rank_data))

    return text(format_user_performance(portfolio_data, rank_data))


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
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
