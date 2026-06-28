import pytest

from polymarket_mcp.server import (
    READ_ONLY_ANNOTATIONS,
    SERVER_INSTRUCTIONS,
    mcp,
)

EXPECTED_TOOLS = frozenset({
    "get_user_positions",
    "search_markets",
    "get_market_details",
    "get_user_performance",
    "get_trending_markets",
    "get_leaderboard",
    "get_market_holders",
})


@pytest.mark.asyncio
async def test_list_tools_returns_all_seven() -> None:
    tools = await mcp.list_tools()
    names = {tool.name for tool in tools}
    assert names == EXPECTED_TOOLS


@pytest.mark.asyncio
async def test_all_tools_have_read_only_annotations() -> None:
    tools = await mcp.list_tools()
    for tool in tools:
        assert tool.annotations is not None, f"{tool.name} missing annotations"
        assert tool.annotations.readOnlyHint is True, tool.name
        assert tool.annotations.destructiveHint is False, tool.name
        assert tool.annotations.idempotentHint is True, tool.name
        assert tool.annotations.openWorldHint is True, tool.name


def test_server_instructions_are_set() -> None:
    assert mcp.instructions == SERVER_INSTRUCTIONS
    assert "read-only" in mcp.instructions.lower()
    assert "search_markets" in mcp.instructions
    assert "get_market_details" in mcp.instructions


def test_server_website_url_is_set() -> None:
    assert mcp.website_url == "https://github.com/0xChron/polymarket-mcp"


def test_read_only_annotations_constant() -> None:
    assert READ_ONLY_ANNOTATIONS.readOnlyHint is True
    assert READ_ONLY_ANNOTATIONS.destructiveHint is False
