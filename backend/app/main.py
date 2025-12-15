from fastapi import FastAPI

from backend.session import Base, engine
from backend.models import user  # ⚠️ MODEL IMPORT ŞART (yoksa tablo oluşmaz)

from .feed import router as feed_router
from .auth import router as auth_router

app = FastAPI(title="Nuvie Backend API")


@app.on_event("startup")
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


app.include_router(auth_router)
app.include_router(feed_router)


@app.get("/health")
def health():
    return {"status": "ok"}
