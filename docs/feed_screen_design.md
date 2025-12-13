# feed screen design — nuvie

this document describes the feed screen design, layout, and component specifications for the ios app.

---

## overview

the feed screen (home screen) is the main screen users see after logging in. it shows personalized movie recommendations, trending content, and friend activity.

---

## screen layout

the feed screen has a vertical scrollable layout with four main sections:

1. hero section (ai recommendations header)
2. recommended for you (personalized movies)
3. trending now (popular movies)
4. friend activity (recent friend actions)

---

## section 1: hero section

**purpose**: introduces ai recommendations and shows user's match scores.

**layout**:
- full-width card with rounded corners
- gradient background (amber/yellow/red tones)
- padding: 24pt on all sides
- border: subtle amber border

**content**:
- icon: sparkles icon in amber (left side)
- title: "ai recommendations" (large text)
- subtitle: "personalized picks based on your taste and social network" (smaller, muted text)
- badges: two small badges showing:
  - ml score: 94% (amber background)
  - social match: 89% (red background)

**visual details**:
- decorative emoji icons in background (low opacity)
- gradient overlay for depth
- rounded corners: 16pt radius

**spacing**:
- section margin bottom: 32pt
- internal padding: 24pt
- gap between elements: 12pt

---

## section 2: recommended for you

**purpose**: shows personalized movie recommendations.

**layout**:
- section header with title and "see all" link
- grid layout: 2 columns on small screens, 3 on medium, 4 on large
- gap between cards: 16pt

**header**:
- title: "recommended for you" (left aligned)
- link: "see all" (right aligned, amber color)
- margin bottom: 16pt

**movie cards**:
- grid: 2 columns (iphone se), 3 columns (iphone 14/15), 4 columns (iphone pro max)
- card aspect ratio: 2:3 (portrait poster)
- each card shows:
  - movie poster image
  - title (below poster)
  - year and genres (small text)
  - rating badges (on hover/overlay)

**card specifications**:
- poster: full width, rounded corners (8pt radius)
- title: 14pt font, single line with ellipsis
- metadata: 12pt font, muted color
- hover state: scale up slightly, show rating badges

---

## section 3: trending now

**purpose**: shows popular movies across the platform.

**layout**:
- section header with trending icon
- horizontal scrollable grid
- 6 columns on large screens, 3 on medium, 2 on small
- gap between cards: 16pt

**header**:
- icon: trending up icon (orange color)
- title: "trending now"
- margin bottom: 16pt

**movie cards**:
- compact version (smaller than recommended)
- same 2:3 aspect ratio
- poster only (no title/metadata on card)
- title appears on hover/tap

**interaction**:
- horizontal scroll
- tap to see movie detail

---

## section 4: friend activity

**purpose**: shows recent activities from friends.

**layout**:
- section header with clock icon
- vertical list of activity cards
- gap between cards: 12pt
- "view all activity" button at bottom

**header**:
- icon: clock icon (blue color)
- title: "friend activity"
- margin bottom: 16pt

**activity cards**:
- full width cards
- rounded corners: 12pt
- padding: 16pt
- background: dark with subtle border

**card content**:
- friend avatar (left, 40pt circle)
- activity text (friend name + action)
- movie poster thumbnail (right, 64pt width)
- timestamp (small, muted)
- rating stars (if rating activity)

**button**:
- "view all activity" link
- full width
- centered text
- dark background
- padding: 12pt vertical

---

## movie card component

**standard size** (recommended section):
- width: varies by grid (2-4 columns)
- aspect ratio: 2:3
- poster: full width, rounded 8pt
- title area: below poster, 40pt height
- total height: poster + title area

**compact size** (trending section):
- width: smaller (6 columns)
- aspect ratio: 2:3
- poster only
- no title visible (shows on hover)

**card elements**:

1. **poster image**:
   - fills card width
   - aspect ratio 2:3
   - rounded corners: 8pt
   - fallback: placeholder if no image

2. **overlay (on hover)**:
   - dark gradient from bottom
   - shows rating badges
   - ai score badge (amber)
   - social score badge (if available)

3. **title** (standard cards only):
   - font size: 14pt
   - single line, ellipsis if long
   - color: white
   - margin top: 8pt

4. **metadata** (standard cards only):
   - year and genres
   - font size: 12pt
   - color: muted gray
   - margin top: 4pt

5. **user rating badge** (if rated):
   - top right corner
   - green background
   - star icon + rating number
   - small size: 24pt height

6. **quick recommend button** (on hover):
   - top left corner
   - amber gradient background
   - send icon
   - circular, 32pt diameter
   - opacity: 0 until hover

**interaction states**:
- default: poster visible, title/metadata below
- hover: overlay appears, badges show, recommend button appears
- tap: navigate to movie detail screen

---

## loading states

**skeleton ui for feed screen**:

1. **hero section skeleton**:
   - rounded rectangle, full width
   - height: 120pt
   - shimmer animation
   - gray background

2. **movie cards skeleton**:
   - grid matches final layout
   - each card: 2:3 aspect ratio
   - rounded corners
   - shimmer animation
   - gray background

3. **activity cards skeleton**:
   - full width rectangles
   - height: 80pt
   - rounded corners
   - shimmer animation
   - gray background

**shimmer effect**:
- subtle gradient animation
- moves left to right
- duration: 1.5 seconds
- repeats continuously

---

## empty states

**no recommendations**:
- icon: sparkles icon (large, muted)
- title: "no recommendations yet"
- message: "rate some movies to get personalized recommendations"
- button: "discover movies" (links to discover screen)

**no trending movies**:
- section hidden if no data
- or show message: "check back later for trending movies"

**no friend activity**:
- icon: users icon (large, muted)
- title: "no friend activity"
- message: "add friends to see what they're watching"
- button: "find friends" (links to social screen)

**empty state design**:
- centered vertically and horizontally
- icon: 64pt, muted color
- title: 18pt, white
- message: 14pt, muted gray
- button: amber gradient, 44pt height
- padding: 32pt all around

---

## spacing and layout

**screen margins**:
- horizontal: 16pt on all devices
- vertical: 24pt top, 16pt bottom

**section spacing**:
- between sections: 32pt
- within sections: 16pt

**card spacing**:
- grid gap: 16pt
- card padding: 0 (content fills card)

**typography**:
- section titles: 20pt, bold, white
- card titles: 14pt, regular, white
- metadata: 12pt, regular, muted gray
- badges: 11pt, regular

---

## colors

**backgrounds**:
- screen background: dark slate (#0f172a)
- card background: darker slate (#1e293b)
- hero section: gradient (amber/yellow/red tones)

**text**:
- primary: white (#ffffff)
- secondary: muted gray (#94a3b8)
- accent: amber (#f59e0b)

**badges**:
- ai score: amber gradient
- social score: red/pink gradient
- user rating: green (#10b981)

**borders**:
- subtle: rgba(amber, 0.2)
- cards: rgba(white, 0.1)

---

## animations

**card hover**:
- scale: 1.0 to 1.05
- duration: 0.2s
- easing: ease-out

**overlay fade**:
- opacity: 0 to 1
- duration: 0.3s
- easing: ease-in-out

**shimmer loading**:
- gradient position: -100% to 100%
- duration: 1.5s
- repeat: infinite
- easing: linear

**section appear**:
- fade in from bottom
- duration: 0.4s
- stagger: 0.1s between sections

---

## responsive behavior

**iphone se (small)**:
- 2 columns for recommended
- 2 columns for trending
- full width activity cards

**iphone 14/15 (standard)**:
- 3 columns for recommended
- 3 columns for trending
- full width activity cards

**iphone 14/15 pro max (large)**:
- 4 columns for recommended
- 6 columns for trending
- full width activity cards

**ipad (future)**:
- 5-6 columns for recommended
- 8 columns for trending
- 2 columns for activity cards

---

## accessibility

**touch targets**:
- minimum 44pt x 44pt
- cards meet this requirement
- buttons meet this requirement

**contrast**:
- text on dark background: high contrast
- badges: readable colors
- icons: sufficient contrast

**screen readers**:
- section titles: proper headings
- movie cards: labeled with title
- buttons: descriptive labels
- activity cards: describe friend and action

---

## implementation notes

**swiftui components needed**:
- feedview: main screen container
- herocard: ai recommendations header
- moviecard: reusable movie card component
- activitycard: friend activity card
- skeletonview: loading state component
- emptystateview: empty state component

**data requirements**:
- recommendation feed (from api)
- trending movies (from api)
- friend activities (from api)
- user ratings (from api)

**state management**:
- loading state: show skeletons
- error state: show error message
- empty state: show empty state view
- success state: show content

---

## design references

this design is based on the react ui prototype in the ui ux for nuvie folder. the swiftui implementation should match the visual design and behavior of the react components while following ios design patterns.

key reference files:
- components/home.tsx: main feed screen layout
- components/moviecard.tsx: movie card component
- components/activitycard.tsx: activity card component

