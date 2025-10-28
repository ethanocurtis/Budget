from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...utils.deps import get_db, get_current_user
from ...db import models
from ...schemas.categories import CategoryGroupCreate, CategoryGroupOut, CategoryCreate, CategoryOut

router = APIRouter()

@router.post("/groups", response_model=CategoryGroupOut)
def create_group(data: CategoryGroupCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    g = models.CategoryGroup(user_id=user.id, name=data.name)
    db.add(g); db.commit(); db.refresh(g)
    return g

@router.get("/groups", response_model=list[CategoryGroupOut])
def list_groups(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.CategoryGroup).filter(models.CategoryGroup.user_id == user.id).all()

@router.post("", response_model=CategoryOut)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    c = models.Category(user_id=user.id, **data.model_dump())
    db.add(c); db.commit(); db.refresh(c)
    return c

@router.get("", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Category).filter(models.Category.user_id == user.id).all()
