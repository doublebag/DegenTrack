from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from database import get_session
from models import User
from auth.jwt import create_access_token, verify_password, get_password_hash
import os

auth_router = APIRouter()
templates = Jinja2Templates(directory="templates")

@auth_router.get("/signup", response_class=HTMLResponse)
async def signup_get(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@auth_router.post("/signup")
async def signup_post(request: Request, email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    existing = session.exec(select(User).where(User.email == email)).first()
    if existing:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Email already registered."})
    hashed = get_password_hash(password)
    user = User(email=email, hashed_password=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse(url=f"/dashboard?token={token}", status_code=status.HTTP_302_FOUND)
    return response

@auth_router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@auth_router.post("/login")
async def login_post(request: Request, email: str = Form(...), password: str = Form(...), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials."})
    token = create_access_token({"sub": str(user.id)})
    response = RedirectResponse(url=f"/dashboard?token={token}", status_code=status.HTTP_302_FOUND)
    return response
