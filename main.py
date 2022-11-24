from fastapi import FastAPI
from router import user_router, transaction_router, subscription_router, token_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"Broadcast application": "v0.0.1"}

app.include_router(user_router)
app.include_router(transaction_router)
app.include_router(subscription_router)
app.include_router(token_router)