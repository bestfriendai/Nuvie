# api contracts — nuvie

this document defines the api contracts between ios, backend, and ai services. it lists all required data fields for ui components.

---

## overview

nuvie has three parts that work together:

**ios app (swift)**
- the frontend users interact with
- sends requests to backend api
- displays data to users

**backend api (fastapi)**
- handles business logic
- manages authentication
- talks to database
- talks to ai service

**ai service (fastapi)**
- generates recommendations
- creates explanations
- serves trained models

**how they connect**
- ios app sends http requests to backend api
- backend api sends requests to ai service (internal)
- all responses use json format

---

## environments & base urls

**backend**
- base url: `https://api.nuvie.app` (prod)
- base url: `http://localhost:8000` (dev)

**ai service (internal)**
- base url: `http://ai-service:8000` (docker)
- base url: `http://localhost:9000` (dev)

---

## authentication

### headers (backend)
all authenticated requests must include:

```text
Authorization: Bearer {access_token}
token expires after 24 hours. refresh endpoint available.
internal auth (backend → ai)
backend calls to ai service must include:
X-Internal-Token: {internal_secret}
error responses (global)
all endpoints return errors like this:
{
  "error": {
    "code": "MOVIE_NOT_FOUND",
    "message": "Movie with ID 123 not found",
    "details": {}
  }
}
common error codes
AUTHENTICATION_REQUIRED - not logged in
MOVIE_NOT_FOUND - movie doesn't exist
USER_NOT_FOUND - user doesn't exist
RATING_INVALID - rating out of range
FRIEND_REQUEST_EXISTS - request already sent
RATE_LIMIT_EXCEEDED - too many requests
INTERNAL_ERROR - unexpected error
response pagination (backend)
lists support pagination.
query parameters

limit (integer, default: 20, max: 100)
offset (integer, default: 0)
response format
{
  "items": [],
  "total_count": 150,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
authentication api (ios → backend)
endpoint: post /auth/login
request
{
  "provider": "apple",
  "token": "apple_id_token",
  "user_identifier": "user_apple_id"
}
response
{
  "access_token": "jwt_token_string",
  "user": {
    "user_id": 123,
    "name": "John Doe",
    "avatar_url": "https://...",
    "email": "user@example.com"
  }
}
required fields for ui
user.user_id (integer) - user id
user.name (string) - display name
user.avatar_url (string, optional) - profile picture
movie data (ios → backend)
endpoint: get /movies/{movie_id}
response
{
  "movie_id": 1,
  "title": "The Matrix",
  "genres": ["Sci-Fi", "Action"],
  "poster_url": "https://image.tmdb.org/t/p/w500/...",
  "overview": "A computer hacker learns...",
  "release_date": "1999-03-31",
  "tmdb_id": 603,
  "rating": 4.5,
  "rating_count": 1250,
  "user_rating": 5,
  "ai_score": 94,
  "social_score": 89,
  "in_watchlist": false,
  "watch_status": null
}
required fields for ui
movie_id (integer)
title (string)
genres (array)
poster_url (string, optional)
overview (string, optional)
release_date (string) - date "yyyy-mm-dd"
rating (float, optional) - average rating 1-5
rating_count (integer, optional)
user_rating (integer, optional) - 1-5
ai_score (integer, optional) - 0-100
social_score (integer, optional) - 0-100
in_watchlist (boolean)
watch_status (string, optional) - started, completed, paused, or null
recommendation feed (ios → backend)
endpoint: get /feed/recommendations
query parameters
limit (integer, default: 20)
offset (integer, default: 0)
response
{
  "recommendations": [
    {
      "movie_id": 1,
      "title": "The Matrix",
      "poster_url": "https://...",
      "genres": ["Sci-Fi", "Action"],
      "release_date": "1999-03-31",
      "rating": 4.5,
      "ai_score": 94,
      "social_score": 89,
      "explanation": {
        "primary_reason": "genre_match",
        "confidence": 0.94,
        "factors": [
          {
            "type": "genre_match",
            "weight": 0.4,
            "value": 94,
            "payload": { "genres": ["Sci-Fi", "Action"] },
            "description": "Strong match with your Sci-Fi preferences"
          },
          {
            "type": "friend_activity",
            "weight": 0.6,
            "value": 3,
            "payload": { "friend_user_ids": [2, 8, 19] },
            "description": "3 friends rated this highly"
          }
        ]
      },
      "friend_ratings": {
        "count": 3,
        "average": 5.0,
        "friends": [
          {
            "user_id": 2,
            "name": "Sarah",
            "avatar_url": "https://...",
            "rating": 5
          }
        ]
      }
    }
  ],
  "last_updated": "2024-01-15T10:30:00Z",
  "total_count": 50
}
required fields for ui
recommendations[] - list of movies
all movie fields shown above (subset ok for feed)
explanation
primary_reason (string)
confidence (float 0-1)
factors[] (array)
friend_ratings
count (integer)
average (float)
friends[] (array)
friends & social (ios → backend)
endpoint: get /friends
response
{
  "friends": [
    {
      "user_id": 2,
      "name": "Sarah Chen",
      "avatar_url": "https://...",
      "favorite_genres": ["Drama", "Romance", "Sci-Fi"],
      "mutual_friends": 8,
      "status": "accepted",
      "watched_count": 42,
      "last_active": "2024-01-15T10:30:00Z"
    }
  ],
  "suggestions": [
    {
      "user_id": 5,
      "name": "David Park",
      "avatar_url": "https://...",
      "mutual_friends": 5,
      "shared_genres": ["Sci-Fi", "Action"],
      "match_score": 87
    }
  ]
}
required fields for ui
friends[]
user_id (integer)
name (string)
avatar_url (string, optional)
favorite_genres (array, optional)
mutual_friends (integer)
status (string) - accepted, pending, blocked
watched_count (integer, optional)
last_active (string, optional)
suggestions[]
user_id (integer)
name (string)
avatar_url (string, optional)
mutual_friends (integer)
shared_genres (array)
match_score (integer 0-100)
activity feed (ios → backend)
endpoint: get /feed/activities
query parameters
limit (integer, default: 20)
offset (integer, default: 0)
type (string, optional) - rating, review, watched, started, watchlist
response
{
  "activities": [
    {
      "activity_id": 1,
      "user_id": 2,
      "user_name": "Sarah Chen",
      "user_avatar": "https://...",
      "movie_id": 1,
      "movie_title": "The Matrix",
      "movie_poster": "https://...",
      "type": "rating",
      "rating": 5,
      "comment": null,
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "total_count": 50
}
required fields for ui
activities[]
activity_id (integer)
user_id (integer)
user_name (string)
user_avatar (string, optional)
movie_id (integer)
movie_title (string)
movie_poster (string, optional)
type (string) - rating, review, watched, started, watchlist
rating (integer, optional)
comment (string, optional)
timestamp (string)
ratings & reviews (ios → backend)
endpoint: post /movies/{movie_id}/rate
request
{
  "rating": 5,
  "comment": "Amazing movie!",
  "is_review": true
}
response
{
  "success": true,
  "rating": {
    "user_id": 1,
    "movie_id": 1,
    "rating": 5,
    "comment": "Amazing movie!",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
endpoint: get /movies/{movie_id}/reviews
response
{
  "reviews": [
    {
      "review_id": 1,
      "user_id": 2,
      "user_name": "Sarah Chen",
      "user_avatar": "https://...",
      "movie_id": 1,
      "rating": 5,
      "comment": "Mind-blowing!",
      "timestamp": "2024-01-15T10:30:00Z",
      "likes": 12,
      "user_liked": false
    }
  ],
  "total_count": 25
}
required fields for ui
reviews[]
review_id (integer, optional)
user_id (integer)
user_name (string)
user_avatar (string, optional)
movie_id (integer)
rating (integer) - 1-5 stars
comment (string, optional)
timestamp (string)
likes (integer)
user_liked (boolean)
search & discovery (ios → backend)
endpoint: get /movies/search
query parameters
q (string)
genres (string, optional) - comma-separated genres
limit (integer, default: 20)
offset (integer, default: 0)
response
{
  "movies": [
    {
      "movie_id": 1,
      "title": "The Matrix",
      "poster_url": "https://...",
      "genres": ["Sci-Fi", "Action"],
      "release_date": "1999-03-31",
      "rating": 4.5,
      "ai_score": 94
    }
  ],
  "total_count": 150
}
required fields for ui
same as movie data (subset ok)
sorted by relevance
user profile (ios → backend)
endpoint: get /users/{user_id}
response
{
  "user_id": 1,
  "name": "Alex Johnson",
  "avatar_url": "https://...",
  "bio": "Movie enthusiast",
  "favorite_genres": ["Sci-Fi", "Action", "Thriller"],
  "watched_count": 42,
  "friends_count": 12,
  "ratings_count": 38,
  "favorites_count": 18,
  "stats": {
    "average_rating_given": 4.2,
    "most_watched_genre": "Sci-Fi",
    "total_watch_time": 1200
  }
}
required fields for ui
user_id (integer)
name (string)
avatar_url (string, optional)
bio (string, optional)
favorite_genres (array, optional)
watched_count (integer)
friends_count (integer)
ratings_count (integer, optional)
favorites_count (integer, optional)
stats (object, optional)
ai explanation data (ios → backend)
endpoint: get /movies/{movie_id}/explanation
response
{
  "movie_id": 1,
  "ai_score": 94,
  "explanation": {
    "primary_reason": "genre_match",
    "confidence": 0.94,
    "factors": [
      {
        "type": "genre_match",
        "weight": 0.4,
        "value": 94,
        "payload": { "genres": ["Sci-Fi", "Action"] },
        "description": "Strong match with your Sci-Fi preferences"
      }
    ]
  },
  "social_signals": {
    "friend_ratings_count": 3,
    "friend_ratings_avg": 5.0,
    "friend_watch_count": 5,
    "mutual_friends_watched": 2
  }
}
required fields for ui
ai_score (integer) - overall score 0-100
explanation
primary_reason (string)
confidence (float) - 0-1
factors[]
type (string)
weight (float)
value (varies)
payload (object)
description (string)
social_signals
friend_ratings_count (integer)
friend_ratings_avg (float)
friend_watch_count (integer)
mutual_friends_watched (integer)
watchlist & watch events (ios → backend)
endpoint: post /movies/{movie_id}/watchlist
request
{
  "action": "add"
}
endpoint: post /movies/{movie_id}/watch
request
{
  "event_type": "started",
  "progress_percent": 25
}
backend ↔ ai service contracts (internal)
this section defines the internal contract between backend api and ai service.
ios never calls these endpoints directly.
ai reason type enum (shared)
allowed factor types
genre_match
because_you_rated
similar_users
friend_activity
trending
popular
rules
type must be one of the above strings.
payload must be small and safe for ui.
description may be generated by ai or backend (preferred for i18n).
recommendation score mapping (standard)
ai service returns score as float [0, 1]
backend maps to feed field ai_score = round(score * 100) (0-100)
endpoint: post /ai/recommend
headers
X-Internal-Token: {internal_secret}
request
{
  "request_id": "uuid-1234",
  "user_id": 123,
  "limit": 20,
  "offset": 0,
  "exclude_movie_ids": [10, 20, 30],
  "context": {
    "use_social": true,
    "seed_movie_ids": [1, 2],
    "locale": "tr-TR",
    "time": "2025-12-13T10:30:00Z"
  }
}
response
{
  "request_id": "uuid-1234",
  "user_id": 123,
  "model": {
    "name": "ibcf",
    "version": "v1",
    "trained_at": "2025-12-10T00:00:00Z"
  },
  "generated_at": "2025-12-13T10:30:05Z",
  "ttl_seconds": 900,
  "items": [
    {
      "movie_id": 50,
      "score": 0.8731,
      "rank": 1,
      "explanation": {
        "primary_reason": "genre_match",
        "confidence": 0.82,
        "factors": [
          {
            "type": "genre_match",
            "weight": 0.6,
            "value": 94,
            "payload": { "genres": ["Sci-Fi", "Action"] },
            "description": "Strong match with your Sci-Fi preferences"
          },
          {
            "type": "friend_activity",
            "weight": 0.4,
            "value": 3,
            "payload": { "friend_user_ids": [2, 8, 19] },
            "description": "3 friends rated this highly"
          }
        ]
      }
    }
  ]
}
required behavior
request_id is generated by backend and must be returned unchanged by ai.
exclude_movie_ids must be filtered out.
limit max 50.
cold start: if user has insufficient history, ai should return popular or trending reasons.
endpoint: post /ai/explain
headers
X-Internal-Token: {internal_secret}
request
{
  "request_id": "uuid-999",
  "user_id": 123,
  "movie_id": 50,
  "context": { "use_social": true }
}
response
{
  "request_id": "uuid-999",
  "user_id": 123,
  "movie_id": 50,
  "ai_score": 94,
  "explanation": {
    "primary_reason": "because_you_rated",
    "confidence": 0.77,
    "factors": [
      {
        "type": "because_you_rated",
        "weight": 0.7,
        "value": 2,
        "payload": { "seed_movie_ids": [1, 2] },
        "description": "Because you liked similar movies"
      }
    ]
  },
  "social_signals": {
    "friend_ratings_count": 3,
    "friend_ratings_avg": 5.0,
    "friend_watch_count": 5
  }
}
ai errors (internal)
ai service must use the global error format.
common ai error codes

INVALID_REQUEST
USER_NOT_FOUND
MODEL_NOT_READY
TIMEOUT
INTERNAL_ERROR
caching & ttl (backend)
backend may cache ai results in database (example: recommendation_feed) using ttl_seconds.
suggested behavior

if cached recs exist and are not expired: return cached
else call /ai/recommend, store results, return
data transformation notes
genre parsing
database: pipe-separated string "sci-fi|action|thriller"
api: return as array ["sci-fi", "action", "thriller"]
ios: expects array
date formatting
timestamps: iso 8601 format "2024-01-15T10:30:00Z" (uppercase T and Z)
ios: converts to local time
display: "2 hours ago" or date
image urls
poster urls: full urls only
fallback: placeholder if null
sizes: w200, w500, original
optional fields
use null explicitly (don't omit)
ios: handles null gracefully
ios integration notes
use codable for json parsing
cache with core data for offline
handle errors with retry
show loading states
pagination for infinite scroll
cache images locally
