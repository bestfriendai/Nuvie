# movie card ui design — nuvie

this document describes the movie card component design, including poster, scores, and explanation badges.

---

## overview

the movie card is the primary component for displaying movies throughout the app. it shows the poster, ratings, ai scores, and explanation badges.

---

## component variants

the movie card has two variants:

1. **standard card**: full details (title, year, genres visible)
2. **compact card**: poster only (details on hover/tap)

---

## standard card

**use cases**:
- recommended for you section
- discover screen results
- profile watched movies

**dimensions**:
- width: varies by grid (2-4 columns)
- aspect ratio: 2:3 (portrait poster)
- total height: poster + title area (approximately 40pt)

**layout structure**:
```
┌─────────────────┐
│                 │
│   POSTER IMAGE  │  (2:3 aspect ratio)
│                 │
│                 │
└─────────────────┘
┌─────────────────┐
│ Movie Title     │  (title area)
│ 1999 • Sci-Fi   │  (metadata)
└─────────────────┘
```

---

## compact card

**use cases**:
- trending now section
- horizontal scroll lists
- related movies

**dimensions**:
- width: smaller (fits 6 columns)
- aspect ratio: 2:3 (portrait poster)
- height: poster only (no title area)

**layout structure**:
```
┌─────────────────┐
│                 │
│   POSTER IMAGE  │  (2:3 aspect ratio)
│                 │
│                 │
└─────────────────┘
```

---

## poster image

**specifications**:
- fills entire card width
- aspect ratio: 2:3 (portrait)
- rounded corners: 8pt radius
- content mode: aspect fill (crops to fit)
- fallback: placeholder image if poster_url is null

**placeholder**:
- solid color: dark slate (#1e293b)
- icon: film icon (centered, muted)
- text: "no poster" (small, centered)

**loading state**:
- show skeleton/shimmer while loading
- gray background with shimmer animation

---

## overlay (hover/press state)

**when to show**:
- user hovers over card (desktop/web)
- user presses card (mobile)
- user long presses card

**overlay design**:
- dark gradient from bottom to top
- opacity: 80% at bottom, 20% in middle, 0% at top
- appears with fade animation (0.3s)

**overlay content** (bottom of card):
- rating badges
- ai score badge
- social score badge (if available)
- explanation indicator

**badge layout**:
- horizontal row at bottom
- padding: 12pt from edges
- gap between badges: 8pt
- badges: rounded, semi-transparent background

---

## rating badges

**community rating badge**:
- icon: star (filled, yellow)
- text: rating number (e.g., "4.5")
- background: yellow with 20% opacity
- text color: yellow (#fbbf24)
- padding: 4pt horizontal, 4pt vertical
- font size: 11pt

**ai score badge**:
- icon: sparkles (amber)
- text: score percentage (e.g., "94%")
- background: amber with 20% opacity
- text color: amber (#f59e0b)
- padding: 4pt horizontal, 4pt vertical
- font size: 11pt

**social score badge** (if available):
- icon: users (blue)
- text: score percentage (e.g., "89%")
- background: blue with 20% opacity
- text color: blue (#3b82f6)
- padding: 4pt horizontal, 4pt vertical
- font size: 11pt

---

## user rating badge

**location**: top right corner of poster

**design**:
- background: green (#10b981)
- text color: white
- icon: star (filled, white)
- text: rating number (e.g., "5")
- padding: 4pt horizontal, 4pt vertical
- font size: 11pt
- rounded corners: 4pt
- size: approximately 24pt height

**when to show**:
- only if user has rated the movie
- always visible (not just on hover)

---

## quick recommend button

**location**: top left corner of poster

**design**:
- background: amber gradient (from amber-500 to amber-600)
- icon: send icon (white)
- shape: circle
- size: 32pt diameter
- shadow: large shadow for depth

**visibility**:
- opacity: 0 by default
- opacity: 1 on hover/press
- transition: 0.3s fade

**interaction**:
- tap: opens friend selection modal
- shows share dialog

---

## title area (standard cards only)

**layout**:
- below poster image
- margin top: 8pt
- padding: 0 (text flush with card edges)

**title text**:
- font size: 14pt
- font weight: regular
- color: white (#ffffff)
- line height: 1.2
- max lines: 1
- overflow: ellipsis (...)
- truncation: if too long

**metadata text**:
- font size: 12pt
- font weight: regular
- color: muted gray (#94a3b8)
- line height: 1.4
- content: year • genres
- example: "1999 • Sci-Fi, Action"

**spacing**:
- gap between title and metadata: 4pt
- gap between year and genres: 4pt (bullet separator)

---

## explanation indicators

**purpose**: show why movie is recommended

**design options**:

1. **badge on overlay**:
   - small badge in overlay
   - text: "why?" or explanation icon
   - tap to expand explanation

2. **icon indicator**:
   - small icon on card corner
   - color coded by reason type
   - genre match: amber
   - friend activity: blue
   - similar movies: green

3. **explanation badge**:
   - shows primary reason
   - example: "3 friends loved this"
   - appears in overlay with other badges

**recommended approach**:
- show explanation badge in overlay
- include in badge row at bottom
- color coded by type
- tap card to see full explanation on detail screen

---

## interaction states

**default state**:
- poster visible
- title/metadata visible (standard cards)
- user rating badge visible (if rated)
- overlay hidden
- recommend button hidden

**hover/press state**:
- poster scales up slightly (1.05x)
- overlay fades in
- rating badges appear
- recommend button appears
- smooth transitions (0.2-0.3s)

**selected state** (if selectable):
- border: 2pt amber border
- background: slight amber tint
- scale: 1.02x

**loading state**:
- skeleton placeholder
- shimmer animation
- same dimensions as final card

**error state**:
- placeholder image
- error icon (optional)
- retry option (optional)

---

## animations

**card hover**:
- scale: 1.0 → 1.05
- duration: 0.2s
- easing: ease-out

**overlay fade**:
- opacity: 0 → 1
- duration: 0.3s
- easing: ease-in-out

**badge appear**:
- scale: 0.8 → 1.0
- opacity: 0 → 1
- duration: 0.2s
- delay: 0.1s (staggered)

**recommend button**:
- opacity: 0 → 1
- scale: 0.9 → 1.0
- duration: 0.2s

---

## colors

**backgrounds**:
- card background: transparent (shows poster)
- overlay: black gradient (80% → 20% → 0%)
- badge backgrounds: color with 20% opacity

**text**:
- title: white (#ffffff)
- metadata: muted gray (#94a3b8)
- badge text: matches badge color

**badges**:
- rating: yellow (#fbbf24)
- ai score: amber (#f59e0b)
- social score: blue (#3b82f6)
- user rating: green (#10b981)
- recommend button: amber gradient

**borders**:
- none (rounded corners only)

---

## typography

**title**:
- font: system font (sf pro)
- size: 14pt
- weight: regular
- color: white

**metadata**:
- font: system font (sf pro)
- size: 12pt
- weight: regular
- color: muted gray

**badges**:
- font: system font (sf pro)
- size: 11pt
- weight: medium
- color: badge-specific

---

## responsive behavior

**iphone se (small)**:
- 2 columns: cards wider
- title area: same height
- badges: same size

**iphone 14/15 (standard)**:
- 3 columns: cards medium width
- title area: same height
- badges: same size

**iphone 14/15 pro max (large)**:
- 4 columns: cards narrower
- title area: same height
- badges: same size

**ipad (future)**:
- 5-6 columns: cards narrow
- title area: same height
- badges: same size

---

## accessibility

**touch targets**:
- entire card is tappable
- minimum 44pt x 44pt (cards meet this)
- recommend button: 32pt (meets minimum)

**screen readers**:
- card labeled with movie title
- badges announced: "rating 4.5 stars, ai score 94 percent"
- recommend button: "recommend to friend"

**contrast**:
- white text on dark overlay: high contrast
- badge text on semi-transparent: readable
- all text meets wcag aa standards

---

## implementation notes

**swiftui component**:
- moviedardview: main component
- accepts movie model
- accepts compact parameter
- handles all states and interactions

**data model**:
- uses movie struct from api contracts
- required fields: movie_id, title, poster_url, genres
- optional fields: rating, ai_score, social_score, user_rating

**state management**:
- hover state: @state or gesture
- loading state: @state
- error state: @state

**image loading**:
- use asyncimage or custom loader
- cache images locally
- show placeholder while loading
- handle errors gracefully

---

## design references

this design is based on the react moviecard component in the ui ux for nuvie folder. the swiftui implementation should match the visual design and behavior.

key reference:
- components/moviecard.tsx: react implementation
- components/home.tsx: usage in feed screen

