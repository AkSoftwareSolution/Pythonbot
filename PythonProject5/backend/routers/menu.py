from fastapi import APIRouter
from backend.database import get_db

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/{restaurant_id}")
def menu(restaurant_id: int):

    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT * FROM menu_items WHERE restaurant_id=%s",
        (restaurant_id,)
    )
    return cur.fetchall()
