from typing import Literal

Category = Literal[
    "OVERALL", "POLITICS", "SPORTS", "ESPORTS", "CRYPTO",
    "CULTURE", "MENTIONS", "WEATHER",
    "ECONOMICS", "TECH", "FINANCE",
]
TimePeriod = Literal["DAY", "WEEK", "MONTH", "ALL"]
LeaderboardOrderBy = Literal["PNL", "VOL"]
TrendingOrderBy = Literal["volume24hr", "volume", "liquidity", "competitive"]
