from datetime import datetime, timedelta
import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import get_db
from ..deps import require_admin, get_current_user
from ..models import Unit, Invitation, User
from ..schemas import UnitCreate, UnitResponse, InviteCreate
from ..services.email_service import send_email
from ..utils import get_unit_balance

router = APIRouter(prefix="/api/units", tags=["units"])

@router.get("")
def list_units(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    units = db.query(Unit).filter(Unit.tenant_id == current_user.tenant_id).order_by(Unit.id.asc()).all()
    return [get_unit_balance(db, unit) for unit in units]

@router.post("", response_model=UnitResponse)
def create_unit(payload: UnitCreate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    unit = Unit(tenant_id=current_user.tenant_id, name=payload.name, resident_name=payload.resident_name, resident_email=payload.resident_email)
    db.add(unit); db.commit(); db.refresh(unit)
    return unit

@router.post("/invite")
def invite_resident(payload: InviteCreate, current_user: User = Depends(require_admin), db: Session = Depends(get_db)):
    unit = db.query(Unit).filter(Unit.id == payload.unit_id, Unit.tenant_id == current_user.tenant_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already in use")
    token = secrets.token_urlsafe(32)
    invite = Invitation(tenant_id=current_user.tenant_id, unit_id=unit.id, email=payload.email, token=token, expires_at=datetime.utcnow() + timedelta(days=2), invited_by=current_user.id)
    unit.resident_email = payload.email
    db.add(invite); db.commit()
    link = f"/accept-invite?token={token}"
    send_email(payload.email, "Apartman Sistemi Daveti", f"Merhaba,\n\nDavet linkiniz: {link}\n\n48 saat içinde kullanın.")
    return {"message": "Invitation created", "token": token, "link": link}
