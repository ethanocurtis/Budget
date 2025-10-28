from .base import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime, Numeric, Text
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    totp_secret = Column(String(32), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False) # checking, savings, credit, cash
    currency = Column(String(3), default="USD")
    opening_balance = Column(Numeric(12,2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

class CategoryGroup(Base):
    __tablename__ = "category_groups"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    name = Column(String(100), nullable=False)

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    group_id = Column(Integer, ForeignKey("category_groups.id"), nullable=True)
    name = Column(String(100), nullable=False)
    rollover = Column(Boolean, default=True)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    date = Column(Date, nullable=False)
    payee = Column(String(200), nullable=True)
    memo = Column(Text, nullable=True)
    amount = Column(Numeric(12,2), nullable=False) # positive=income, negative=expense
    cleared = Column(Boolean, default=False)

class Split(Base):
    __tablename__ = "splits"
    id = Column(Integer, primary_key=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    amount = Column(Numeric(12,2), nullable=False)

class Budget(Base):
    __tablename__ = "budgets"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    month = Column(String(7), index=True, nullable=False)  # YYYY-MM
    planned = Column(Numeric(12,2), default=0)

class Goal(Base):
    __tablename__ = "goals"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    type = Column(String(50), nullable=False)  # target-by-date, monthly-savings, debt-payoff
    target_amount = Column(Numeric(12,2), nullable=False)
    target_date = Column(Date, nullable=True)

class Attachment(Base):
    __tablename__ = "attachments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)
    filename = Column(String(255), nullable=False)
    path = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    action = Column(String(100), nullable=False)
    detail = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
