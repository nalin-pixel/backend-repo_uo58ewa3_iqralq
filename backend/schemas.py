from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    email: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Account(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    type: str = Field(description="e.g., checking, savings")
    balance: float = 0.0
    currency: str = "USD"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("balance", pre=True)
    def ensure_float(cls, v):
        return float(v)


class Card(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    brand: str = "Visa"
    last4: str
    cardholder: str
    status: str = Field(default="active", description="active | locked | inactive")
    color: Optional[str] = "#7c3aed"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Transaction(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    account_id: Optional[str] = None
    amount: float
    currency: str = "USD"
    description: str
    category: Optional[str] = None
    direction: str = Field(description="debit or credit")
    occurred_at: datetime = Field(default_factory=datetime.utcnow)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @validator("amount", pre=True)
    def ensure_amount_float(cls, v):
        return float(v)
