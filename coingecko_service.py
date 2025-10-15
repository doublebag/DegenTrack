import httpx
BASE = "https://api.coingecko.com/api/v3"

async def get_market_list(per_page=250, vs_currency="usd"):
    url = f"{BASE}/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": 1,
        "price_change_percentage": "24h"
    }
    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        return r.json()

async def get_top_movers_and_losers(limit=10):
    data = await get_market_list()
    cleaned = [d for d in data if d.get("price_change_percentage_24h") is not None]
    sorted_gain = sorted(cleaned, key=lambda x: x["price_change_percentage_24h"], reverse=True)
    sorted_loss = sorted(cleaned, key=lambda x: x["price_change_percentage_24h"])
    movers = [{"id": c["id"], "symbol": c["symbol"].upper(), "name": c["name"], "change": round(c["price_change_percentage_24h"],2), "price": c["current_price"]} for c in sorted_gain[:limit]]
    losers = [{"id": c["id"], "symbol": c["symbol"].upper(), "name": c["name"], "change": round(c["price_change_percentage_24h"],2), "price": c["current_price"]} for c in sorted_loss[:limit]]
    return movers, losers
