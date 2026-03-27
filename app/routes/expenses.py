from decimal import Decimal, ROUND_HALF_UP
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import require_admin, get_current_user
from ..models import Expense, ExpenseShare, Unit, User
from ..schemas import ExpenseCreate, ExpenseResponse

router = APIRouter(prefix="/api/expenses", tags=["expenses"])

@router.get("")
def list_expenses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = db.query(Expense).filter(Expense.tenant_id == current_user.tenant_id).order_by(Expense.due_date.desc()).all()
    return [ExpenseResponse.model_validate(item) for item in items]

@router.post("", response_model=ExpenseResponse)
def create_expense(payload: ExpenseCreate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    units = db.query(Unit).filter(Unit.tenant_id == current_user.tenant_id).all()
    if not units:
        raise HTTPException(status_code=400, detail="Create units first")
    expense = Expense(tenant_id=current_user.tenant_id, title=payload.title, category=payload.category, total_amount=payload.total_amount, due_date=payload.due_date, notes=payload.notes, created_by=current_user.id)
    db.add(expense); db.flush()
    total = Decimal(payload.total_amount); count = len(units)
    per_unit = (total / count).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    allocated = Decimal("0.00")
    for idx, unit in enumerate(units, start=1):
        amount = per_unit if idx < count else total - allocated
        allocated += amount
        db.add(ExpenseShare(expense_id=expense.id, unit_id=unit.id, amount=amount))
    db.commit(); db.refresh(expense)
    return expense
