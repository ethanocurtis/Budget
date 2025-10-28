from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...utils.deps import get_db, get_current_user
from ...schemas.users import UserOut

router = APIRouter()

@router.get("/me", response_model=UserOut)
def me(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return user
