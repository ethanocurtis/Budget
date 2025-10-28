from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...utils.deps import get_db, get_current_user
from ...db import models
from ...schemas.accounts import AccountCreate, AccountOut
from ...services.audit import log as audit_log

router = APIRouter()

@router.post("", response_model=AccountOut)
def create_account(data: AccountCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    acc = models.Account(user_id=user.id, **data.model_dump())
    db.add(acc); db.commit(); db.refresh(acc)
    audit_log(db, user.id, "account.create", f"{acc.name}")
    return acc

@router.get("", response_model=list[AccountOut])
def list_accounts(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Account).filter(models.Account.user_id == user.id).all()
