from fastapi import FastAPI
from routers import users, restaurants, menu, orders

app = FastAPI(title="Food Delivery API")

app.include_router(users.router)
app.include_router(restaurants.router)
app.include_router(menu.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"status": "Food API running"}
