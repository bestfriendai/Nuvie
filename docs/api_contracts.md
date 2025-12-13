# API Contracts — NUVIE

This document defines the API contracts between iOS, Backend, and AI services.
It also lists required data fields for UI components and defines the internal Backend↔AI contract.

---

## Overview

NUVIE has three parts that work together:

**iOS App (Swift)**
- The frontend users interact with
- Sends requests to the Backend API
- Displays data to users

**Backend API (FastAPI)**
- Handles business logic
- Manages authentication
- Talks to the database
- Talks to the AI service

**AI Service (FastAPI)**
- Generates recommendations
- Creates explanations
- Serves trained models

**How they connect**
- iOS app sends HTTP requests to Backend API
- Backend API sends internal requests to AI service
- All responses use JSON

---

## Environments & Base URLs

**Backend**
- Prod: `https://api.nuvie.app`
- Dev: `http://localhost:8000`

**AI Service (internal)**
- Docker: `http://ai-service:8000`
- Dev: `http://localhost:9000`

---

## Authentication

### Backend auth header
All authenticated requests must include:

```text
Authorization: Bearer {access_token}
Token expires after 24 hours
Refresh endpoint available (TBD)
Internal auth (Backend → AI)
Backend calls to AI service must include:
X-Internal-Token: {internal_secret}
Error Responses (Global)
All endpoints return errors like this:
{
  "error": {
    "code": "MOVIE_NOT_FOUND",
    "message": "Movie with ID 123 not found",
    "details": {}
  }
}
Common error codes
AUTHENTICATION_REQUIRED - not logged in
MOVIE_NOT_FOUND - movie doesn't exist
USER_NOT_FOUND - user doesn't exist
RATING_INVALID - rating out of range
FRIEND_REQUEST_EXISTS - request already sent
RATE_LIMIT_EXCEEDED - too many requests
INTERNAL_ERROR - unexpected error
Pagination (Backend)
Lists support pagination.
Query parameters

limit (integer, default: 20, max: 100)
offset (integer, default: 0)
Standard response format
{
  "items": [],
  "total_count": 150,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
iOS → Backend API
Auth
Endpoint: POST /auth/login
Request
{
  "provider": "apple",
  "token": "apple_id_token",
  "user_identifier": "user_apple_id"
}
Response
{
  "access_token": "jwt_token_string",
  "user": {
    "user_id": 123,
    "name": "John Doe",
    "avatar_url": "https://...",
    "email": "user@example.com"
  }
}
Required fields for UI
user.user_id (integer) - user id
user.name (string) - display name
user.avatar_url (string, optional) - profile picture
Movie Data
Endpoint: GET /movies/{movie_id}
Response
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
Required fields for UI
movie_id (integer)
title (string)
genres (array)
poster_url (string, optional)
overview (string, optional)
release_date (string) - yyyy-mm-dd
rating (float, optional) - average rating 1-5
rating_count (integer, optional)
user_rating (integer, optional) - 1-5
ai_score (integer, optional) - 0-100
social_score (integer, optional) - 0-100
in_watchlist (boolean)
watch_status (string, optional) - started, completed, paused, or null
Recommendation Feed
Endpoint: GET /feed/recommendations
Query parameters
limit (integer, default: 20)
offset (integer, default: 0)
Response
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
Required fields for UI
recommendations[]
all movie fields shown above (subset ok for feed)
explanation
primary_reason (string)
confidence (float 0-1)
factors[] (array)
friend_ratings
count (integer)
average (float)
friends[] (array)
Friends & Social
Endpoint: GET /friends
Response
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
Required fields for UI
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
Activity Feed
Endpoint: GET /feed/activities
Query parameters
limit (integer, default: 20)
offset (integer, default: 0)
type (string, optional) - rating, review, watched, started, watchlist
Response
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
Required fields for UI
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
timestamp (string) - ISO 8601
Ratings & Reviews
Endpoint: POST /movies/{movie_id}/rate
Request
{
  "rating": 5,
  "comment": "Amazing movie!",
  "is_review": true
}
Response
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
Endpoint: GET /movies/{movie_id}/reviews
Response
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
Required fields for UI
reviews[]
review_id (integer, optional)
user_id (integer)
user_name (string)
user_avatar (string, optional)
movie_id (integer)
rating (integer) - 1-5
comment (string, optional)
timestamp (string) - ISO 8601
likes (integer)
user_liked (boolean)
Search & Discovery
Endpoint: GET /movies/search
Query parameters
q (string)
genres (string, optional) - comma-separated genres
limit (integer, default: 20)
offset (integer, default: 0)
Response
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
User Profile
Endpoint: GET /users/{user_id}
Response
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
AI Explanation (per-movie)
Endpoint: GET /movies/{movie_id}/explanation
Response
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
Watchlist & Watch Events
Endpoint: POST /movies/{movie_id}/watchlist
Request
{
  "action": "add"
}
Endpoint: POST /movies/{movie_id}/watch
Request
{
  "event_type": "started",
  "progress_percent": 25
}
Backend ↔ AI Service Contracts (Internal)
This section defines the internal contract between Backend API and AI service.
iOS never calls these endpoints directly.
Shared Explainability Types (Reason Types)
Allowed factor types
genre_match
because_you_rated
similar_users
friend_activity
trending
popular
Rules
type must be one of the above strings
payload must be small and UI-safe
description may be generated by AI or Backend (recommended to generate in Backend for i18n)
Score Mapping Standard
AI service returns score as float in [0, 1]
Backend maps: ai_score = round(score * 100) (0-100)
Endpoint: POST /ai/recommend
Headers
X-Internal-Token: {internal_secret}
Request
{
  "request_id": "uuid-1234",
  "user_id": 123,
  "limit": 20,
  "offset": 0,
  "exclude_movie_ids": [10, 20, 30],
  "context": {
    "use_social": true,
    "seed_movie_ids": [1, 2],
    "locale": "en-US",
    "time": "2025-12-13T10:30:00Z"
  }
}
Response
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
Required behavior
request_id is generated by Backend and must be returned unchanged by AI
exclude_movie_ids must be filtered out
limit max 50
Cold start: if user history is insufficient, AI should return items with popular or trending reasons
Endpoint: POST /ai/explain
Headers
X-Internal-Token: {internal_secret}
Request
{
  "request_id": "uuid-999",
  "user_id": 123,
  "movie_id": 50,
  "context": { "use_social": true }
}
Response
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
AI Errors (Internal)
AI service must use the global error format.
Common AI error codes

INVALID_REQUEST
USER_NOT_FOUND
MODEL_NOT_READY
TIMEOUT
INTERNAL_ERROR
Caching & TTL (Backend)
Backend may cache AI results in DB (example: recommendation_feed) using ttl_seconds.
Suggested behavior

If cached recommendations exist and are not expired: return cached
Else call /ai/recommend, store results, return
Data Transformation Notes
Genre parsing
database: pipe-separated string "sci-fi|action|thriller"
api: return as array ["sci-fi", "action", "thriller"]
ios: expects array
Date formatting
timestamps: ISO 8601 format "2024-01-15T10:30:00Z" (uppercase T and Z)
ios: converts to local time
Image URLs
poster urls: full urls only
fallback: placeholder if null
Optional fields
use null explicitly (don't omit)
ios must handle null gracefullyiOS Integration Notes

use Codable for json parsing
cache with core data for offline
handle errors with retry + user-friendly messaging
show loading states
implement pagination for infinite scroll
cache images locally