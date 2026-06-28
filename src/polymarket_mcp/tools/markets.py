import json

from polymarket_mcp.config import READ_ONLY_ANNOTATIONS, data_url, gamma_url
from polymarket_mcp.server import mcp
from polymarket_mcp.types import TrendingOrderBy
from polymarket_mcp.utils.formatters import (
    format_market_details,
    format_market_holders,
    format_search_markets,
    format_trending_markets,
)
from polymarket_mcp.utils.helpers import err, get, parse_market_slug, text


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
async def search_markets(
    query: str,
    limit: int = 5,
    active_only: bool = True,
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


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
async def get_market_details(
    slug: str | None = None,
    market_link: str | None = None,
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


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
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


@mcp.tool(annotations=READ_ONLY_ANNOTATIONS)
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
