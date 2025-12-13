import os
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from .auth import get_current_user
from backend.session import get_db

router = APIRouter(prefix="/feed", tags=["Feed"])


def safe_year(release_date):
    # I extract the year safely so the API never crashes on missing dates
    if not release_date:
        return None
    try:
        return int(str(release_date)[:4])
    except Exception:
        return None


@router.get("/home")
def home_feed(
    limit: int = 20,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    This endpoint returns a feed of movie recommendations for the logged-in user.

    Phase 2 note:
    - I only check that a Bearer token exists (auth stub).
    - I read movies directly from DB (Neon) to give iOS real posters/overview.
    """
    user_id = user["id"]  # I keep this for future AI personalization

    # I pull real movie metadata from DB so the mobile feed can render posters and text
    rows = db.execute(
        text("""
            SELECT movie_id, title, poster_url, overview, release_date
            FROM movies
            ORDER BY movie_id
            LIMIT :limit
        """),
        {"limit": limit},
    ).mappings().all()

    return {
        "items": [
            {
                "type": "recommendation",
                "created_at": "2025-12-13T10:00:00Z",
                "movie": {
                    "id": r["movie_id"],
                    "title": r["title"],
                    "year": safe_year(r["release_date"]),
                    "poster_url": r["poster_url"],
                    "overview": r["overview"],
                    "release_date": r["release_date"],
                },
                "score": 0.8,
                "reason_chips": ["DB fallback (Phase 2)"],
            }
            for r in rows
        ]
    }
