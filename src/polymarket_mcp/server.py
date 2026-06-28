from mcp.server.fastmcp import FastMCP

from polymarket_mcp.config import READ_ONLY_ANNOTATIONS, SERVER_INSTRUCTIONS

mcp = FastMCP(
    "polymarket-mcp",
    instructions=SERVER_INSTRUCTIONS,
    website_url="https://github.com/0xChron/polymarket-mcp",
)

# Register resources, prompts, and tools (import for side effects).
from polymarket_mcp import prompts as _prompts  # noqa: E402, F401
from polymarket_mcp import resources as _resources  # noqa: E402, F401
import polymarket_mcp.tools as _tools  # noqa: E402, F401

__all__ = ["READ_ONLY_ANNOTATIONS", "SERVER_INSTRUCTIONS", "mcp", "main"]


def main() -> None:
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    main()
