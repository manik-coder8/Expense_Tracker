from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sqlite3
import uuid
from datetime import datetime
from typing import Optional, List
import os 

app = FastAPI(title="Expense Tracker API")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "expenses.db")

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id TEXT PRIMARY KEY,
    amount INTEGER,
    category TEXT,
    description TEXT,
    date TEXT,
    created_at TEXT,
    request_id TEXT UNIQUE
)
""")
conn.commit()

# ---------- MODELS ----------
class ExpenseIn(BaseModel):
    amount: float = Field(gt=0)
    category: str
    description: Optional[str] = ""
    date: str
    request_id: str

class ExpenseOut(BaseModel):
    id: str
    amount: float
    category: str
    description: str
    date: str
    created_at: str

# ---------- API ----------
@app.post("/expenses", response_model=ExpenseOut)
def create_expense(expense: ExpenseIn):
    cursor.execute(
        "SELECT * FROM expenses WHERE request_id = ?",
        (expense.request_id,)
    )
    existing = cursor.fetchone()

    if existing:
        return {
            "id": existing[0],
            "amount": existing[1] / 100,
            "category": existing[2],
            "description": existing[3],
            "date": existing[4],
            "created_at": existing[5],
        }

    expense_id = str(uuid.uuid4())
    cursor.execute("""
        INSERT INTO expenses VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        expense_id,
        int(expense.amount * 100),
        expense.category,
        expense.description,
        expense.date,
        datetime.utcnow().isoformat(),
        expense.request_id
    ))
    conn.commit()

    return {
        "id": expense_id,
        "amount": expense.amount,
        "category": expense.category,
        "description": expense.description,
        "date": expense.date,
        "created_at": datetime.utcnow().isoformat(),
    }

@app.get("/expenses", response_model=List[ExpenseOut])
def list_expenses(
    category: Optional[str] = None,
    sort: Optional[str] = "date_desc"
):
    query = "SELECT * FROM expenses"
    params = []

    if category:
        query += " WHERE category = ?"
        params.append(category)

    if sort == "date_desc":
        query += " ORDER BY date DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "amount": r[1] / 100,
            "category": r[2],
            "description": r[3],
            "date": r[4],
            "created_at": r[5],
        }
        for r in rows
    ]
