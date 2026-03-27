from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import require_admin, get_current_user
from ..models import Payment, Unit, User
from ..schemas import PaymentCreate, PaymentResponse

router = APIRouter(prefix="/api/payments", tags=["payments"])

@router.get("")
def list_payments(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Payment).filter(Payment.tenant_id == current_user.tenant_id)
    if not current_user.is_admin:
        query = query.filter(Payment.unit_id == current_user.unit_id)
    rows = query.order_by(Payment.paid_at.desc()).all()
    return [PaymentResponse.model_validate(row) for row in rows]

@router.post("", response_model=PaymentResponse)
def create_payment(payload: PaymentCreate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    unit = db.query(Unit).filter(Unit.id == payload.unit_id, Unit.tenant_id == current_user.tenant_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    payment = Payment(tenant_id=current_user.tenant_id, unit_id=payload.unit_id, amount=payload.amount, description=payload.description, paid_at=payload.paid_at, recorded_by=current_user.id)
    db.add(payment); db.commit(); db.refresh(payment)
    return payment
