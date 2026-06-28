from polymarket_mcp.server import mcp


@mcp.prompt(
    title="Research Market",
    description="Analyze a Polymarket market: details, top holders, and a research summary.",
)
def research_market(slug: str = "", market_link: str = "") -> list:
    target = slug or market_link or "(not specified)"
    return [
        {
            "role": "user",
            "content": (
                f"Research the Polymarket market: {target}\n\n"
                "Follow this workflow using available tools:\n"
                "1. Call get_market_details with the slug or market_link.\n"
                "2. Call get_market_holders for the same market.\n"
                "3. Summarize: question, current prices, volume/liquidity, "
                "notable holders per outcome, and key takeaways."
            ),
        }
    ]


@mcp.prompt(
    title="Compare Traders",
    description="Compare two Polymarket wallets on performance and open positions.",
)
def compare_traders(address_a: str, address_b: str) -> list:
    return [
        {
            "role": "user",
            "content": (
                f"Compare these two Polymarket traders:\n"
                f"- Wallet A: {address_a}\n"
                f"- Wallet B: {address_b}\n\n"
                "For each wallet, call get_user_performance and get_user_positions. "
                "Then compare: portfolio value, P&L, leaderboard rank, volume, "
                "and open position themes. Highlight the biggest differences."
            ),
        }
    ]


@mcp.prompt(
    title="Scan Trending",
    description="Fetch trending markets and brief on the most active ones.",
)
def scan_trending(tag_slug: str = "", limit: int = 5) -> list:
    filter_note = f' filtered by tag "{tag_slug}"' if tag_slug else ""
    return [
        {
            "role": "user",
            "content": (
                f"Scan trending Polymarket events{filter_note}.\n\n"
                f"1. Call get_trending_markets(limit={limit}"
                + (f', tag_slug="{tag_slug}"' if tag_slug else "")
                + ").\n"
                "2. For the top results, briefly summarize each: title, slug, "
                "24h volume, and why it may be interesting.\n"
                "3. If one stands out, offer to deep-dive with get_market_details."
            ),
        }
    ]
