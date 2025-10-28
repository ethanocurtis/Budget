# Seed demo data
from sqlalchemy.orm import Session
from ..db.session import SessionLocal
from ..db import models
from ..core.security import hash_password
from datetime import date
from decimal import Decimal

def run(db: Session):
    if db.query(models.User).filter(models.User.email=="demo@demo.com").first():
        return
    user = models.User(email="demo@demo.com", password_hash=hash_password("demo123"))
    db.add(user); db.commit(); db.refresh(user)

    acc = models.Account(user_id=user.id, name="Checking", type="checking", opening_balance=Decimal("1000.00"))
    db.add(acc); db.commit(); db.refresh(acc)

    g = models.CategoryGroup(user_id=user.id, name="Housing")
    db.add(g); db.commit(); db.refresh(g)

    c = models.Category(user_id=user.id, group_id=g.id, name="Rent", rollover=False)
    db.add(c); db.commit(); db.refresh(c)

    t = models.Transaction(user_id=user.id, account_id=acc.id, date=date.today(), payee="Landlord", memo="October rent", amount=Decimal("-800.00"))
    db.add(t); db.commit(); db.refresh(t)

    s = models.Split(transaction_id=t.id, category_id=c.id, amount=Decimal("-800.00"))
    db.add(s); db.commit()

def main():
    db = SessionLocal()
    try:
        run(db)
        print("Seeded demo data.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
