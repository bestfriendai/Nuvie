from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

import pandas as pd


@dataclass
class PipelineConfig:
    raw_movies_path: str = "ai/data/movies.dat"
    raw_ratings_path: str = "ai/data/ratings.dat"
    processed_dir: str = "ai/data/processed"

    movies_csv: str = "ai/data/processed/movies.csv"
    ratings_csv: str = "ai/data/processed/ratings.csv"
    popular_csv: str = "ai/data/processed/popular_movies.csv"
    stats_json: str = "ai/data/processed/dataset_stats.json"

def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def _read_movies_dat(path: str) -> pd.DataFrame:
    """
    MovieLens .dat common format:
      movie_id::title (year)::Genre1|Genre2|...
    """
    df = pd.read_csv(
        path,
        sep="::",
        engine="python",
        header=None,
        names=["movie_id", "title", "genres_raw"],
        encoding="latin-1",
    )
    df["movie_id"] = df["movie_id"].astype(int)
    df["genres_raw"] = df["genres_raw"].fillna("").astype(str)

def parse_year(title: str) -> Optional[int]:
        m = re.search(r"\((\d{4})\)\s*$", title)
        return int(m.group(1)) if m else None

    def strip_year(title: str) -> str:
        return re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()

    df["year"] = df["title"].apply(parse_year)
    df["clean_title"] = df["title"].apply(strip_year)
    df["genres"] = df["genres_raw"].apply(
        lambda s: [g for g in s.split("|") if g and g != "(no genres listed)"]
    )
    return df[["movie_id", "title", "clean_title", "year", "genres_raw", "genres"]]

def parse_year(title: str) -> Optional[int]:
        m = re.search(r"\((\d{4})\)\s*$", title)
        return int(m.group(1)) if m else None

    def strip_year(title: str) -> str:
        return re.sub(r"\s*\(\d{4}\)\s*$", "", title).strip()

    df["year"] = df["title"].apply(parse_year)
    df["clean_title"] = df["title"].apply(strip_year)
    df["genres"] = df["genres_raw"].apply(
        lambda s: [g for g in s.split("|") if g and g != "(no genres listed)"]
    )
    return df[["movie_id", "title", "clean_title", "year", "genres_raw", "genres"]]

def run_pipeline(cfg: PipelineConfig) -> Tuple[pd.DataFrame, pd.DataFrame]:
    _ensure_dir(cfg.processed_dir)

    movies = _read_movies_dat(cfg.raw_movies_path)
    ratings = _read_ratings_dat(cfg.raw_ratings_path)

    # Clean ratings
    ratings = ratings.dropna(subset=["user_id", "movie_id", "rating"])
    ratings = ratings[(ratings["rating"] >= 0.5) & (ratings["rating"] <= 5.0)]

    # Keep only ratings for existing movies
    ratings = ratings.merge(movies[["movie_id"]], on="movie_id", how="inner")

    # Dedup (keep latest)
    ratings = ratings.sort_values(["user_id", "movie_id", "timestamp"], ascending=True)
    ratings = ratings.drop_duplicates(["user_id", "movie_id"], keep="last")

    # Save processed tables
    movies.to_csv(cfg.movies_csv, index=False)
    ratings.to_csv(cfg.ratings_csv, index=False)
  
    # Popularity for cold-start (count desc, then avg rating desc)
    pop = (
        ratings.groupby("movie_id")
        .agg(rating_count=("rating", "size"), rating_avg=("rating", "mean"))
        .reset_index()
        .sort_values(["rating_count", "rating_avg"], ascending=[False, False])
    )
    pop.to_csv(cfg.popular_csv, index=False)

    stats = {
        "movies": int(len(movies)),
        "ratings": int(len(ratings)),
        "users": int(ratings["user_id"].nunique()),
        "items": int(ratings["movie_id"].nunique()),
        "min_rating": float(ratings["rating"].min()),
        "max_rating": float(ratings["rating"].max()),
    }
    with open(cfg.stats_json, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

    print(f"wrote {cfg.movies_csv}")
    print(f"wrote {cfg.ratings_csv}")
    print(f"wrote {cfg.popular_csv}")
    print(f"wrote {cfg.stats_json}")
    return movies, ratings


if __name__ == "__main__":
    run_pipeline(PipelineConfig())

    
