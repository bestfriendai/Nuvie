# ios architecture — nuvie

this document describes the ios app structure, main screens, navigation, and explainable ui design rules.

---

## main screens

the nuvie ios app has four main screens. users navigate between them using tabs at the bottom.

### 1. login/authentication screen

**purpose**: users sign in here.

**key features**:
- sign in with apple
- first-time user setup
- optional profile info (favorite genres, bio)
- terms and privacy acceptance

**navigation**:
- after login → home screen
- skip setup → home screen (can finish later)

**data requirements**:
- user auth token
- user profile (user_id, name, avatar)
- recommendation feed (if ready)

---

### 2. home screen (feed)

**purpose**: shows personalized movie recommendations.

**key features**:
- **ai recommendations**: movies picked for you
  - shows ai score (0-100%)
  - shows social match percentage
  - shows why it's recommended
  - swipe or grid view
  
- **trending now**: popular movies
  - based on recent ratings
  - updates in real-time
  
- **friend activity**: what friends are doing
  - friend ratings and reviews
  - watchlist additions
  - tap to see details
  
- **quick actions**:
  - search movies
  - filter by genre
  - refresh recommendations

**navigation**:
- tap movie card → movie detail screen
- tap friend activity → movie detail or social screen
- bottom tabs to other screens

**data requirements**:
- recommendation feed
- movie info (title, poster, genres, overview, date)
- ai scores and social scores
- friend activities
- user's ratings

---

### 3. discover screen

**purpose**: browse and search movies.

**key features**:
- **search bar**: search by title, director, or description
- **genre filters**: filter by genre
- **movie grid**: shows search results
- **ai notice**: tells you results are personalized
- **movie cards**: shows poster, title, year, genres, ratings

**navigation**:
- tap movie card → movie detail screen
- bottom tabs to other screens

**data requirements**:
- movie list
- search results
- genre filtering
- movie metadata

---

### 4. movie detail screen

**purpose**: full movie info and actions.

**key features**:
- **hero section**:
  - large poster
  - title, year, genres
  - ratings and scores
  
- **action buttons**:
  - rate movie (1-5 stars)
  - add to watchlist
  - recommend to friend
  - share movie
  
- **overview section**:
  - movie description
  - director and cast (if available)
  - release date and duration
  
- **explainable ai section**:
  - "why this movie?" card
  - shows reasoning
  - visual badges
  
- **reviews section**:
  - friend reviews first
  - community reviews
  - user's own review
  - like and comment

**navigation**:
- back button → previous screen
- recommend button → friend picker
- tap friend review → social screen
- bottom tabs

**data requirements**:
- full movie data
- user's rating
- reviews
- friend ratings
- ai explanation
- watch status

---

### 5. social screen (social feed)

**purpose**: see friend activity and manage friends.

**key features**:
- **suggested friends**: ai suggests friends
  - based on genre preferences
  - shows mutual friends
  - shows shared genres
  - follow/add button
  
- **activity feed**: friend activities
  - shows what friends did
  - shows avatars and posters
  - types: ratings, reviews, watched, watchlist
  - pull to refresh
  
- **friend profile**: tap to see
  - watched movies count
  - favorite genres
  - mutual friends
  - shared interests

**navigation**:
- tap friend → friend profile
- tap activity → movie detail screen
- bottom tabs

**data requirements**:
- friends list
- friend suggestions
- friend activities
- friend profiles
- mutual friends count

---

## navigation structure

users start at the login screen. after login, they see the main tab bar with four tabs: home, discover, social, and profile.

from any tab, users can tap a movie card to see the movie detail screen. the movie detail screen can be opened from home, discover, or social screens.

the tab bar stays visible at the bottom so users can switch between screens anytime.

**navigation patterns**:
- **tab bar**: main navigation (always visible)
  - home: main feed
  - discover: browse movies
  - social: friend activities
  - profile: user settings
- **push navigation**: movie details (can go back)
- **modal/sheet**: friend picker, share dialogs
- **deep linking**: direct links to movies or friends

---

## explainable ui design rules

### "why recommended?" feature

we show users why movies are recommended. this builds trust. it's what makes nuvie different.

#### design principles:

1. **always show reasoning**
   - every recommendation has an explanation
   - no hidden reasons
   - badges on movie cards

2. **multi-factor explanations**
   - combine different signals:
     - genre match: "you love sci-fi"
     - friend activity: "3 friends rated this 5 stars"
     - similar movies: "like movies you rated highly"
     - ai score: "94% match"

3. **visual hierarchy**
   - main reason is biggest
   - other reasons are smaller
   - use colors:
     - genre match (amber/yellow)
     - friend activity (blue)
     - ai score (purple/amber)
     - similar movies (green)

4. **explanation card**
   - on movie detail screen
   - expandable card
   - shows breakdown:
     ```
     why you'll love this:
     • 94% genre match (sci-fi, action)
     • 3 friends rated 5 stars
     • similar to "the matrix" (you rated 5 stars)
     • high ai confidence
     ```

5. **contextual explanations**
   - feed: short badge
   - movie detail: full card
   - friend recs: "your friend sarah loves this"

6. **social proof**
   - show friend activity
   - "x friends watched this" badges
   - friend avatars on cards
   - highlight friend ratings

7. **transparency**
   - show confidence levels
   - say when data is limited
   - explain when recs update

#### implementation:

**on movie cards**:
- show main reason badge
- show ai score badge
- show genre match if relevant

**on movie detail**:
- expandable "why recommended?" section
- breakdown with icons
- progress bars for match scores
- friend activity timeline

**visual design**:
- gradients for ai scores
- blue for friend stuff
- green for matches
- icons for different types

#### data requirements:

**from backend api**:
- explanation_reason: main reason
- explanation_factors: list of factors
  - type: genre_match, friend_activity, similar_movies, ai_score
  - value: number or text
  - confidence: 0-100
- friend_ratings_count: how many friends rated
- friend_ratings_avg: average friend rating
- genre_match_percentage: genre score
- similar_movies: list of similar movies

**from ai service**:
- ai_score: 0-100 confidence
- explanation_text: readable explanation
- feature_importance: what mattered most

---

## architecture patterns

### mvvm (model-view-viewmodel)

**models**:
- movie, user, friend, rating, activity
- maps directly from api

**viewmodels**:
- feedviewmodel: manages feed state
- moviedetailviewmodel: handles movie data
- friendsviewmodel: manages friends
- profileviewmodel: user profile

**views**:
- swiftui views for each screen
- reusable components

### data flow

```
view → viewmodel → network → backend api
                ↓
            local cache
                ↓
            view updates
```

---

## key components

### reusable ui components

1. **moviecard**
   - poster image
   - title, year, genres
   - rating badges
   - explanation badges

2. **activitycard**
   - friend avatar
   - activity icon
   - movie poster
   - timestamp

3. **explanationbadge**
   - icon and text
   - color by type
   - tap to expand

4. **ratingstars**
   - 1-5 star rating
   - hover states
   - saves to backend

---

## state management

- swiftui state: local ui state
- combine: reactive data
- core data: local cache
- userdefaults: preferences

---

## screen specifications

### screen sizes
- iphone se (smallest)
- iphone 14/15 (standard)
- iphone 14/15 pro max (largest)
- ipad (future)

### dark mode
- dark theme
- amber/yellow accents
- high contrast

---

## future enhancements

- push notifications
- watch together
- movie groups
- better search
- offline mode
