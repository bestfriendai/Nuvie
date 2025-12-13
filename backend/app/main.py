from fastapi import FastAPI
from .feed import router as feed_router

app = FastAPI(title="NUVIE Backend API")

# I include routers here so the endpoints are actually reachable
app.include_router(feed_router)

@app.get("/health")
def health():
    return {"status": "ok"}
