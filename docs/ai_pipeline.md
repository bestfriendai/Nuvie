
# AI Pipeline — NUVIE

This document describes the AI recommendation pipeline for NUVIE (Phase 1).
It defines required input tables/features, output format, and explainability reason types.

---

## 1) Goals (Phase 1 / Phase 2 alignment)

**Phase 1 (Docs)**
- Define AI inputs (tables + features)
- Define AI outputs (recommendation response format)
- Define explainability reason types (genre, friend, etc.)
- Share AI data needs with DB + Backend teams

**Phase 2 (Implementation)**
- Build baseline recommender (IBCF)
- Generate offline metrics (RMSE/Recall@K)
- Serve mock recommendations via FastAPI

---

## 2) AI Inputs (Required tables & columns)

### Core tables (required)

**users**
- `user_id` (PK)

**movies**
- `movie_id` (PK)
- `title` (string)
- `genres` (string or array)  
  - if stored as `"Action|Sci-Fi"` or `"action|sci-fi"`: must be parseable

**ratings**
- `user_id` (FK → users.user_id)
- `movie_id` (FK → movies.movie_id)
- `rating` (int or float)
- `timestamp` (optional but recommended)

### Social / behavioral tables (recommended)

**friends**
- `user_id_1` (FK → users.user_id)
- `user_id_2` (FK → users.user_id)
- `status` (pending/accepted/blocked)
- `created_at`

**watch_events**
- `event_id` (PK)
- `user_id` (FK → users.user_id)
- `movie_id` (FK → movies.movie_id)
- `event_type` (started/completed/paused)
- `progress_percent` (optional)
- `timestamp`

### Output cache table (optional)

**recommendation_feed**
- `user_id` (unique, FK → users.user_id)
- `movie_id_list` (integer[])
- `last_calculated` (timestamp)

---

## 3) Feature Definitions (v1)

### 3.1 User–Genre Vector
- Parse `movies.genres` into a multi-hot vector
- For each user:
  - `user_genre_score[g] = sum_over_ratings( rating(u,m) * 1[m has genre g] )`
- Normalize user vector (L2 or sum-to-1)

Used for:
- Cold-start personalization
- Explainability: `genre_match`

### 3.2 Item Popularity (Fallback)
- `popularity(movie) = count(ratings)`, optionally weighted by average rating
- Used when user has little or no rating history

Used for:
- Cold-start fallback
- Explainability: `popular` / `trending`

### 3.3 Social Signals (Optional Boost)
Signals derived from friends and watch events:
- number of friends who rated/watched the movie
- average friend rating
- recent friend activity window (e.g., last 7 days)

Used for:
- Social ranking / re-ranking
- Explainability: `friend_activity`

---

## 4) AI Outputs (Standard response objects)

AI output must follow the internal contract used by Backend:

### 4.1 Recommendation result (internal)
- `movie_id` (int)
- `score` (float in `[0,1]`)
- `rank` (int)
- `explanation` (object)

Backend maps:
- `ai_score = round(score * 100)` (0–100)

### 4.2 Explanation object
- `primary_reason` (string)
- `confidence` (float 0–1)
- `factors[]`:
  - `type` (enum)
  - `weight` (float 0–1)
  - `value` (number)
  - `payload` (object)
  - `description` (string)

---

## 5) Explainability Reason Types (Enum)

Allowed factor types:

- `genre_match`
  - payload: `{ "genres": ["Sci-Fi", "Action"] }`
- `because_you_rated`
  - payload: `{ "seed_movie_ids": [1,2] }`
- `similar_users`
  - payload: `{ "neighbor_user_ids": [44,91] }` (optional to expose)
- `friend_activity`
  - payload: `{ "friend_user_ids": [2,8,19] }`
- `trending`
  - payload: `{ "window_days": 7 }`
- `popular`
  - payload: `{ "rating_count": 12000 }`

Rules:
- `type` must be one of the above
- `payload` must be small and UI-safe
- `description` can be AI-generated or (preferred) Backend-generated for localization/i18n

---

## 6) Baseline Model Plan (Phase 2)

### Model: IBCF (Item-Based Collaborative Filtering)
- Compute item-item similarity (cosine) from ratings matrix
- Recommend by aggregating similarities of items the user rated highly
- Apply filters:
  - remove already-rated / watched items
  - apply backend-provided `exclude_movie_ids`

### Cold start behavior
- If user has insufficient ratings:
  - return popularity/trending list
  - explanation primary reason: `popular` or `trending`

---

## 7) Offline Evaluation (Phase 2)

Metrics:
- `Recall@K` for top-K ranking
- Optional: `RMSE` if doing rating prediction

Splits:
- preferred: time-based split using `ratings.timestamp`
- fallback: random train/test split

---

## 8) Data Needs to Share with DB/Backend

### Indexes (recommended)
- `ratings(user_id)`
- `ratings(movie_id)`
- `ratings(user_id, movie_id)` (composite)
- `movies(movie_id)` (PK/index)
- optional:
  - `watch_events(user_id, timestamp)`
  - `watch_events(user_id, movie_id)`
  - `friends(user_id_1, user_id_2, status)`

### Security note
- DB credentials must not be committed to git
- Use `.env` + secrets + credential rotation if leaked

---

## 9) Ownership & Deliverables

**Elif (AI Engineer)**
- Phase 1:
  - `ai_pipeline.md` (this file)
  - `api_contracts.md` (AI sections + formatting)
  - share data needs with DB & Backend (Slack/GitHub comment)
- Phase 2:
  - `ai/data/processed/` (clean dataset)
  - `ai/features/feature_pipeline.py`
  - `ai/models/ibcf.py`
  - `ai/evaluation/offline_metrics.py`
  - `ai/serving/app.py` (mock AI API)