from sqlalchemy.orm import Session
from ..db import models

def log(db: Session, user_id: int, action: str, detail: str | None = None):
    db.add(models.AuditLog(user_id=user_id, action=action, detail=detail))
    db.commit()
