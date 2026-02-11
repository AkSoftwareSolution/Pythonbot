from fastapi import APIRouter
from backend.database import get_db

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def place_order(user_id:int, restaurant_id:int, total:float, address:str):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO orders(user_id,restaurant_id,total,status,address) VALUES(%s,%s,%s,'PENDING',%s)",
        (user_id, restaurant_id, total, address)
    )
    db.commit()
    return {"message": "Order placed", "status": "PENDING"}
