from polymarket_mcp.content import load as load_content
from polymarket_mcp.server import mcp


@mcp.resource(
    "polymarket://glossary",
    name="glossary",
    title="Polymarket Glossary",
    description="Definitions for events, markets, slugs, conditionId, and wallet addresses.",
    mime_type="text/markdown",
)
def glossary_resource() -> str:
    return load_content("glossary.md")


@mcp.resource(
    "polymarket://categories",
    name="categories",
    title="Categories & Tags",
    description="Leaderboard categories, time periods, and event tag_slug values.",
    mime_type="text/markdown",
)
def categories_resource() -> str:
    return load_content("categories.md")


@mcp.resource(
    "polymarket://tool-guide",
    name="tool-guide",
    title="Tool Guide",
    description="When to use each tool and common chaining workflows.",
    mime_type="text/markdown",
)
def tool_guide_resource() -> str:
    return load_content("tool-guide.md")
