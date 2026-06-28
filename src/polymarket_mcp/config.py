from mcp.types import ToolAnnotations
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    gamma_url: str = "https://gamma-api.polymarket.com"
    data_url: str = "https://data-api.polymarket.com"
    default_timeout: int = 15


_settings = Settings()
gamma_url = _settings.gamma_url
data_url = _settings.data_url

READ_ONLY_ANNOTATIONS = ToolAnnotations(
    readOnlyHint=True,
    destructiveHint=False,
    idempotentHint=True,
    openWorldHint=True,
)

SERVER_INSTRUCTIONS = """\
Read-only Polymarket prediction market data (Gamma + Data APIs). This server cannot \
place trades, sign transactions, or access private wallets.

Vocabulary:
- Event: a group of related markets (e.g. an election race).
- Market: a single Yes/No question inside an event; identified by slug or URL.
- conditionId: on-chain market identifier; use get_market_details to obtain it.
- Wallet addresses are 0x-prefixed Polygon addresses.

Tool chaining:
1. search_markets or get_trending_markets to discover markets.
2. get_market_details for full context (prices, volume, conditionId).
3. get_market_holders for top holders per outcome.
4. get_leaderboard for top traders; get_user_performance for one wallet.
5. get_user_positions for a wallet's open positions.

Category values: OVERALL, POLITICS, SPORTS, ESPORTS, CRYPTO, CULTURE, MENTIONS, \
WEATHER, ECONOMICS, TECH, FINANCE. Time periods: DAY, WEEK, MONTH, ALL."""
