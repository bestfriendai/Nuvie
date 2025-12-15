from fastapi import FastAPI
from .feed import router as feed_router

# I create the FastAPI application instance
# because this is the entry point of my backend service
app = FastAPI(
    title="NUVIE Backend API",
    description="I use this service to deliver movie data to the iOS app",
    version="1.0.0"
)

# I register the feed router
# so endpoints like /feed/home become accessible
app.include_router(feed_router)

# I expose a health check endpoint
# so I can verify that the backend is running correctly
@app.get("/health")
def health():
    return {"status": "ok"}
