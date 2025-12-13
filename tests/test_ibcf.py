import os
import pandas as pd
from aii.models.ibcf import ModelConfig, IBCFRecommender


def test_ibcf_smoke(tmp_path):
    processed = tmp_path / "processed"
    processed.mkdir()

    # movies.csv - minimal
    movies = pd.DataFrame({"movie_id": [10, 20, 30], "title": ["A", "B", "C"]})
    movies.to_csv(processed / "movies.csv", index=False)

    # ratings.csv - small user history
    ratings = pd.DataFrame(
        {
            "user_id": [1, 1, 2, 2],
            "movie_id": [10, 20, 10, 30],
            "rating": [5.0, 4.0, 3.0, 4.0],
            "timestamp": [1, 2, 3, 4],
        }
    )
    ratings.to_csv(processed / "ratings.csv", index=False)

    # popular_movies.csv - simple fallback table
    pop = pd.DataFrame({"movie_id": [10, 20, 30], "rating_count": [2, 1, 1], "rating_avg": [4.5, 4.0, 4.0]})
    pop.to_csv(processed / "popular_movies.csv", index=False)

    cfg = ModelConfig(processed_dir=str(processed))
    rec = IBCFRecommender(cfg)
    rec.load()
    rec.fit()
    out = rec.recommend(user_id=1, limit=2)

    assert isinstance(out, list)
    assert len(out) <= 2
    assert all("movie_id" in r and "score" in r for r in out)
