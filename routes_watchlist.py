from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select
from database import get_session
from models import WatchlistItem
from auth.jwt import decode_access_token

router = APIRouter()

class WatchlistCreate(BaseModel):
    coin_id: str
    symbol: str | None = None

def get_user_id(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")
    payload = decode_access_token(authorization)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload.get("sub"))

@router.get("/", response_model=list[WatchlistItem])
def list_watchlist(user_id: int = Depends(get_user_id), session: Session = Depends(get_session)):
    items = session.exec(select(WatchlistItem).where(WatchlistItem.user_id == user_id)).all()
    return items

@router.post("/")
def add_watchlist_item(payload: WatchlistCreate, user_id: int = Depends(get_user_id), session: Session = Depends(get_session)):
    item = WatchlistItem(user_id=user_id, coin_id=payload.coin_id, symbol=payload.symbol)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
