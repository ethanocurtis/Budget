from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...utils.deps import get_db, get_current_user
from ...db import models
from ...schemas.goals import GoalCreate, GoalOut

router = APIRouter()

@router.post("", response_model=GoalOut)
def create_goal(data: GoalCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    g = models.Goal(user_id=user.id, **data.model_dump())
    db.add(g); db.commit(); db.refresh(g)
    return g

@router.get("", response_model=list[GoalOut])
def list_goals(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(models.Goal).filter(models.Goal.user_id == user.id).all()
