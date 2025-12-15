# aii/serving/app.py
from __future__ import annotations

import os
import time
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from aii.models.ibcf import IBCFRecommender, ModelConfig

INTERNAL_TOKEN = os.environ.get("AI_INTERNAL_TOKEN", "dev-internal-token")


def api_error(code: str, message: str, details: Optional[dict] = None, status_code: int = 400):
    raise HTTPException(
        status_code=status_code,
        detail={
            "error": {
                "code": code,
                "message": message,
                "details": details or {},
            }
        },
    )


class Context(BaseModel):
    use_social: bool = True
    seed_movie_ids: list[int] = Field(default_factory=list)
    locale: Optional[str] = "en-US"
    time: Optional[str] = None


class RecommendRequest(BaseModel):
    request_id: str
    user_id: int
    limit: int = 20
    offset: int = 0
    exclude_movie_ids: list[int] = Field(default_factory=list)
    context: Context = Field(default_factory=Context)


class ExplainRequest(BaseModel):
    request_id: str
    user_id: int
    movie_id: int
    context: Context = Field(default_factory=Context)


app = FastAPI(title="NUVIE AI Service", version="0.3.0")

model: Optional[IBCFRecommender] = None


@app.on_event("startup")
def _startup():
    global model
    m = IBCFRecommender(ModelConfig())
    m.load()
    # IMPORTANT: caches similarities to disk so startup is fast after first run
    m.load_or_fit()
    model = m


def _auth_or_401(x_internal_token: Optional[str]):
    if x_internal_token != INTERNAL_TOKEN:
        api_error("AUTHENTICATION_REQUIRED", "Missing or invalid X-Internal-Token", status_code=401)
    return True


@app.get("/health")
def health():
    return {"ok": True, "model_loaded": model is not None}


@app.post("/ai/recommend")
def recommend(
    req: RecommendRequest,
    x_internal_token: Optional[str] = Header(default=None, alias="X-Internal-Token"),
):
    _auth_or_401(x_internal_token)

    if req.limit < 1:
        api_error("INVALID_REQUEST", "limit must be >= 1", details={"limit": req.limit})
    if req.limit > 50:
        api_error("INVALID_REQUEST", "limit max 50", details={"limit": req.limit})
    if req.offset < 0:
        api_error("INVALID_REQUEST", "offset must be >= 0", details={"offset": req.offset})

    if model is None:
        api_error("MODEL_NOT_READY", "Model not loaded", status_code=503)

    t0 = time.time()

    items = model.recommend(
        user_id=req.user_id,
        limit=req.limit,
        offset=req.offset,
        exclude_movie_ids=req.exclude_movie_ids,
        use_social=req.context.use_social,
        seed_movie_ids=req.context.seed_movie_ids,
    )

    # double safety
    excl = set(req.exclude_movie_ids or [])
    items = [it for it in items if int(it["movie_id"]) not in excl]

    return {
        "request_id": req.request_id,
        "user_id": req.user_id,
        "model": {"name": "ibcf", "version": "v1", "trained_at": None},
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ttl_seconds": 900,
        "items": items,
        "meta": {"latency_ms": int((time.time() - t0) * 1000)},
    }


@app.post("/ai/explain")
def explain(
    req: ExplainRequest,
    x_internal_token: Optional[str] = Header(default=None, alias="X-Internal-Token"),
):
    _auth_or_401(x_internal_token)

    if model is None:
        api_error("MODEL_NOT_READY", "Model not loaded", status_code=503)

    out = model.explain(user_id=req.user_id, movie_id=req.movie_id, use_social=req.context.use_social)

    return {
        "request_id": req.request_id,
        "user_id": req.user_id,
        "movie_id": req.movie_id,
        "ai_score": out.get("ai_score", 50),
        "explanation": out["explanation"],
        "social_signals": out.get("social_signals", {}),
    }
