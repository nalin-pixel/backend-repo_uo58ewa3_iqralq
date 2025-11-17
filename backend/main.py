from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from database import create_document, get_documents
from schemas import User, Account, Card, Transaction

app = FastAPI(title="Fintech Dashboard API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateUser(BaseModel):
    name: str
    email: str


class CreateAccount(BaseModel):
    user_id: str
    type: str
    balance: float = 0.0
    currency: str = "USD"


class CreateCard(BaseModel):
    user_id: str
    brand: str = "Visa"
    last4: str
    cardholder: str
    color: Optional[str] = "#7c3aed"


class CreateTransaction(BaseModel):
    user_id: str
    account_id: Optional[str] = None
    amount: float
    currency: str = "USD"
    description: str
    category: Optional[str] = None
    direction: str
    occurred_at: Optional[datetime] = None


@app.get("/test")
async def test():
    return {"status": "ok", "time": datetime.utcnow().isoformat()}


@app.post("/users", response_model=User)
async def create_user(payload: CreateUser):
    data = payload.dict()
    user = create_document("user", data)
    return User(**user)


@app.get("/users", response_model=List[User])
async def list_users():
    users = get_documents("user")
    return [User(**u) for u in users]


@app.post("/accounts", response_model=Account)
async def create_account(payload: CreateAccount):
    data = payload.dict()
    account = create_document("account", data)
    return Account(**account)


@app.get("/accounts", response_model=List[Account])
async def list_accounts(user_id: Optional[str] = None):
    filt = {"user_id": user_id} if user_id else None
    accounts = get_documents("account", filt)
    return [Account(**a) for a in accounts]


@app.post("/cards", response_model=Card)
async def create_card(payload: CreateCard):
    data = payload.dict()
    card = create_document("card", data)
    return Card(**card)


@app.get("/cards", response_model=List[Card])
async def list_cards(user_id: Optional[str] = None):
    filt = {"user_id": user_id} if user_id else None
    cards = get_documents("card", filt)
    return [Card(**c) for c in cards]


@app.post("/transactions", response_model=Transaction)
async def create_tx(payload: CreateTransaction):
    data = payload.dict()
    if not data.get("occurred_at"):
        data["occurred_at"] = datetime.utcnow()
    tx = create_document("transaction", data)
    return Transaction(**tx)


@app.get("/transactions", response_model=List[Transaction])
async def list_txs(user_id: Optional[str] = None, account_id: Optional[str] = None, limit: int = 50):
    filt = {}
    if user_id:
        filt["user_id"] = user_id
    if account_id:
        filt["account_id"] = account_id
    txs = get_documents("transaction", filt or None, limit=limit)
    return [Transaction(**t) for t in txs]
