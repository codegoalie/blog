# Plan: Epcot Flower & Garden 2026 Park Guide

## Context

The user has an existing festival overview in `2026.md`/`2026.html` and personal favorites in `2026-notes.md`. They want a new mobile-friendly interactive guide to use while walking Epcot — showing only their favorites, organized by World Showcase geography (starting at Mexico), with the ability to mark items as "tried" and hide them.

---

## Key Data Notes

**Booth attribution fix:** `2026-notes.md` lists several Lan Yuan (China) items under the `## Jardin de Fiestas` header — likely a note-taking mix-up. Per `2026.md`, these belong at Lan Yuan:
- Pan-fried Vegetable Dumplings
- Sha Cha Beef Bao Bun
- Tanghulu
- First Emperor cocktail

The Mexico-only items at Jardin de Fiestas are: Chilaquiles con Carne, Spicy Mango Margarita.

---

## Output

A single new file: `/home/codegoalie/workspace/flower-and-garden/park-guide.html`

Reuses the green Flower & Garden color palette from `2026.html` (CSS variables: `--green-dark`, `--green-mid`, `--green-light`, etc.).

---

## Structure

### Section 1 — World Showcase (Mexico → Canada, counterclockwise)

Only booths where the user has favorites are shown. Booths with no favorites are skipped.

| Stop | Country | Booth | User's Favorites |
|------|---------|-------|-----------------|
| 1 | Mexico | Jardin de Fiestas | Chilaquiles con Carne, Spicy Mango Margarita |
| 2 | China | Lan Yuan | Pan-fried Vegetable Dumplings, Sha Cha Beef Bao Bun, Tanghulu, First Emperor cocktail |
| 3 | Germany | Bauernmarkt | Potato Pancakes, Pretzel Bread Ham Sandwich, Apfelschaumwein |
| 4 | Italy | Primavera Kitchen | Insalata di Pasta, Italian Red Sangria, Elderflower Sparkling Cocktail |
| 5 | The American Adventure | Magnolia Terrace | Keel Farms King Cake Hard Cider, Spicy Chicken Gumbo |
| 6 | Japan | Hanami | Frushi, 3 Daughters Brewing Strawberry Ichigo IPA, Sakura Beauty Sake |
| 7 | Morocco | Tangerine Café | Cider Flight (3 varieties), Moroccan Wrap (Maybe) |
| 8 | Canada | Canada Popcorn Cart | Blueberry-Ginger Smash |

### Section 2 — Other Park Booths

Non-World-Showcase booths with user favorites:

- **Nectar** (World Nature / Land Kiosk) — Coconut Panna Cotta *(is it dairy free?)*
- **Beach Grub** — Orange Cream Bar, Key Lime Hard Cider
- **Yacht Grub** — Limoncello-Basil Sparkling Cider
- **Swirled Showcase** — Liquid Nitro Honey-Mascarpone Cheesecake, DOLE Whip Peach
- **Connections Eatery** — Hot Honey Chicken Sandwich, Pizza Bianca, Garden Glimmer cocktail
- **The Honey Bee-stro** — Honeycomb Bowl, Brew Hub Nectar Bloom IPA, Orange Blossom Honey Wine
- **Pineapple Promenade** — Spicy Hot Dog with plantain chips, Sparkling Pineapple Wine, Deschutes Brewery Tropical Fresh IPA
- **La Isla Fresca** — Jamaican Jerk Chicken, Ceviche, Citrus Slushy with Don Q Limón Rum
- **Trowel & Trellis** — Miso Cola-glazed Sticky Pork Ribs

---

## Features

### "Tried" Toggle
- Each item has a large tap-friendly checkbox or button: **"Try"** / **"Tried ✓"**
- When marked tried: item text gets strikethrough + muted color
- State persisted in `localStorage` keyed by `booth:itemIndex`

### Hide/Show Tried Items
- Sticky button at top: **"Hide Tried"** / **"Show All"**
- When hiding: tried items collapse with CSS transition (no layout jump)
- Counter in header: "5 of 23 tried"

### Reset
- Small "Reset all" link (confirmation prompt before clearing localStorage)

### Mobile-first design
- min tap target 44px
- Large readable font (16px+)
- Booth cards with clear country label and emoji flag
- Sticky header with progress + hide toggle
- No horizontal scroll

---

## Implementation Details

- Pure HTML + vanilla JS (no build step, works offline)
- All data hardcoded inline in a JS `const BOOTHS = [...]` array
- `localStorage` key: `fg2026_tried` storing a Set serialized as JSON array
- The "Maybe" Moroccan Wrap is included with a "?" badge but otherwise treated the same as other items

---

## Files to Create/Modify

| File | Action |
|------|--------|
| `/home/codegoalie/workspace/flower-and-garden/park-guide.html` | **Create** new file |

No existing files modified.

---

## Verification

1. Open `park-guide.html` in a browser
2. Confirm World Showcase section lists booths in Mexico → Canada order
3. Tap a few items → verify strikethrough + localStorage persistence on page reload
4. Toggle "Hide Tried" → verify tried items collapse and counter updates
5. Check mobile layout in browser DevTools responsive mode
6. Confirm Lan Yuan items appear under China, not Mexico
