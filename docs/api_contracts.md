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

**how they connect:**
- ios app sends http requests to backend api
- backend api sends requests to ai service
- all responses use json format

---

## authentication

### endpoint: `post /auth/login`

**request**:
```json
{
  "provider": "apple",
  "token": "apple_id_token",
  "user_identifier": "user_apple_id"
}
```

**response**:
```json
{
  "access_token": "jwt_token_string",
  "user": {
    "user_id": 123,
    "name": "John Doe",
    "avatar_url": "https://...",
    "email": "user@example.com"
  }
}
```

**required fields for ui**:
- user_id (integer) - user id
- name (string) - display name
- avatar_url (string, optional) - profile picture

---

## movie data

### endpoint: `get /movies/{movie_id}`

**response**:
```json
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
```

**required fields for ui**:
- movie_id (integer) - movie id
- title (string) - movie title
- genres (array) - genre list
- poster_url (string, optional) - poster image
- overview (string, optional) - description
- release_date (string) - date "yyyy-mm-dd"
- rating (float, optional) - average rating 1-5
- rating_count (integer, optional) - number of ratings
- user_rating (integer, optional) - user's rating 1-5
- ai_score (integer, optional) - ai score 0-100
- social_score (integer, optional) - social score 0-100
- in_watchlist (boolean) - in watchlist?
- watch_status (string, optional) - started, completed, paused, or null

---

## recommendation feed

### endpoint: `get /feed/recommendations`

**query parameters**:
- limit (integer, default: 20) - how many
- offset (integer, default: 0) - pagination

**response**:
```json
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
        "factors": [
          {
            "type": "genre_match",
            "value": 94,
            "description": "Strong match with your Sci-Fi preferences"
          },
          {
            "type": "friend_activity",
            "value": 3,
            "description": "3 friends rated this 5 stars"
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
```

**required fields for ui**:
- recommendations[] - list of movies
  - all movie fields
  - explanation object
    - primary_reason (string) - main reason
    - factors[] (array) - breakdown
  - friend_ratings object
    - count (integer) - how many friends
    - average (float) - average rating
    - friends[] (array) - friend details

---

## friends & social

### endpoint: `get /friends`

**response**:
```json
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
```

**required fields for ui**:
- friends[] - accepted friends
  - user_id (integer)
  - name (string)
  - avatar_url (string, optional)
  - favorite_genres (array, optional)
  - mutual_friends (integer) - count
  - status (string) - accepted, pending, or blocked
  - watched_count (integer, optional)
  - last_active (string, optional) - timestamp

- suggestions[] - friend suggestions
  - all friend fields
  - shared_genres (array) - common genres
  - match_score (integer) - compatibility 0-100

---

## activity feed

### endpoint: `get /feed/activities`

**query parameters**:
- limit (integer, default: 20)
- offset (integer, default: 0)
- type (string, optional) - rating, review, watched, or watchlist

**response**:
```json
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
```

**required fields for ui**:
- activities[] - list of activities
  - activity_id (integer) - id
  - user_id (integer) - friend id
  - user_name (string) - friend name
  - user_avatar (string, optional) - avatar url
  - movie_id (integer) - movie id
  - movie_title (string) - movie title
  - movie_poster (string, optional) - poster url
  - type (string) - rating, review, watched, started, or watchlist
  - rating (integer, optional) - rating 1-5
  - comment (string, optional) - review text
  - timestamp (string) - iso timestamp

---

## ratings & reviews

### endpoint: `post /movies/{movie_id}/rate`

**request**:
```json
{
  "rating": 5,
  "comment": "Amazing movie!",
  "is_review": true
}
```

**response**:
```json
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
```

### endpoint: `get /movies/{movie_id}/reviews`

**response**:
```json
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
```

**required fields for ui**:
- reviews[] - list of reviews
  - review_id (integer, optional)
  - user_id (integer)
  - user_name (string)
  - user_avatar (string, optional)
  - movie_id (integer)
  - rating (integer) - 1-5 stars
  - comment (string, optional) - review text
  - timestamp (string) - iso timestamp
  - likes (integer) - like count
  - user_liked (boolean) - did user like?

---

## search & discovery

### endpoint: `get /movies/search`

**query parameters**:
- q (string) - search query
- genres (string, optional) - comma-separated genres
- limit (integer, default: 20)
- offset (integer, default: 0)

**response**:
```json
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
```

**required fields for ui**:
- same as movie data
- sorted by relevance

---

## user profile

### endpoint: `get /users/{user_id}`

**response**:
```json
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
```

**required fields for ui**:
- user_id (integer)
- name (string)
- avatar_url (string, optional)
- bio (string, optional)
- favorite_genres (array, optional)
- watched_count (integer)
- friends_count (integer)
- ratings_count (integer, optional)
- favorites_count (integer, optional)
- stats (object, optional) - extra stats

---

## ai explanation data

### endpoint: `get /movies/{movie_id}/explanation`

**response**:
```json
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
```

**required fields for ui**:
- ai_score (integer) - overall score 0-100
- explanation object
  - primary_reason (string) - main factor
  - confidence (float) - 0-1 score
  - factors[] - list of factors
    - type (string) - factor type
    - weight (float) - importance 0-1
    - value (varies) - factor value
    - description (string) - readable text
- social_signals object - friend activity metrics

---

## watchlist & watch events

### endpoint: `post /movies/{movie_id}/watchlist`

**request**:
```json
{
  "action": "add"
}
```

### endpoint: `post /movies/{movie_id}/watch`

**request**:
```json
{
  "event_type": "started",
  "progress_percent": 25
}
```

---

## data transformation notes

### genre parsing
- database: pipe-separated string "sci-fi|action|thriller"
- api: return as array ["sci-fi", "action", "thriller"]
- ios: expects array

### date formatting
- timestamps: iso 8601 format "2024-01-15t10:30:00z"
- ios: converts to local time
- display: "2 hours ago" or date

### image urls
- poster urls: full urls only
- fallback: placeholder if null
- sizes: w200, w500, original

### optional fields
- use null explicitly (don't omit)
- ios: handles null gracefully

---

## error responses

all endpoints return errors like this:

```json
{
  "error": {
    "code": "MOVIE_NOT_FOUND",
    "message": "Movie with ID 123 not found",
    "details": {}
  }
}
```

**common error codes**:
- authentication_required - not logged in
- movie_not_found - movie doesn't exist
- rating_invalid - rating out of range
- friend_request_exists - request already sent
- rate_limit_exceeded - too many requests

---

## response pagination

lists support pagination:

**query parameters**:
- limit (integer, default: 20, max: 100)
- offset (integer, default: 0)

**response format**:
```json
{
  "items": [...],
  "total_count": 150,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
```

---

## authentication headers

all authenticated requests need:

```
Authorization: Bearer {access_token}
```

token expires after 24 hours. refresh endpoint available.

---

## ios integration notes

- use codable for json parsing
- cache with core data for offline
- handle errors with retry
- show loading states
- pagination for infinite scroll
- cache images locally
