from fastapi import APIRouter
from backend.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/login")
def login(phone: str):
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT IGNORE INTO users(phone) VALUES(%s)", (phone,))
    db.commit()
    return {"message": "Login successful", "phone": phone}
