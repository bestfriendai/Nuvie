# empty states design — nuvie

this document describes the empty state designs for when there's no data to display.

---

## overview

empty states appear when there's no content to show. they should be helpful, friendly, and guide users to take action.

---

## empty state principles

**why empty states matter**:
- better than blank screens
- guide user actions
- set expectations
- build trust

**design rules**:
- be helpful, not annoying
- explain why it's empty
- suggest what to do next
- use friendly tone

---

## feed screen empty states

### no recommendations

**when to show**:
- user is new (no ratings yet)
- no recommendations available
- recommendation service error

**design**:
- icon: sparkles icon (large, 64pt, muted amber)
- title: "no recommendations yet"
- message: "rate some movies to get personalized recommendations"
- button: "discover movies" (amber gradient, links to discover)

**layout**:
- centered vertically and horizontally
- padding: 32pt all around
- max width: 280pt (readable)

**visual**:
- icon: amber color, 20% opacity
- title: 18pt, white, bold
- message: 14pt, muted gray
- button: 44pt height, full width

---

### no trending movies

**when to show**:
- no trending data available
- service temporarily unavailable

**design**:
- section hidden if no data (preferred)
- or show message: "check back later for trending movies"
- no action needed (informational only)

**layout**:
- if shown: small message, centered
- icon: trending icon (muted)
- text: 14pt, muted gray

---

### no friend activity

**when to show**:
- user has no friends
- friends have no recent activity
- no activity data available

**design**:
- icon: users icon (large, 64pt, muted blue)
- title: "no friend activity"
- message: "add friends to see what they're watching"
- button: "find friends" (amber gradient, links to social)

**layout**:
- centered vertically and horizontally
- padding: 32pt all around
- max width: 280pt

**visual**:
- icon: blue color, 20% opacity
- title: 18pt, white, bold
- message: 14pt, muted gray
- button: 44pt height, full width

---

## discover screen empty states

### no search results

**when to show**:
- search query returns no results
- filters too restrictive

**design**:
- icon: search icon (large, 64pt, muted)
- title: "no movies found"
- message: "try different search terms or filters"
- button: "clear filters" (if filters applied)

**layout**:
- centered in results area
- padding: 32pt all around

**visual**:
- icon: gray, 20% opacity
- title: 18pt, white, bold
- message: 14pt, muted gray
- suggestions: list of popular genres (optional)

---

### no movies in genre

**when to show**:
- selected genre has no movies
- database issue

**design**:
- icon: film icon (large, 64pt, muted)
- title: "no movies in this genre"
- message: "try selecting a different genre"
- button: "browse all" (amber gradient)

**layout**:
- centered in results area
- padding: 32pt all around

---

## social screen empty states

### no friends

**when to show**:
- user has no friends added
- all friend requests pending

**design**:
- icon: user plus icon (large, 64pt, muted blue)
- title: "no friends yet"
- message: "add friends to see their movie activity"
- button: "find friends" (amber gradient)

**layout**:
- centered in friends section
- padding: 32pt all around

**visual**:
- icon: blue, 20% opacity
- title: 18pt, white, bold
- message: 14pt, muted gray
- button: 44pt height, full width

---

### no friend suggestions

**when to show**:
- no friend suggestions available
- user already added all suggested friends

**design**:
- section hidden (preferred)
- or small message: "no new suggestions"
- no action needed

---

### no activity

**when to show**:
- friends have no recent activity
- activity feed is empty

**design**:
- icon: clock icon (large, 64pt, muted)
- title: "no recent activity"
- message: "your friends haven't been active lately"
- button: "refresh" (outline button)

**layout**:
- centered in activity feed
- padding: 32pt all around

---

## profile screen empty states

### no watched movies

**when to show**:
- user hasn't watched any movies
- watch history is empty

**design**:
- icon: film icon (large, 64pt, muted)
- title: "no watched movies"
- message: "start watching to build your history"
- button: "discover movies" (amber gradient)

**layout**:
- centered in watched section
- padding: 32pt all around

---

### no ratings

**when to show**:
- user hasn't rated any movies
- ratings list is empty

**design**:
- icon: star icon (large, 64pt, muted yellow)
- title: "no ratings yet"
- message: "rate movies to improve your recommendations"
- button: "rate movies" (amber gradient)

**layout**:
- centered in ratings section
- padding: 32pt all around

---

## movie detail screen empty states

### no reviews

**when to show**:
- movie has no reviews
- reviews section is empty

**design**:
- icon: message icon (large, 64pt, muted)
- title: "no reviews yet"
- message: "be the first to review this movie"
- button: "write review" (amber gradient)

**layout**:
- centered in reviews section
- padding: 32pt all around

---

## empty state components

### standard empty state

**structure**:
- icon (large, centered)
- title (bold, white)
- message (muted gray)
- button (optional, amber gradient)

**spacing**:
- icon to title: 16pt
- title to message: 8pt
- message to button: 24pt
- padding around all: 32pt

**sizing**:
- icon: 64pt
- title: 18pt font
- message: 14pt font
- button: 44pt height
- max width: 280pt

---

## colors

**icons**:
- muted color: 20% opacity
- color matches context (amber, blue, etc.)

**text**:
- title: white (#ffffff)
- message: muted gray (#94a3b8)

**buttons**:
- primary: amber gradient
- outline: transparent with border

**backgrounds**:
- transparent (shows screen background)
- or subtle card background

---

## typography

**title**:
- font: system font (sf pro)
- size: 18pt
- weight: bold
- color: white
- alignment: center

**message**:
- font: system font (sf pro)
- size: 14pt
- weight: regular
- color: muted gray
- alignment: center
- line height: 1.4

**button text**:
- font: system font (sf pro)
- size: 16pt
- weight: medium
- color: white (on gradient)

---

## animations

**empty state appear**:
- fade in: opacity 0 → 1
- duration: 0.3s
- easing: ease-in-out

**icon animation** (optional):
- subtle scale: 1.0 → 1.05 → 1.0
- duration: 2s
- repeat: infinite (very subtle)

**button hover**:
- scale: 1.0 → 1.02
- duration: 0.2s
- easing: ease-out

---

## responsive behavior

**iphone se (small)**:
- max width: 260pt
- padding: 24pt
- icon: 56pt

**iphone 14/15 (standard)**:
- max width: 280pt
- padding: 32pt
- icon: 64pt

**iphone 14/15 pro max (large)**:
- max width: 300pt
- padding: 32pt
- icon: 64pt

**ipad (future)**:
- max width: 400pt
- padding: 40pt
- icon: 72pt

---

## accessibility

**screen readers**:
- announce empty state title
- announce message
- announce button if present
- describe what user can do

**touch targets**:
- buttons: minimum 44pt height
- entire button area tappable
- sufficient spacing between elements

**contrast**:
- text meets wcag aa standards
- icons have sufficient contrast
- buttons are clearly visible

---

## implementation notes

**swiftui component**:
- emptystateview: reusable component
- accepts: icon, title, message, button
- handles all empty state scenarios

**usage**:
```swift
EmptyStateView(
    icon: "sparkles",
    title: "no recommendations yet",
    message: "rate some movies...",
    buttonTitle: "discover movies",
    buttonAction: { navigate to discover }
)
```

**state management**:
- check if data is empty
- show empty state if true
- hide when data loads

**data flow**:
```
load data → check if empty → show empty state
user action → navigate to suggested screen
```

---

## design references

empty states should be helpful and friendly. they guide users to take action rather than leaving them confused.

key principles:
- explain why it's empty
- suggest what to do next
- use friendly, helpful tone
- make actions clear and easy

