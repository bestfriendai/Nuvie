# aii/evaluation/offline_metrics.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from aii.models.ibcf import IBCFRecommender, ModelConfig


@dataclass
class EvalConfig:
    ratings_csv: str = "aii/data/processed/ratings.csv"
    test_ratio: float = 0.2
    k: int = 10
    min_user_test_items: int = 1


def temporal_split(ratings: pd.DataFrame, test_ratio: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split per user by timestamp: last X% interactions as test.
    """
    ratings = ratings.sort_values(["user_id", "timestamp"])
    train_parts = []
    test_parts = []

    for uid, g in ratings.groupby("user_id"):
        n = len(g)
        if n < 5:
            train_parts.append(g)
            continue
        cut = int(np.floor(n * (1 - test_ratio)))
        train_parts.append(g.iloc[:cut])
        test_parts.append(g.iloc[cut:])

    train = pd.concat(train_parts, ignore_index=True)
    test = pd.concat(test_parts, ignore_index=True) if test_parts else ratings.iloc[:0].copy()
    return train, test


def rmse_mae(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    err = y_true - y_pred
    rmse = float(np.sqrt(np.mean(err * err))) if len(err) else float("nan")
    mae = float(np.mean(np.abs(err))) if len(err) else float("nan")
    return {"rmse": rmse, "mae": mae}


def recall_at_k(recommended: List[int], relevant: set[int], k: int) -> float:
    rec_k = recommended[:k]
    if not relevant:
        return 0.0
    return float(len(set(rec_k) & relevant) / len(relevant))


def dcg_at_k(recommended: List[int], relevant: set[int], k: int) -> float:
    score = 0.0
    for i, mid in enumerate(recommended[:k], start=1):
        if mid in relevant:
            score += 1.0 / np.log2(i + 1)
    return float(score)


def ndcg_at_k(recommended: List[int], relevant: set[int], k: int) -> float:
    dcg = dcg_at_k(recommended, relevant, k)
    ideal_hits = min(len(relevant), k)
    if ideal_hits == 0:
        return 0.0
    ideal = sum(1.0 / np.log2(i + 1) for i in range(1, ideal_hits + 1))
    return float(dcg / ideal)


def map_at_k(recommended: List[int], relevant: set[int], k: int) -> float:
    hits = 0
    ap_sum = 0.0
    for i, mid in enumerate(recommended[:k], start=1):
        if mid in relevant:
            hits += 1
            ap_sum += hits / i
    if not relevant:
        return 0.0
    return float(ap_sum / min(len(relevant), k))


def run_offline_eval(cfg: EvalConfig) -> Dict[str, float]:
    ratings = pd.read_csv(cfg.ratings_csv)
    # validate expected columns early with a clear error message
    required = {"user_id", "movie_id", "rating", "timestamp"}
    missing = required - set(ratings.columns)
    if missing:
        raise RuntimeError(f"Ratings CSV '{cfg.ratings_csv}' is missing required columns: {', '.join(sorted(missing))}")
    train_df, test_df = temporal_split(ratings, cfg.test_ratio)

    # Build a model only on train
    # (write temp CSVs in memory by overwriting config paths is possible, but simplest: patch recommender directly)
    model = IBCFRecommender(ModelConfig())
    model.ratings = train_df
    # minimal movie title map not needed for eval
    model.user_hist = {}
    for r in train_df.itertuples(index=False):
        model.user_hist.setdefault(int(r.user_id), []).append((int(r.movie_id), float(r.rating)))

    # Popular fallback also not needed for evaluation ranking; but explain uses it—safe to keep empty
    model.popular = (
        train_df.groupby("movie_id")
        .agg(rating_count=("rating", "size"), rating_avg=("rating", "mean"))
        .reset_index()
        .sort_values(["rating_count", "rating_avg"], ascending=[False, False])
    )

    model.fit()

    # Rating prediction eval: predict only on users with history
    y_true = []
    y_pred = []

    # Ranking eval
    recalls = []
    ndcgs = []
    maps = []

    test_by_user = test_df.groupby("user_id")

    for uid, g in test_by_user:
        relevant = set(g["movie_id"].astype(int).tolist())
        if len(relevant) < cfg.min_user_test_items:
            continue

        # Recommend K for ranking
        rec_items = model.recommend(user_id=int(uid), limit=cfg.k, offset=0, exclude_movie_ids=None)
        rec_ids = [int(x["movie_id"]) for x in rec_items]

        recalls.append(recall_at_k(rec_ids, relevant, cfg.k))
        ndcgs.append(ndcg_at_k(rec_ids, relevant, cfg.k))
        maps.append(map_at_k(rec_ids, relevant, cfg.k))

        # For RMSE/MAE, use the model's internal score as a proxy prediction mapped to 0.5..5.0
        # (Baseline: convert score [0,1] -> rating [0.5,5.0])
        rec_map = {int(x["movie_id"]): float(x["score"]) for x in rec_items}

        for row in g.itertuples(index=False):
            true_r = float(row.rating)
            s01 = rec_map.get(int(row.movie_id), 0.5)
            pred_r = 0.5 + 4.5 * s01
            y_true.append(true_r)
            y_pred.append(pred_r)

    rating_metrics = rmse_mae(np.array(y_true, dtype=float), np.array(y_pred, dtype=float))
    results = {
        **rating_metrics,
        "recall@k": float(np.mean(recalls)) if recalls else float("nan"),
        "ndcg@k": float(np.mean(ndcgs)) if ndcgs else float("nan"),
        "map@k": float(np.mean(maps)) if maps else float("nan"),
        "users_evaluated": int(len(recalls)),
    }
    return results


if __name__ == "__main__":
    cfg = EvalConfig()
    res = run_offline_eval(cfg)
    print(" Offline metrics")
    for k, v in res.items():
        print(f"{k}: {v}")
