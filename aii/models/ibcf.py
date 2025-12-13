from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd


@dataclass
class ModelConfig:
    processed_dir: str = "aii/data/processed"
    ratings_csv: Optional[str] = None
    movies_csv: Optional[str] = None
    popular_csv: Optional[str] = None

    min_user_history: int = 5
    max_k: int = 50

    # similarity build controls
    min_common_raters: int = 2
    topk_sim_per_item: int = 200

    def __post_init__(self) -> None:
        # derive CSV paths from processed_dir when not explicitly provided
        if not self.ratings_csv:
            self.ratings_csv = os.path.join(self.processed_dir, "ratings.csv")
        if not self.movies_csv:
            self.movies_csv = os.path.join(self.processed_dir, "movies.csv")
        if not self.popular_csv:
            self.popular_csv = os.path.join(self.processed_dir, "popular_movies.csv")


class IBCFRecommender:
    """
    Baseline Item-Based CF:
      - mean-center ratings per user
      - compute item-item cosine similarity using co-rating dot products
      - predict score(u,i) = sum_j sim(i,j)*r_u,j / sum_j |sim(i,j)|
    """

    def __init__(self, cfg: ModelConfig):
        self.cfg = cfg

        self.ratings: Optional[pd.DataFrame] = None
        self.movies: Optional[pd.DataFrame] = None
        self.popular: Optional[pd.DataFrame] = None

        self.user_hist: Dict[int, List[Tuple[int, float]]] = {}
        self.item_sims: Dict[int, List[Tuple[int, float, int]]] = {}  # item -> [(other, sim, common)]

        self.movie_title: Dict[int, str] = {}

    def load(self) -> None:
        # load CSVs with clear validation and helpful error messages
        try:
            self.ratings = pd.read_csv(self.cfg.ratings_csv)
        except Exception as e:  # FileNotFoundError, pd.errors.EmptyDataError, etc.
            raise RuntimeError(f"Failed to read ratings CSV at '{self.cfg.ratings_csv}': {e}")
        try:
            self.movies = pd.read_csv(self.cfg.movies_csv)
        except Exception as e:
            raise RuntimeError(f"Failed to read movies CSV at '{self.cfg.movies_csv}': {e}")
        try:
            self.popular = pd.read_csv(self.cfg.popular_csv)
        except Exception as e:
            raise RuntimeError(f"Failed to read popular CSV at '{self.cfg.popular_csv}': {e}")

        self.movie_title = dict(
            zip(self.movies["movie_id"].astype(int), self.movies["title"].astype(str))
        )

        self.user_hist.clear()
        for r in self.ratings.itertuples(index=False):
            self.user_hist.setdefault(int(r.user_id), []).append((int(r.movie_id), float(r.rating)))

    def fit(self) -> None:
        if self.ratings is None:
            raise RuntimeError("Call load() before fit().")

        df = self.ratings.copy()

        # mean-center per user (vectorized)
        user_mean = df.groupby("user_id")["rating"].mean()
        df = df.copy()
        df["r_c"] = df["rating"] - df["user_id"].map(user_mean).astype(float)

        # Build norms per item and dot products per item-pair using user groups
        norm: Dict[int, float] = {}
        dot: Dict[Tuple[int, int], float] = {}
        common: Dict[Tuple[int, int], int] = {}

        for uid, g in df.groupby("user_id"):
            items = list(zip(g["movie_id"].astype(int).tolist(), g["r_c"].astype(float).tolist()))
            # norms
            for i, rci in items:
                norm[i] = norm.get(i, 0.0) + rci * rci
            # pairwise dot + common
            n = len(items)
            for a in range(n):
                i, rci = items[a]
                for b in range(a + 1, n):
                    j, rcj = items[b]
                    if i == j:
                        continue
                    key = (i, j) if i < j else (j, i)
                    dot[key] = dot.get(key, 0.0) + (rci * rcj)
                    common[key] = common.get(key, 0) + 1

        # build per-item sim list (truncate)
        sims: Dict[int, List[Tuple[int, float, int]]] = {}
        for (i, j), d in dot.items():
            c = common.get((i, j), 0)
            if c < self.cfg.min_common_raters:
                continue
            ni, nj = norm.get(i, 0.0), norm.get(j, 0.0)
            if ni <= 0 or nj <= 0:
                continue
            sim = float(d / (np.sqrt(ni) * np.sqrt(nj)))
            if sim <= 0:
                continue
            sims.setdefault(i, []).append((j, sim, c))
            sims.setdefault(j, []).append((i, sim, c))

        self.item_sims = {}
        for i, lst in sims.items():
            lst.sort(key=lambda x: x[1], reverse=True)
            self.item_sims[i] = lst[: self.cfg.topk_sim_per_item]

    def recommend(
        self,
        user_id: int,
        limit: int = 20,
        offset: int = 0,
        exclude_movie_ids: Optional[List[int]] = None,
        use_social: bool = False,  # reserved for later
        seed_movie_ids: Optional[List[int]] = None,
    ) -> List[Dict]:
        if limit > self.cfg.max_k:
            limit = self.cfg.max_k

        exclude = set(exclude_movie_ids or [])
        hist = self.user_hist.get(int(user_id), [])
        seen = {mid for mid, _ in hist}

        # Optional: treat seed_movie_ids as additional "history" (useful for demo)
        if seed_movie_ids:
            for mid in seed_movie_ids:
                if mid not in seen:
                    hist.append((int(mid), 4.0))  # neutral-ish positive
                    seen.add(int(mid))

        # Cold start
        if len(hist) < self.cfg.min_user_history:
            return self._popular_fallback(limit=limit, offset=offset, exclude=exclude)

        # Candidate scoring
        # score(i) accumulates sim(i,j) * rating(u,j)
        num: Dict[int, float] = {}
        den: Dict[int, float] = {}
        # keep best contributing seeds for explanations
        best_seed: Dict[int, Tuple[int, float]] = {}  # item -> (seed_movie, contrib)

        for seed_mid, seed_r in hist:
            for other_mid, sim, _common in self.item_sims.get(seed_mid, []):
                if other_mid in seen or other_mid in exclude:
                    continue
                contrib = sim * seed_r
                num[other_mid] = num.get(other_mid, 0.0) + contrib
                den[other_mid] = den.get(other_mid, 0.0) + abs(sim)

                prev = best_seed.get(other_mid)
                if prev is None or contrib > prev[1]:
                    best_seed[other_mid] = (seed_mid, contrib)

        scored = []
        for mid, n in num.items():
            d = den.get(mid, 1e-9)
            pred = n / d
            scored.append((mid, float(pred)))

        scored.sort(key=lambda x: x[1], reverse=True)
        window = scored[offset : offset + limit]

        # Normalize to [0,1] score (simple min-max on window, stable enough for mock)
        if not window:
            return self._popular_fallback(limit=limit, offset=offset, exclude=exclude)

        vals = [s for _, s in window]
        vmin, vmax = min(vals), max(vals)
        def to01(x: float) -> float:
            if vmax - vmin < 1e-9:
                return 0.5
            return (x - vmin) / (vmax - vmin)

        items = []
        for rank_idx, (mid, pred) in enumerate(window, start=1):
            seed_mid, _ = best_seed.get(mid, (None, 0.0))

            items.append(
                {
                    "movie_id": int(mid),
                    "score": float(to01(pred)),
                    "rank": int(offset + rank_idx),
                    "explanation": {
                        "primary_reason": "because_you_rated",
                        "confidence": 0.75,
                        "factors": [
                            {
                                "type": "because_you_rated",
                                "weight": 1.0,
                                "value": 1,
                                "payload": {"seed_movie_ids": [int(seed_mid)] if seed_mid else []},
                                "description": "Recommended based on similar movies you rated",
                            }
                        ],
                    },
                }
            )
        return items

    def explain(self, user_id: int, movie_id: int) -> Dict:
        hist = self.user_hist.get(int(user_id), [])
        seen = {mid for mid, _ in hist}

        if len(hist) < self.cfg.min_user_history:
            return {
                "movie_id": int(movie_id),
                "ai_score": 50,
                "explanation": {
                    "primary_reason": "popular",
                    "confidence": 0.6,
                    "factors": [
                        {
                            "type": "popular",
                            "weight": 1.0,
                            "value": 1,
                            "payload": {},
                            "description": "Recommended because it's popular among users",
                        }
                    ],
                },
                "social_signals": {"friend_ratings_count": 0, "friend_ratings_avg": None, "friend_watch_count": 0},
            }

        # find strongest similar item from user history
        best = None  # (seed_mid, sim)
        for seed_mid, _r in hist:
            for other_mid, sim, _c in self.item_sims.get(seed_mid, []):
                if int(other_mid) == int(movie_id):
                    if best is None or sim > best[1]:
                        best = (seed_mid, sim)

        if best is None:
            primary = "because_you_rated"
            payload = {"seed_movie_ids": [mid for mid, _ in hist[:2]]}
            desc = "Recommended based on your rating history"
            conf = 0.65
        else:
            primary = "because_you_rated"
            payload = {"seed_movie_ids": [int(best[0])]}
            desc = "Recommended because you rated a similar movie"
            conf = 0.78

        # map to ai_score 0-100 (mock)
        ai_score = int(round(conf * 100))

        return {
            "movie_id": int(movie_id),
            "ai_score": ai_score,
            "explanation": {
                "primary_reason": primary,
                "confidence": float(conf),
                "factors": [
                    {
                        "type": "because_you_rated",
                        "weight": 1.0,
                        "value": 1,
                        "payload": payload,
                        "description": desc,
                    }
                ],
            },
            "social_signals": {"friend_ratings_count": 0, "friend_ratings_avg": None, "friend_watch_count": 0},
        }

    def _popular_fallback(self, limit: int, offset: int, exclude: set[int]) -> List[Dict]:
        assert self.popular is not None
        rows = self.popular[~self.popular["movie_id"].isin(list(exclude))].iloc[offset : offset + limit]
        items = []
        for idx, r in enumerate(rows.itertuples(index=False), start=1):
            items.append(
                {
                    "movie_id": int(r.movie_id),
                    "score": 0.5,  # neutral for cold-start
                    "rank": int(offset + idx),
                    "explanation": {
                        "primary_reason": "popular",
                        "confidence": 0.6,
                        "factors": [
                            {
                                "type": "popular",
                                "weight": 1.0,
                                "value": int(getattr(r, "rating_count", 1)),
                                "payload": {},
                                "description": "Recommended because it's popular",
                            }
                        ],
                    },
                }
            )
        return items
