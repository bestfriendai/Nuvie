# Phase 2 Team Task Breakdown

## Öykü

### 1. Feed Screen Design
- **File**: `Views/FeedView.swift`
- **Status**: Complete
- **Description**: Movie cards layout with all sections (hero, recommended, trending, activity)

### 2. Movie Card UI 
- **File**: `Components/MovieCard.swift`
- **Status**: Complete
- **Description**: Poster, score, reason badges - standard and compact variants

### 3. Loading States 
- **File**: `Components/SkeletonView.swift`
- **Status**: Complete
- **Description**: Skeleton UI with shimmer animations

### 4. Empty States 
- **File**: `Components/EmptyStateView.swift`
- **Status**: Complete
- **Description**: No data UX for all scenarios

---

## Can

### 1. Create iOS Folder Structure
- Already created (shared infrastructure)
- **Status**: Complete

### 2. Define API Headers
- **File**: `Network/APIClient.swift`
- **Status**: TODO
- **Tasks**:
  - Auth headers: `Authorization: Bearer {token}`
  - Content-Type: `application/json`
  - Internal token for Backend → AI: `X-Internal-Token`

### 3. Network Layer Plan
- **File**: `Network/APIClient.swift`
- **Status**: TODO
- **Tasks**:
  - BaseURL configuration (dev/prod)
  - Token storage and refresh flow
  - Request/response handling
  - Error handling

### 4. Endpoint Mapping
- **File**: `Network/Endpoints.swift` (or in APIClient)
- **Status**: TODO
- **Tasks**:
  - `GET /feed/recommendations` → FeedResponse
  - `GET /movies/{movie_id}` → Movie
  - `POST /movies/{movie_id}/rate` → Rating response
  - `GET /feed/activities` → ActivityFeedResponse
  - All endpoints from `/docs/api_contracts.md`

### 5. Connect Mock Feed API
- **File**: `Network/APIClient.swift`
- **Status**: TODO
- **Tasks**:
  - Implement mock/real API client
  - Load fake feed data for testing
  - Connect to `FeedView`

### 6. Decode Feed JSON
- **File**: `Models/` (replace placeholders)
- **Status**: TODO
- **Tasks**:
  - Replace placeholder models with proper Codable implementations
  - Ensure JSON decoding matches API contracts
  - Handle optional fields correctly

### 7. Display Feed
- **File**: `ViewModels/FeedViewModel.swift`
- **Status**: TODO
- **Tasks**:
  - Create ViewModel for FeedView
  - Bind API data to UI
  - Handle loading/error states
  - Connect to `Views/FeedView.swift`

### 8. Handle Errors
- **Files**: `Network/APIClient.swift`, `ViewModels/`
- **Status**: TODO
- **Tasks**:
  - Network error handling
  - Retry logic
  - User-friendly error messages
  - Error state UI (already created in `EmptyStateView.swift`)
