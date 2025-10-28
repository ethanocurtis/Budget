from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from ...db.session import SessionLocal
from ...db import models
from ...core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from ...schemas.auth import RegisterRequest, LoginRequest, Token, RefreshRequest
from ...schemas.common import Msg
from ...utils.deps import get_db
from ...services.audit import log as audit_log

router = APIRouter()

@router.post("/register", response_model=Msg)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = models.User(email=data.email, password_hash=hash_password(data.password))
    db.add(user); db.commit()
    audit_log(db, user.id, "register", f"user {data.email} registered")
    return {"msg": "registered"}

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # TOTP optional: allow login without for now; pluggable later
    access = create_access_token(sub=user.email)
    refresh = create_refresh_token(sub=user.email)
    audit_log(db, user.id, "login", "ok")
    return Token(access_token=access, refresh_token=refresh)

@router.post("/refresh", response_model=Token)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    try:
        payload = decode_token(data.refresh_token)
        if payload.get("type") != "refresh":
            raise Exception("wrong token")
        sub = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    # Make sure user still exists
    user = db.query(models.User).filter(models.User.email == sub).first()
    if not user:
        raise HTTPException(status_code=401, detail="user not found")
    return Token(access_token=create_access_token(sub=sub), refresh_token=create_refresh_token(sub=sub))
