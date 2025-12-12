# system architecture — nuvie

this document describes the system architecture, design philosophy, and ux principles.

---

## ux principles (design goals)

### 1. transparency & trust

**principle**: users should understand why content is recommended.

**implementation**:
- every recommendation has an explanation
- ai decisions are clear, not hidden
- show confidence levels
- show friend activity
- let users control their data

**why**: builds trust and increases engagement.

---

### 2. social-first discovery

**principle**: social connections help more than algorithms alone.

**implementation**:
- show friend activity prominently
- boost recs by friend preferences
- easy sharing to friends
- show "3 friends loved this" badges
- filter by friends

**why**: people trust friends more than algorithms. social signals build community.

---

### 3. personalization without isolation

**principle**: personalize but keep discovery diverse.

**implementation**:
- mix personalized and trending content
- suggest "outside your comfort zone" movies
- show diverse genres
- let users explore
- mix ai recs with community trends

**why**: prevents filter bubbles. keeps experience fresh.

---

### 4. respectful of user time

**principle**: make interactions quick and easy.

**implementation**:
- one-tap actions
- swipeable interfaces
- smart defaults
- minimal onboarding
- fast loading
- offline support

**why**: users have limited attention. every second counts.

---

### 5. progressive disclosure

**principle**: show essentials first, details on demand.

**implementation**:
- movie cards show key info
- details on tap
- expandable sections
- collapsible lists
- hide settings until needed

**why**: reduces cognitive load. keeps interface clean.

---

### 6. delight through details

**principle**: small thoughtful touches matter.

**implementation**:
- smooth animations
- contextual interactions
- personalized messages
- celebration moments
- beautiful design

**why**: emotional connection drives engagement.

---

### 7. data ownership & privacy

**principle**: users control their data.

**implementation**:
- clear privacy policy
- users can export data
- opt-out options
- transparent about data usage
- secure auth (sign in with apple)

**why**: trust is essential. users must feel safe.

---

### 8. accessibility & inclusion

**principle**: usable by everyone.

**implementation**:
- high contrast design
- screen reader support
- large touch targets (44x44pt min)
- clear typography
- color-blind friendly
- multiple languages (future)

**why**: inclusive design helps everyone.

---

### 9. continuous learning

**principle**: system improves with feedback.

**implementation**:
- learn from ratings and watch behavior
- adapt recommendations
- retrain models
- a/b testing
- feedback loops

**why**: static systems get stale. continuous improvement keeps recs relevant.

---

### 10. mobile-first, cross-platform ready

**principle**: optimize for mobile but support growth.

**implementation**:
- native ios app
- responsive design
- touch-optimized
- offline-first
- api-first design

**why**: mobile is primary. architecture should support growth.

---

## system architecture overview

nuvie has three main parts that work together:

**ios app (swift)**
- views: the screens users see
- viewmodels: handles business logic
- models: data structures
- network layer: talks to backend

**backend api (fastapi)**
- handles authentication
- manages business logic
- accesses database
- talks to ai service

**ai service (fastapi)**
- generates recommendations
- creates explanations
- serves trained models
- handles training

**database (postgresql)**
- stores users
- stores movies
- stores ratings
- stores friends
- stores watch events

**how they connect:**
- ios app sends requests to backend api over https
- backend api talks to ai service for recommendations
- backend api reads and writes to database
- everything uses json for data

---

## data flow

### recommendation flow

1. user opens feed screen
   - ios app requests: get /feed/recommendations

2. backend api receives request
   - validates auth
   - checks cache (redis)
   - if miss, calls ai service

3. ai service processes
   - loads user profile
   - runs algorithms (ibcf, neural cf)
   - generates explanations
   - returns ranked list

4. backend api formats response
   - adds friend activity
   - adds social signals
   - formats for ios
   - caches in redis

5. ios app displays
   - parses json
   - renders movie cards
   - caches locally

### rating flow

1. user rates movie (1-5 stars)
   - ios app sends: post /movies/{movie_id}/rate

2. backend api processes
   - validates rating
   - stores in ratings table
   - updates user profile
   - triggers friend notification

3. ai service updates (async)
   - incorporates new rating
   - retrains model (scheduled)
   - updates explanations

4. feedback to user
   - ios shows confirmation
   - updates ui
   - refreshes recs (optional)

---

## component architecture

### backend api structure

```
backend/
├── app/
│   ├── main.py          # FastAPI app entry
│   ├── auth.py          # Authentication routes
│   ├── feed.py          # Feed & recommendations
│   ├── movies.py        # Movie CRUD operations
│   ├── friends.py       # Friend management
│   └── ratings.py       # Rating & review routes
├── models/
│   ├── user.py          # User ORM model
│   ├── movie.py         # Movie ORM model
│   └── rating.py        # Rating ORM model
├── schemas/
│   ├── user.py          # Pydantic schemas
│   └── movie.py         # Request/response schemas
└── db/
    └── connection.py    # Database connection
```

### ai service structure

```
aii/
├── serving/
│   └── app.py           # AI API service
├── models/
│   ├── ibcf.py          # Item-based CF
│   └── neural_cf.py     # Neural collaborative filtering
├── explanations/
│   └── reason_generator.py  # Explanation logic
└── training/
    └── train_baseline.py    # Model training
```

### ios app structure

```
NuvieApp/
├── Views/
│   ├── LoginView.swift
│   ├── FeedView.swift
│   ├── MovieDetailView.swift
│   └── FriendsView.swift
├── ViewModels/
│   ├── FeedViewModel.swift
│   ├── MovieDetailViewModel.swift
│   └── FriendsViewModel.swift
├── Models/
│   ├── Movie.swift
│   ├── User.swift
│   └── Activity.swift
├── Network/
│   ├── APIClient.swift
│   └── Endpoints.swift
└── Components/
    ├── MovieCard.swift
    ├── ActivityCard.swift
    └── ExplanationBadge.swift
```

---

## security architecture

### authentication flow

1. user signs in with apple
   - ios app gets apple id token
   - sends to backend: post /auth/login

2. backend validates token
   - verifies with apple
   - creates/updates user
   - generates jwt token
   - returns token to ios

3. ios app stores token
   - secure keychain storage
   - includes in all requests: authorization: bearer {token}

4. token refresh
   - tokens expire after 24 hours
   - refresh endpoint available
   - auto refresh on 401

### data privacy

- user data: encrypted at rest
- api: https only
- token storage: ios keychain
- pii: minimal collection (name, email only)
- gdpr: export and deletion endpoints

---

## performance considerations

### caching strategy

- redis cache:
  - recommendation feeds (5 min ttl)
  - movie metadata (1 hour ttl)
  - user profiles (15 min ttl)

- ios local cache:
  - core data for offline
  - image caching
  - recent recs (24 hour ttl)

### database optimization

- indexes:
  - ratings(user_id, movie_id)
  - movies(movie_id)
  - friends(user_id_1, user_id_2)

- query optimization:
  - pagination
  - eager loading
  - connection pooling

### api performance

- response times:
  - feed recs: < 500ms (cached) or < 2s (uncached)
  - movie details: < 200ms
  - search: < 300ms

- rate limiting:
  - 100 requests/minute per user
  - 1000 requests/hour per user
  - burst: 20 requests/10 seconds

---

## scalability

### horizontal scaling

- backend api: stateless, scales horizontally
- ai service: stateless, multiple instances
- database: read replicas
- redis: cluster mode

### load balancing

- api gateway: routes requests
- health checks: auto failover
- cdn: static assets

---

## deployment architecture

### development environment

- local: docker compose
  - backend api: localhost:8000
  - ai service: localhost:9000
  - postgresql: localhost:5432
  - redis: localhost:6379

### production environment

- backend api: cloud provider
- ai service: separate service, auto-scaling
- database: neon (managed postgresql)
- redis: upstash (managed redis)
- cdn: cloudflare
- ci/cd: github actions

---

## monitoring & analytics

### metrics tracked

- user engagement:
  - daily active users
  - recommendation click rate
  - rating submission rate
  - friend interaction rate

- system performance:
  - api response times
  - error rates
  - database query performance
  - cache hit rates

- ai model performance:
  - recommendation accuracy (rmse, mae)
  - user satisfaction
  - explanation quality

### logging

- structured logging: json format
- log levels: debug, info, warning, error
- centralized logging: cloud service
- error tracking: sentry or similar

---

## future enhancements

### phase 2-5 roadmap

- phase 2: data & baseline
  - movielens data integration
  - ibcf baseline model
  - mock recommendation endpoints

- phase 3: full integration
  - ios → backend → ai data flow
  - live recommendation feed
  - real-time friend activity

- phase 4: social ai
  - friend-aware reranking
  - social explanations
  - group recommendations

- phase 5: continuous learning
  - feedback collection
  - automatic model retraining
  - a/b testing framework

### long-term vision

- multi-platform: web app, android app
- advanced features:
  - watch together
  - movie groups
  - better search
  - personalized news
- community features:
  - movie clubs
  - discussion forums
  - event planning

---

## references

- database schema: see docs/database_schema.md
- api contracts: see docs/api_contracts.md
- ios architecture: see docs/ios_architecture.md
- ai pipeline: see docs/ai_pipeline.md
