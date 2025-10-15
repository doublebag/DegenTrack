from fastapi import APIRouter
from services.coingecko_service import get_top_movers_and_losers
router = APIRouter()
@router.get("/movers_losers")
async def movers_losers():
    movers, losers = await get_top_movers_and_losers()
    return {"movers": movers, "losers": losers}
