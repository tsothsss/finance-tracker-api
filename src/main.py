from fastapi import FastAPI
from src.routers import expenses, analytics, subscriptions
from src.routers import expenses, analytics, subscriptions, auth



app = FastAPI(
    title="Finance & Subscription Tracker API",
    description="A robust backend service to manage personal expenses, recurring subscriptions, and analytics.",
    version="1.0.0"
)

app.include_router(expenses.router)
app.include_router(analytics.router)
app.include_router(subscriptions.router)
app.include_router(auth.router)

@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "service": "Finance Tracker API",
        "version": "1.0.0"
    }