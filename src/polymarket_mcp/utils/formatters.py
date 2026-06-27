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


def format_trending_markets(events: list[dict]) -> str:
    if not events:
        return "No trending markets found."

    lines = ["# Trending Markets\n"]

    for event in events:
        if not isinstance(event, dict):
            continue

        lines.append(f"## {event.get('title')}")
        lines.append(f"Slug: {event.get('slug')}")
        lines.append(f"24h Volume: ${event.get('volume24hr')}")
        lines.append(f"Total Volume: ${event.get('volume')}")
        lines.append(f"Liquidity: ${event.get('liquidity')}")
        lines.append(f"End Date: {event.get('endDate')}")
        lines.append(f"Active: {event.get('active')}")

    return "\n".join(lines)


def format_leaderboard(entries: list[dict]) -> str:
    if not entries:
        return "No leaderboard entries found."

    lines = ["# Trader Leaderboard\n"]

    for entry in entries:
        if not isinstance(entry, dict):
            continue

        lines.append(f"## #{entry.get('rank')} {entry.get('userName')}")
        lines.append(f"Wallet: {entry.get('proxyWallet')}")
        lines.append(f"PNL: ${entry.get('pnl')}")
        lines.append(f"Volume: ${entry.get('vol')}")
        if entry.get("xUsername"):
            lines.append(f"X: @{entry.get('xUsername')}")
        if entry.get("verifiedBadge"):
            lines.append("Verified: true")

    return "\n".join(lines)


def format_market_holders(
    data: list[dict],
    market_title: str | None = None,
    outcome_labels: list[str] | None = None,
) -> str:
    if not data:
        return "No holder data found for this market."

    header = f"# Top Holders — {market_title}\n" if market_title else "# Top Holders\n"
    lines = [header]

    for group in data:
        if not isinstance(group, dict):
            continue

        holders = group.get("holders", [])
        if not holders:
            continue

        outcome_index = holders[0].get("outcomeIndex", 0)
        if outcome_labels and 0 <= outcome_index < len(outcome_labels):
            label = outcome_labels[outcome_index]
        else:
            label = f"Outcome {outcome_index}"

        lines.append(f"## {label}")

        for holder in holders:
            name = holder.get("name") or holder.get("pseudonym") or holder.get("proxyWallet")
            lines.append(f"- {name}: {holder.get('amount')} shares")
            lines.append(f"  Wallet: {holder.get('proxyWallet')}")

    if len(lines) == 1:
        return "No holder data found for this market."

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