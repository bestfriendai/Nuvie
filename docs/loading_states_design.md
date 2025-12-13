# loading states design — nuvie

this document describes the skeleton ui and loading state patterns for the ios app.

---

## overview

loading states show users that content is being fetched. we use skeleton ui (shimmer effects) to indicate loading without showing blank screens.

---

## skeleton ui principles

**why skeleton ui**:
- better than blank screens
- shows layout structure
- feels faster than spinners
- reduces perceived wait time

**design rules**:
- match final content layout
- use subtle animations
- keep it simple
- don't distract users

---

## feed screen loading

**when to show**:
- initial app load
- refreshing recommendations
- loading more content (pagination)

**layout**:
- matches feed screen structure
- four sections with skeletons

**section 1: hero skeleton**:
- full width card
- height: 120pt
- rounded corners: 16pt
- shimmer animation
- background: dark slate (#1e293b)

**section 2: recommended movies skeleton**:
- grid layout: 2-4 columns (matches final layout)
- each card: 2:3 aspect ratio
- rounded corners: 8pt
- shimmer animation
- background: dark slate (#1e293b)
- gap: 16pt between cards

**section 3: trending movies skeleton**:
- horizontal scrollable grid
- 6 columns on large, 3 on medium, 2 on small
- each card: 2:3 aspect ratio (compact)
- rounded corners: 8pt
- shimmer animation
- background: dark slate (#1e293b)
- gap: 16pt between cards

**section 4: activity cards skeleton**:
- vertical list
- each card: full width, 80pt height
- rounded corners: 12pt
- shimmer animation
- background: dark slate (#1e293b)
- gap: 12pt between cards

---

## movie card skeleton

**standard card skeleton**:
- poster area: 2:3 aspect ratio
- title area: 40pt height below poster
- rounded corners: 8pt
- shimmer animation

**compact card skeleton**:
- poster area: 2:3 aspect ratio
- no title area
- rounded corners: 8pt
- shimmer animation

**skeleton structure**:
```
┌─────────────────┐
│   [shimmer]     │  (poster area)
│                 │
│                 │
└─────────────────┘
┌─────────────────┐
│ [shimmer line]  │  (title, if standard)
│ [shimmer line]  │  (metadata, if standard)
└─────────────────┘
```

---

## activity card skeleton

**layout**:
- full width card
- height: 80pt
- rounded corners: 12pt
- padding: 16pt

**skeleton elements**:
- avatar circle: 40pt diameter (left)
- text lines: 2-3 lines (middle)
- poster thumbnail: 64pt width (right)

**skeleton structure**:
```
┌─────────────────────────────────────┐
│ [○]  [━━━━━━━━━━━━━━━━━━━━━━━━━━]  │
│      [━━━━━━━━━━━━━━━━━━━━━━━━]    │
│      [━━━━━━━━━━━━━━━━━━━━━━━━━━]  │
│                    [━━━━━━━━━━━━]  │
└─────────────────────────────────────┘
```

---

## shimmer animation

**effect**:
- gradient overlay moves across skeleton
- creates "shimmer" or "sweep" effect
- indicates loading activity

**gradient**:
- start: transparent → light gray → transparent
- light gray: rgba(255, 255, 255, 0.1)
- width: 200pt
- angle: horizontal (left to right)

**animation**:
- position: -100% to 100% (off-screen to off-screen)
- duration: 1.5 seconds
- repeat: infinite
- easing: linear (constant speed)

**implementation**:
- use linear gradient
- animate gradient position
- loop continuously
- stop when content loads

---

## loading indicators

**when to use spinners**:
- small actions (button clicks)
- form submissions
- quick operations

**when to use skeletons**:
- page loads
- list content
- large data fetches

**spinner design** (if needed):
- size: 20pt diameter
- color: amber (#f59e0b)
- style: system activity indicator
- centered in container

---

## empty state loading

**initial load**:
- show skeleton while fetching
- if no data after load: show empty state
- transition: skeleton → empty state (fade)

**refreshing**:
- show skeleton overlay
- keep existing content visible
- overlay fades in/out

---

## error states

**network error**:
- show error message
- retry button
- icon: wifi off or alert

**timeout**:
- show timeout message
- retry button
- icon: clock

**error message design**:
- centered on screen
- icon: 48pt, muted color
- title: "something went wrong"
- message: "please check your connection"
- button: "try again" (amber gradient)

---

## loading state transitions

**skeleton → content**:
- fade out skeleton (0.3s)
- fade in content (0.3s)
- stagger: slight delay between items
- smooth transition

**content → skeleton** (refresh):
- fade out content (0.2s)
- fade in skeleton (0.2s)
- quick transition

**loading → error**:
- fade out skeleton (0.3s)
- fade in error (0.3s)
- show retry option

---

## performance considerations

**skeleton rendering**:
- lightweight (no images)
- fast to render
- doesn't block ui

**animation performance**:
- use gpu-accelerated animations
- avoid layout recalculations
- keep animations smooth (60fps)

**when to stop**:
- stop shimmer when content ready
- remove skeleton immediately
- don't show skeleton too long

---

## implementation notes

**swiftui components**:
- skeletonview: reusable skeleton component
- shimmer modifier: animation modifier
- skeletoncard: movie card skeleton
- skeletonactivity: activity card skeleton

**state management**:
- @state var isLoading: bool
- show skeleton when true
- hide when false

**data flow**:
```
view appears → isLoading = true → show skeleton
api call → fetch data
data received → isLoading = false → show content
```

---

## accessibility

**screen readers**:
- announce "loading" when skeleton shows
- announce "loaded" when content appears
- don't read skeleton content

**reduced motion**:
- respect prefersreducedmotion
- show static gray boxes instead of shimmer
- still indicate loading state

---

## design references

skeleton ui patterns are based on modern ios design guidelines. the implementation should feel native to ios while matching the nuvie design system.

key principles:
- match final layout
- subtle animations
- fast transitions
- clear loading indication

