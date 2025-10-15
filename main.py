from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from database import create_db_and_tables, get_session
from auth.auth_routes import auth_router
from routes_watchlist import router as watchlist_router
from routes_alerts import router as alerts_router
from routes_news import router as news_router
from services.coingecko_service import get_top_movers_and_losers

app = FastAPI(title="DegenTracks")

# Static & templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(watchlist_router, prefix="/api/watchlist", tags=["watchlist"])
app.include_router(alerts_router, prefix="/api/alerts", tags=["alerts"])
app.include_router(news_router, prefix="/api/news", tags=["news"])

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    movers, losers = await get_top_movers_and_losers()
    return templates.TemplateResponse("index.html", {"request": request, "movers": movers, "losers": losers})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # In a real app, verify JWT / session and fetch user watchlist
    return templates.TemplateResponse("dashboard.html", {"request": request})
