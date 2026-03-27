from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Numeric, Text
from sqlalchemy.orm import relationship
from .db import Base

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    users = relationship("User", back_populates="tenant")
    units = relationship("Unit", back_populates="tenant")

class Unit(Base):
    __tablename__ = "units"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String(50), nullable=False)
    resident_name = Column(String(255))
    resident_email = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    tenant = relationship("Tenant", back_populates="units")
    user = relationship("User", back_populates="unit", uselist=False)
    shares = relationship("ExpenseShare", back_populates="unit")
    payments = relationship("Payment", back_populates="unit")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=True, unique=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255))
    is_admin = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    tenant = relationship("Tenant", back_populates="users")
    unit = relationship("Unit", back_populates="user")

class Invitation(Base):
    __tablename__ = "invitations"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)
    email = Column(String(255), nullable=False, index=True)
    token = Column(String(255), nullable=False, unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    accepted_at = Column(DateTime)
    invited_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    total_amount = Column(Numeric(12,2), nullable=False)
    due_date = Column(DateTime, nullable=False)
    notes = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    shares = relationship("ExpenseShare", back_populates="expense")

class ExpenseShare(Base):
    __tablename__ = "expense_shares"
    id = Column(Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey("expenses.id"), nullable=False, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)
    amount = Column(Numeric(12,2), nullable=False)
    expense = relationship("Expense", back_populates="shares")
    unit = relationship("Unit", back_populates="shares")

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False, index=True)
    amount = Column(Numeric(12,2), nullable=False)
    description = Column(String(255))
    paid_at = Column(DateTime, nullable=False)
    recorded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    unit = relationship("Unit", back_populates="payments")
