from decimal import Decimal
from sqlalchemy import func
from sqlalchemy.orm import Session
from .models import ExpenseShare, Payment, Unit

def money(value) -> Decimal:
    return Decimal(value or 0).quantize(Decimal("0.01"))

def get_unit_balance(db: Session, unit: Unit):
    debt = db.query(func.coalesce(func.sum(ExpenseShare.amount), 0)).filter(ExpenseShare.unit_id == unit.id).scalar()
    paid = db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.unit_id == unit.id).scalar()
    debt = money(debt)
    paid = money(paid)
    return {
        "unit_id": unit.id,
        "unit_name": unit.name,
        "resident_name": unit.resident_name,
        "total_debt": debt,
        "total_paid": paid,
        "balance": money(debt - paid),
    }
