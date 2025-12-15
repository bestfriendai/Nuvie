# aii/explanations/reason_generator.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Set


@dataclass(frozen=True)
class ReasonInput:
    user_id: int
    rec_movie_id: int
    seed_movie_id: Optional[int]
    movie_title: Dict[int, str]
    movie_genres: Dict[int, Set[str]]
    use_social: bool = False
    friend_ids: Optional[List[int]] = None


def generate_reason(inp: ReasonInput) -> Dict:
    rec_title = inp.movie_title.get(inp.rec_movie_id, "this movie")
    seed_title = inp.movie_title.get(inp.seed_movie_id, "a movie you liked") if inp.seed_movie_id else None

    rec_g = inp.movie_genres.get(inp.rec_movie_id, set())
    seed_g = inp.movie_genres.get(inp.seed_movie_id, set()) if inp.seed_movie_id else set()
    overlap = sorted(rec_g & seed_g)

    # Social placeholder (until real friend graph is wired)
    if inp.use_social:
        return {
            "primary_reason": "social",
            "confidence": 0.70,
            "text": "Popular with people you follow, and similar to your taste.",
            "factors": [
                {"type": "social", "weight": 0.6, "payload": {"friend_ids": inp.friend_ids or []}},
                {"type": "genre_overlap", "weight": 0.4, "payload": {"overlap": overlap[:3]}},
            ],
        }

    if inp.seed_movie_id and overlap:
        return {
            "primary_reason": "genre_overlap",
            "confidence": 0.78,
            "text": f"Because you liked {seed_title} and it shares genres: {', '.join(overlap[:3])}.",
            "factors": [
                {"type": "because_you_rated", "weight": 0.6, "payload": {"seed_movie_id": int(inp.seed_movie_id)}},
                {"type": "genre_overlap", "weight": 0.4, "payload": {"overlap": overlap[:3]}},
            ],
        }

    if inp.seed_movie_id:
        return {
            "primary_reason": "because_you_rated",
            "confidence": 0.75,
            "text": f"Because you liked {seed_title}, which is similar to {rec_title}.",
            "factors": [
                {"type": "because_you_rated", "weight": 1.0, "payload": {"seed_movie_id": int(inp.seed_movie_id)}},
            ],
        }

    return {
        "primary_reason": "popular",
        "confidence": 0.60,
        "text": f"Recommended because {rec_title} is popular among users.",
        "factors": [{"type": "popular", "weight": 1.0, "payload": {}}],
    }
