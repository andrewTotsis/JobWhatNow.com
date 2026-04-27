# Content OS — JobWhatNow

The brain of the site. This directory is the **persistent editorial system** that feeds every page on JobWhatNow.

It is intentionally *not* a CMS. It's a flat, version-controlled set of files that any human or LLM can read, extend, and use as the source of truth for what gets written next.

> **Excluded from search engines** via `robots.txt`. This is internal tooling.

---

## The five files

| File | Purpose |
|---|---|
| `master-content-table.csv` | The single source of truth. Every idea, queued or published. Ranked by priority score. |
| `personas.json` | 50 distinct authorial voices. Each article is assigned one to keep the site from sounding like a single AI. |
| `keywords.json` | 100+ scored search queries with intent, difficulty, volume estimates. |
| `templates/` | Reusable article scaffolds for the four highest-volume page types. |
| `prioritization.md` | The scoring formula and how the queue gets ordered. |

---

## How it works (the 5-step loop)

```
1. INGEST    →  New keyword/idea lands in keywords.json
2. EXPAND    →  Idea becomes 1+ rows in master-content-table.csv (with persona, angle, scores)
3. PRIORITIZE → priority_score is computed; queue is sorted high → low
4. GENERATE  →  Top N rows are turned into full HTML articles
5. UPDATE    →  Row's `status` flips idea → completed; `uploaded = yes`
```

Token-limit-safe: every intermediate state is a file. Run it, stop it, resume tomorrow.

---

## The master table — column reference

| Column | What it holds |
|---|---|
| `id` | Stable unique ID (e.g., `JWN-0001`) |
| `title` | Final article title (the H1) |
| `slug` | SEO URL slug |
| `keyword` | Primary target query |
| `secondary_keywords` | Pipe-separated long-tail variants |
| `search_intent` | struggle / how-to / reality / comparison / trend / emotional |
| `content_type` | insights / jobs / trends / guides / stats |
| `job_role` | If role-specific (e.g., "Software Engineer") |
| `industry` | If industry-specific |
| `search_volume_score` | 1–10 |
| `competition_score` | 1–10 (higher = harder to rank) |
| `virality_score` | 1–10 (shareability) |
| `recency_score` | 1–10 (how time-sensitive) |
| `emotional_intensity_score` | 1–10 (struggle resonance) |
| `monetization_intent_score` | 1–10 (likelihood of click-through to a tool) |
| `priority_score` | Computed — see `prioritization.md` |
| `angle_type` | brutal-truth / optimistic / analytical / storytelling / contrarian |
| `content_goal` | educate / convert / viral / authority |
| `tone_style` | professional / casual / emotional / direct |
| `persona_id` | FK to `personas.json` |
| `persona_name` | Denormalized for readability |
| `status` | idea / queued / generating / completed |
| `article_generated` | yes / no |
| `uploaded` | yes / no |
| `last_updated` | ISO date |
| `notes` | Free text — research links, caveats |

---

## The persona system

Every article is assigned **one** persona from `personas.json`. Personas vary by:
- Background (recruiter, candidate, coach, analyst)
- Tone (direct, warm, contrarian, data-driven)
- Sentence rhythm
- Vocabulary
- What kind of evidence they reach for

This is the single most important anti-AI-slop mechanism. If two articles share the same persona, they'll start sounding the same. **Spread the load.**

---

## Scaling math

| Pages | Approach |
|---|---|
| 1–10 | Hand-crafted, like the launch piece. Every line read aloud. |
| 10–100 | Templates + persona rotation + manual editing of the lede + closer. |
| 100–1,000 | Programmatic generation from CSV rows; human review pass on top 20% by priority. |
| 1,000–10,000 | Full pipeline: keyword expansion → row generation → templated drafts → spot-check QC sampling (5%). |

Quality bar **must not drop** as volume scales. The Quality Checklist (in `prioritization.md`) is enforced before any row flips to `uploaded = yes`.

---

## What this directory is *not*

- Not the website. The site is the static HTML in the parent directory.
- Not crawled by Google (see `robots.txt`).
- Not a CMS. There's no admin UI. Edit the files.
- Not for users. This is editorial machinery.
