from fastapi import APIRouter

router = APIRouter()

@router.get("/feed")
def get_feed():
    return {
        "items": [
            {"movie_id": 1, "score": 0.95},
            {"movie_id": 2, "score": 0.90}
        ]
    }

