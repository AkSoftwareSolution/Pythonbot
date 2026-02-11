from fastapi import APIRouter
from backend.database import get_db

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

@router.get("/")
def get_restaurants():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM restaurants WHERE is_open=1")
    return cur.fetchall()
