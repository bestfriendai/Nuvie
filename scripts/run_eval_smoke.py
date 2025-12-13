#!/usr/bin/env python3
"""Smoke-run the offline evaluation with tiny synthetic data."""
import tempfile
import os
import pandas as pd
from aii.evaluation.offline_metrics import EvalConfig, run_offline_eval


def make_data(tmpdir):
    # create a tiny ratings CSV with timestamps
    rows = [
        # user 1
        (1, 10, 5.0, 1),
        (1, 20, 4.0, 2),
        (1, 30, 3.0, 3),
        (1, 40, 2.0, 4),
        (1, 50, 1.0, 5),
        # user 2
        (2, 10, 4.0, 1),
        (2, 20, 3.0, 2),
        (2, 30, 5.0, 3),
        (2, 40, 4.0, 4),
        (2, 50, 2.0, 5),
    ]
    df = pd.DataFrame(rows, columns=["user_id", "movie_id", "rating", "timestamp"]) 
    path = os.path.join(tmpdir, "ratings.csv")
    df.to_csv(path, index=False)
    return path


def main():
    with tempfile.TemporaryDirectory() as d:
        ratings_csv = make_data(d)
        cfg = EvalConfig(ratings_csv=ratings_csv, test_ratio=0.4, k=5, min_user_test_items=1)
        res = run_offline_eval(cfg)
        print("Offline eval results:")
        for k, v in res.items():
            print(f"{k}: {v}")


if __name__ == '__main__':
    main()
