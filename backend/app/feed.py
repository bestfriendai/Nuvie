from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from backend.session import get_db
from backend.auth import get_current_user

# I create a router for feed-related endpoints
router = APIRouter(
    prefix="/feed",
    tags=["Feed"]
)

@router.get("/home")
def home_feed(
    limit: int = 20,
    offset: int = 0,
    user = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # I extract the user id from the authenticated user
    user_id = int(user["id"])

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
            "poster_url": row["poster_url"],
            "overview": row["overview"],
            "release_date": row["release_date"],
            # I keep this empty for now and will fill it in Phase 3
            "reason_chips": []
        })

    # I return the feed data along with pagination info
    return {
        "user_id": user_id,
        "items": items,
        "next_offset": offset + limit
    }
