from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict, Field

class BootstrapRequest(BaseModel):
    tenant_name: str
    admin_name: str
    admin_email: EmailStr
    password: str = Field(min_length=6)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UnitCreate(BaseModel):
    name: str
    resident_name: Optional[str] = None
    resident_email: Optional[EmailStr] = None

class UnitResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    resident_name: Optional[str] = None
    resident_email: Optional[EmailStr] = None
    created_at: datetime

class InviteCreate(BaseModel):
    unit_id: int
    email: EmailStr

class InviteAccept(BaseModel):
    token: str
    full_name: str
    password: str = Field(min_length=6)

class ExpenseCreate(BaseModel):
    title: str
    category: str
    total_amount: Decimal
    due_date: datetime
    notes: Optional[str] = None

class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    category: str
    total_amount: Decimal
    due_date: datetime
    notes: Optional[str] = None
    created_at: datetime

class PaymentCreate(BaseModel):
    unit_id: int
    amount: Decimal
    description: Optional[str] = None
    paid_at: datetime

class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    unit_id: int
    amount: Decimal
    description: Optional[str] = None
    paid_at: datetime
    created_at: datetime
