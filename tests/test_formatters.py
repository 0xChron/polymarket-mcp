from polymarket_mcp.utils.formatters import (
    format_leaderboard,
    format_market_holders,
    format_trending_markets,
)
from polymarket_mcp.utils.helpers import parse_market_slug


def test_parse_market_slug_from_link() -> None:
    assert parse_market_slug(market_link="https://polymarket.com/event/will-btc-hit-100k/") == "will-btc-hit-100k"


def test_parse_market_slug_prefers_explicit_slug() -> None:
    assert parse_market_slug(slug="my-market", market_link="https://polymarket.com/event/other") == "my-market"


def test_format_trending_markets() -> None:
    result = format_trending_markets([
        {
            "title": "Bitcoin hits 100k?",
            "slug": "btc-100k",
            "volume24hr": 50000,
            "volume": 1000000,
            "liquidity": 25000,
            "endDate": "2026-12-31",
            "active": True,
        }
    ])
    assert "# Trending Markets" in result
    assert "Bitcoin hits 100k?" in result
    assert "btc-100k" in result
    assert "$50000" in result


def test_format_trending_markets_empty() -> None:
    assert format_trending_markets([]) == "No trending markets found."


def test_format_leaderboard() -> None:
    result = format_leaderboard([
        {
            "rank": "1",
            "userName": "trader1",
            "proxyWallet": "0xabc",
            "pnl": 1000.5,
            "vol": 50000,
            "xUsername": "trader",
            "verifiedBadge": True,
        }
    ])
    assert "# Trader Leaderboard" in result
    assert "#1 trader1" in result
    assert "0xabc" in result
    assert "@trader" in result


def test_format_market_holders_with_outcome_labels() -> None:
    result = format_market_holders(
        [
            {
                "token": "123",
                "holders": [
                    {
                        "name": "alice",
                        "amount": 100,
                        "proxyWallet": "0xalice",
                        "outcomeIndex": 0,
                    }
                ],
            },
            {
                "token": "456",
                "holders": [
                    {
                        "name": "bob",
                        "amount": 50,
                        "proxyWallet": "0xbob",
                        "outcomeIndex": 1,
                    }
                ],
            },
        ],
        market_title="Will it rain?",
        outcome_labels=["Yes", "No"],
    )
    assert "Will it rain?" in result
    assert "## Yes" in result
    assert "## No" in result
    assert "alice" in result
    assert "bob" in result
