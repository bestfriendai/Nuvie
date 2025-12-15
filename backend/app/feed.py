from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

# I import DB dependency so I can query the database when needed
from backend.session import get_db

# I import auth from the same folder (backend/app) so Python finds it correctly
from .auth import get_current_user

# I import AI client so I can ask the AI service for recommendations (Phase 3)
from .ai_client import get_ai_recommendations


# I create a router for feed-related endpoints
router = APIRouter(
    prefix="/feed",
    tags=["Feed"]
)


def safe_year(release_date):
    # I extract the year safely so the API never crashes on missing / weird dates
    if not release_date:
        return None
    try:
        return int(str(release_date)[:4])
    except Exception:
        return None


@router.get("/home")
def home_feed(
    limit: int = 20,
    offset: int = 0,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # I keep user_id as a string because JWT / user ids are usually strings (uuid, etc.)
    user_id = user["id"]

    # ----------------------------
    # Phase 3: Try AI first
    # ----------------------------
    try:
        # I call the AI service to get personalized recommendations
        # I pass user_id, limit, offset so AI can paginate too
        items = get_ai_recommendations(
            user_id=user_id,
            limit=limit,
            offset=offset
        )

        # I return AI items directly if AI succeeds
        return {
            "user_id": user_id,
            "items": items,
            "next_offset": offset + limit,
            "source": "ai"
        }

    except Exception:
        # ----------------------------
        # Phase 2 fallback: DB feed
        # ----------------------------

        # I query movies from the database
        # because Phase 2 only requires a simple feed (no personalization yet)
        rows = db.execute(
            text("""
                SELECT movie_id, title, poster_url, overview, release_date
                FROM movies
                ORDER BY movie_id
                LIMIT :limit OFFSET :offset
            """),
            {"limit": limit, "offset": offset}
        ).mappings().all()

        # I transform database rows into a JSON-friendly structure
        items = []
        for row in rows:
            items.append({
                "movie_id": row["movie_id"],
                "title": row["title"],
                "year": safe_year(row.get("release_date")),
                "poster_url": row["poster_url"],
                "overview": row["overview"],
                "release_date": row["release_date"],
                # I keep this simple in fallback mode
                "reason_chips": ["DB fallback (AI failed)"]
            })

        # I return the feed data along with pagination info
        return {
            "user_id": user_id,
            "items": items,
            "next_offset": offset + limit,
            "source": "db_fallback"
        }
