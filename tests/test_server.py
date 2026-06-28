import pytest

from polymarket_mcp.content import load as load_content
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

EXPECTED_RESOURCES = frozenset({
    "polymarket://glossary",
    "polymarket://categories",
    "polymarket://tool-guide",
})

EXPECTED_PROMPTS = frozenset({
    "research_market",
    "compare_traders",
    "scan_trending",
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


@pytest.mark.asyncio
async def test_list_resources_returns_all_three() -> None:
    resources = await mcp.list_resources()
    uris = {str(resource.uri) for resource in resources}
    assert uris == EXPECTED_RESOURCES


@pytest.mark.asyncio
async def test_read_glossary_resource() -> None:
    contents = await mcp.read_resource("polymarket://glossary")
    assert len(contents) == 1
    assert "# Polymarket Glossary" in contents[0].content
    assert contents[0].mime_type == "text/markdown"


@pytest.mark.asyncio
async def test_list_prompts_returns_all_three() -> None:
    prompts = await mcp.list_prompts()
    names = {prompt.name for prompt in prompts}
    assert names == EXPECTED_PROMPTS


@pytest.mark.asyncio
async def test_get_research_market_prompt() -> None:
    result = await mcp.get_prompt("research_market", {"slug": "will-bitcoin-hit-100k"})
    assert len(result.messages) == 1
    assert result.messages[0].role == "user"
    assert "will-bitcoin-hit-100k" in result.messages[0].content.text
    assert "get_market_details" in result.messages[0].content.text


def test_content_loader_reads_glossary() -> None:
    text = load_content("glossary.md")
    assert "conditionId" in text
