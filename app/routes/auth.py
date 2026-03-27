from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from ..models import Tenant, User, Invitation, Unit
from ..schemas import BootstrapRequest, LoginRequest, TokenResponse, InviteAccept
from ..auth import hash_password, verify_password, create_access_token
from ..deps import get_current_user

router = APIRouter(prefix="/api", tags=["auth"])

@router.post("/bootstrap")
def bootstrap(payload: BootstrapRequest, db: Session = Depends(get_db)):
    if db.query(User).count() > 0:
        raise HTTPException(status_code=400, detail="Bootstrap already completed")
    tenant = Tenant(name=payload.tenant_name)
    db.add(tenant); db.flush()
    admin = User(
        tenant_id=tenant.id,
        email=payload.admin_email,
        full_name=payload.admin_name,
        password_hash=hash_password(payload.password),
        is_admin=True,
    )
    db.add(admin); db.commit()
    token = create_access_token({"sub": str(admin.id), "tenant_id": admin.tenant_id, "is_admin": True})
    return {"access_token": token, "token_type": "bearer", "user": {"id": admin.id, "email": admin.email, "full_name": admin.full_name, "tenant_id": admin.tenant_id, "is_admin": True}}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email, User.is_active == True).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token({"sub": str(user.id), "tenant_id": user.tenant_id, "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "full_name": user.full_name, "tenant_id": user.tenant_id, "unit_id": user.unit_id, "is_admin": user.is_admin}}

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "full_name": current_user.full_name, "tenant_id": current_user.tenant_id, "unit_id": current_user.unit_id, "is_admin": current_user.is_admin}

@router.post("/invites/accept")
def accept_invite(payload: InviteAccept, db: Session = Depends(get_db)):
    invite = db.query(Invitation).filter(Invitation.token == payload.token).first()
    if not invite:
        raise HTTPException(status_code=404, detail="Invitation not found")
    if invite.accepted_at:
        raise HTTPException(status_code=400, detail="Invitation already used")
    if invite.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invitation expired")
    if db.query(User).filter(User.email == invite.email).first():
        raise HTTPException(status_code=400, detail="User already exists")
    unit = db.query(Unit).filter(Unit.id == invite.unit_id, Unit.tenant_id == invite.tenant_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    user = User(tenant_id=invite.tenant_id, unit_id=invite.unit_id, email=invite.email, full_name=payload.full_name, password_hash=hash_password(payload.password), is_admin=False)
    unit.resident_email = invite.email
    unit.resident_name = payload.full_name
    invite.accepted_at = datetime.utcnow()
    db.add(user); db.commit()
    token = create_access_token({"sub": str(user.id), "tenant_id": user.tenant_id, "is_admin": False})
    return {"access_token": token, "token_type": "bearer", "user": {"id": user.id, "email": user.email, "full_name": user.full_name, "tenant_id": user.tenant_id, "unit_id": user.unit_id, "is_admin": user.is_admin}}
