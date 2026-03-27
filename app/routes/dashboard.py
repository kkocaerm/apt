from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import get_current_user
from ..models import Expense, Payment, Unit, User
from ..utils import get_unit_balance, money

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("")
def dashboard(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.is_admin:
        total_expenses = money(db.query(func.coalesce(func.sum(Expense.total_amount), 0)).filter(Expense.tenant_id == current_user.tenant_id).scalar())
        total_collected = money(db.query(func.coalesce(func.sum(Payment.amount), 0)).filter(Payment.tenant_id == current_user.tenant_id).scalar())
        return {
            "total_expenses": total_expenses,
            "total_collected": total_collected,
            "total_outstanding": money(total_expenses - total_collected),
            "unit_count": db.query(Unit).filter(Unit.tenant_id == current_user.tenant_id).count(),
            "resident_count": db.query(User).filter(User.tenant_id == current_user.tenant_id, User.is_admin == False).count(),
        }
    unit = db.query(Unit).filter(Unit.id == current_user.unit_id, Unit.tenant_id == current_user.tenant_id).first()
    return get_unit_balance(db, unit)

@router.get("/my-expenses")
def my_expenses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.is_admin:
        return []
    from ..models import ExpenseShare, Expense
    rows = db.query(ExpenseShare, Expense).join(Expense, Expense.id == ExpenseShare.expense_id).filter(ExpenseShare.unit_id == current_user.unit_id).order_by(Expense.due_date.desc()).all()
    return [{"id": expense.id, "title": expense.title, "category": expense.category, "due_date": expense.due_date, "amount": share.amount} for share, expense in rows]
