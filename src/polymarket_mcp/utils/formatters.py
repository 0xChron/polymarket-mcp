def format_user_positions(positions: list[dict]) -> str:
    if not positions:
        return "No positions found for this user."
    
    lines = ["# User Positions\n"]

    for pos in positions:
        lines.append(f"## {pos.get('title')}")
        lines.append(f"Outcome: {pos.get('outcome')}")
        lines.append(f"Current Price: {pos.get('curPrice')}")
        lines.append(f"Position Size: {pos.get('size')}")
        lines.append(f"Average Entry Price: {pos.get('avgPrice')}")
        lines.append(f"Current Value: {pos.get('currentValue')}")
        lines.append(f"Market End Date: {pos.get('endDate')}")

    return "\n".join(lines)


def format_search_markets(markets: dict) -> str:
    if not markets:
        return "No markets found matching the search query."
    
    lines = ["# Search Results\n"]

    for market in markets.get("events", []):
        if not isinstance(market, dict):
            continue

        lines.append(f"## {market.get('title')}")
        lines.append(f"Description: {market.get('description')}")
        lines.append(f"Current Price: {market.get('curPrice')}")
        lines.append(f"Market Liquidity: {market.get('liquidity')}")
        lines.append(f"Market Volume: {market.get('volume')}")
        lines.append(f"End Date: {market.get('endDate')}")
        lines.append(f"Active: {market.get('active')}")

    return "\n".join(lines)


def format_market_details(market: dict) -> str:
    if not market:
        return "Market not found."
    
    lines = [f"# {market.get('question')}\n"]
    lines.append(f"Description: {market.get('description')}")
    lines.append(f"Outcomes: {market.get('outcomes')}")
    lines.append(f"Current Prices: {market.get('outcomePrices')}")
    lines.append(f"Liquidity: ${market.get('liquidity')}")
    lines.append(f"Volume: ${market.get('volume')}")
    lines.append(f"Start Date: {market.get('startDate')}")
    lines.append(f"End Date: {market.get('endDate')}")
    lines.append(f"Active: {market.get('active')}")
    lines.append(f"Closed: {market.get('closed')}")
    lines.append(f"Condition ID: {market.get('conditionId')}")
    lines.append(f"Slug: {market.get('slug')}")

    return "\n".join(lines)


def format_user_performance(portfolio: list[dict], leaderboard: list[dict]) -> str:
    if not portfolio or not leaderboard:
        return "Performance data not available."
    
    lines = ["# User Performance\n"]
    lines.append(f"Username: {leaderboard[0].get('userName')}")
    lines.append(f"Rank: {leaderboard[0].get('rank')}")
    lines.append(f"Volume: {leaderboard[0].get('vol')}")
    lines.append(f"PNL: {leaderboard[0].get('pnl')}")
    lines.append(f"Total Positions Value: {portfolio[0].get('value')}")

    return "\n".join(lines)