# aii/models/ibcf.py
from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

from aii.explanations.reason_generator import ReasonInput, generate_reason


@dataclass
class ModelConfig:
    processed_dir: str = "aii/data/processed"
    ratings_csv: Optional[str] = None
    movies_csv: Optional[str] = None
    popular_csv: Optional[str] = None

    # similarity cache (so FastAPI startup doesn't hang every time)
    sims_cache: Optional[str] = None

    min_user_history: int = 5
    max_k: int = 50

    # similarity build controls
    min_common_raters: int = 2
    topk_sim_per_item: int = 200

    def __post_init__(self) -> None:
        if not self.ratings_csv:
            self.ratings_csv = os.path.join(self.processed_dir, "ratings.csv")
        if not self.movies_csv:
            self.movies_csv = os.path.join(self.processed_dir, "movies.csv")
        if not self.popular_csv:
            self.popular_csv = os.path.join(self.processed_dir, "popular_movies.csv")
        if not self.sims_cache:
            self.sims_cache = os.path.join(self.processed_dir, "item_sims.npz")


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
        # item -> [(other, sim, common)]
        self.item_sims: Dict[int, List[Tuple[int, float, int]]] = {}

        self.movie_title: Dict[int, str] = {}
        self.movie_genres: Dict[int, set[str]] = {}

    def load(self) -> None:
        try:
            self.ratings = pd.read_csv(self.cfg.ratings_csv)
        except Exception as e:
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

        def _parse_genres(s: str) -> set[str]:
            if not isinstance(s, str) or not s:
                return set()
            return {g.strip().lower() for g in s.split("|") if g.strip()}

        if "genres" in self.movies.columns:
            self.movie_genres = dict(
                zip(
                    self.movies["movie_id"].astype(int),
                    self.movies["genres"].astype(str).map(_parse_genres),
                )
            )
        else:
            self.movie_genres = {}

        self.user_hist.clear()
        for r in self.ratings.itertuples(index=False):
            self.user_hist.setdefault(int(r.user_id), []).append((int(r.movie_id), float(r.rating)))

    def load_or_fit(self) -> None:
        """
        Load cached similarities if present; otherwise fit and cache them.
        This prevents FastAPI startup from hanging every run.
        """
        try:
            if self.cfg.sims_cache and os.path.exists(self.cfg.sims_cache):
                data = np.load(self.cfg.sims_cache, allow_pickle=True)
                self.item_sims = data["item_sims"].item()
                return
        except Exception:
            # fall back to recompute
            pass

        self.fit()

        try:
            os.makedirs(os.path.dirname(self.cfg.sims_cache), exist_ok=True)
            np.savez_compressed(self.cfg.sims_cache, item_sims=self.item_sims)
        except Exception:
            # caching is best-effort
            pass

    def fit(self) -> None:
        if self.ratings is None:
            raise RuntimeError("Call load() before fit().")

        df = self.ratings.copy()

        user_mean = df.groupby("user_id")["rating"].mean()
        df["r_c"] = df["rating"] - df["user_id"].map(user_mean).astype(float)

        norm: Dict[int, float] = {}
        dot: Dict[Tuple[int, int], float] = {}
        common: Dict[Tuple[int, int], int] = {}

        for _uid, g in df.groupby("user_id"):
            items = list(zip(g["movie_id"].astype(int).tolist(), g["r_c"].astype(float).tolist()))
            for i, rci in items:
                norm[i] = norm.get(i, 0.0) + rci * rci

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
        use_social: bool = False,
        seed_movie_ids: Optional[List[int]] = None,
    ) -> List[Dict]:
        if limit > self.cfg.max_k:
            limit = self.cfg.max_k

        exclude = set(exclude_movie_ids or [])
        hist = list(self.user_hist.get(int(user_id), []))  # copy
        seen = {mid for mid, _ in hist}

        seed_movie_ids = [int(m) for m in (seed_movie_ids or []) if int(m) not in exclude]
        effective_seen = set(seen) | set(seed_movie_ids)

        # If no/low history but you gave seeds, do seed-only recs instead of popular.
        if len(effective_seen) < self.cfg.min_user_history:
            if seed_movie_ids:
                return self._seed_only_recommend(seed_movie_ids, limit=limit, offset=offset, exclude=exclude, use_social=use_social)
            return self._popular_fallback(limit=limit, offset=offset, exclude=exclude)

        # Add seeds to history as "soft likes"
        for mid in seed_movie_ids:
            if mid not in seen:
                hist.append((mid, 4.0))
                seen.add(mid)

        # Candidate scoring
        num: Dict[int, float] = {}
        den: Dict[int, float] = {}
        best_seed: Dict[int, Tuple[int, float]] = {}

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
            scored.append((mid, float(n / d)))

        scored.sort(key=lambda x: x[1], reverse=True)
        window = scored[offset : offset + limit]

        if not window:
            return self._popular_fallback(limit=limit, offset=offset, exclude=exclude)

        vals = [s for _, s in window]
        vmin, vmax = min(vals), max(vals)

        def to01(x: float) -> float:
            if vmax - vmin < 1e-9:
                return 0.5
            return (x - vmin) / (vmax - vmin)

        items: List[Dict] = []
        for rank_idx, (mid, pred) in enumerate(window, start=1):
            seed_mid, _ = best_seed.get(mid, (None, 0.0))

            reason = generate_reason(
                ReasonInput(
                    user_id=int(user_id),
                    rec_movie_id=int(mid),
                    seed_movie_id=int(seed_mid) if seed_mid else None,
                    movie_title=self.movie_title,
                    movie_genres=self.movie_genres,
                    use_social=use_social,
                    friend_ids=None,
                )
            )

            items.append(
                {
                    "movie_id": int(mid),
                    "score": float(to01(pred)),
                    "rank": int(offset + rank_idx),
                    "explanation": {
                        "primary_reason": reason["primary_reason"],
                        "confidence": float(reason["confidence"]),
                        "text": reason["text"],
                        "factors": reason["factors"],
                    },
                }
            )
        return items

    def explain(self, user_id: int, movie_id: int, use_social: bool = False) -> Dict:
        hist = self.user_hist.get(int(user_id), [])
        exclude = set()
        seed_mid = None

        # pick strongest similar seed if possible
        best = None
        for smid, _r in hist:
            for other_mid, sim, _c in self.item_sims.get(smid, []):
                if int(other_mid) == int(movie_id):
                    if best is None or sim > best[1]:
                        best = (smid, sim)
        if best:
            seed_mid = int(best[0])

        reason = generate_reason(
            ReasonInput(
                user_id=int(user_id),
                rec_movie_id=int(movie_id),
                seed_movie_id=seed_mid,
                movie_title=self.movie_title,
                movie_genres=self.movie_genres,
                use_social=use_social,
                friend_ids=None,
            )
        )

        ai_score = int(round(float(reason["confidence"]) * 100))

        return {
            "movie_id": int(movie_id),
            "ai_score": ai_score,
            "explanation": {
                "primary_reason": reason["primary_reason"],
                "confidence": float(reason["confidence"]),
                "text": reason["text"],
                "factors": reason["factors"],
            },
            "social_signals": {
                "friend_ratings_count": 0,
                "friend_ratings_avg": None,
                "friend_watch_count": 0,
            },
        }

    def _seed_only_recommend(
        self,
        seed_movie_ids: List[int],
        limit: int,
        offset: int,
        exclude: set[int],
        use_social: bool,
    ) -> List[Dict]:
        # Use seeds as pseudo-history and score similar items
        hist = [(int(mid), 4.0) for mid in seed_movie_ids if int(mid) not in exclude]
        seen = {mid for mid, _ in hist}

        num: Dict[int, float] = {}
        den: Dict[int, float] = {}
        best_seed: Dict[int, Tuple[int, float]] = {}

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

        scored = [(mid, n / max(den.get(mid, 1e-9), 1e-9)) for mid, n in num.items()]
        scored.sort(key=lambda x: x[1], reverse=True)
        window = scored[offset : offset + limit]

        if not window:
            return self._popular_fallback(limit=limit, offset=offset, exclude=exclude)

        vals = [s for _, s in window]
        vmin, vmax = min(vals), max(vals)

        def to01(x: float) -> float:
            if vmax - vmin < 1e-9:
                return 0.5
            return (x - vmin) / (vmax - vmin)

        out: List[Dict] = []
        for idx, (mid, pred) in enumerate(window, start=1):
            seed_mid, _ = best_seed.get(mid, (None, 0.0))
            reason = generate_reason(
                ReasonInput(
                    user_id=-1,
                    rec_movie_id=int(mid),
                    seed_movie_id=int(seed_mid) if seed_mid else None,
                    movie_title=self.movie_title,
                    movie_genres=self.movie_genres,
                    use_social=use_social,
                    friend_ids=None,
                )
            )
            out.append(
                {
                    "movie_id": int(mid),
                    "score": float(to01(pred)),
                    "rank": int(offset + idx),
                    "explanation": {
                        "primary_reason": reason["primary_reason"],
                        "confidence": float(reason["confidence"]),
                        "text": reason["text"],
                        "factors": reason["factors"],
                    },
                }
            )
        return out

    def _popular_fallback(self, limit: int, offset: int, exclude: set[int]) -> List[Dict]:
        assert self.popular is not None
        rows = self.popular[~self.popular["movie_id"].isin(list(exclude))].iloc[offset : offset + limit]
        items = []
        for idx, r in enumerate(rows.itertuples(index=False), start=1):
            reason = {
                "primary_reason": "popular",
                "confidence": 0.60,
                "text": "Recommended because it's popular among users.",
                "factors": [{"type": "popular", "weight": 1.0, "payload": {}}],
            }
            items.append(
                {
                    "movie_id": int(r.movie_id),
                    "score": 0.5,
                    "rank": int(offset + idx),
                    "explanation": {
                        "primary_reason": reason["primary_reason"],
                        "confidence": float(reason["confidence"]),
                        "text": reason["text"],
                        "factors": reason["factors"],
                    },
                }
            )
        return items
