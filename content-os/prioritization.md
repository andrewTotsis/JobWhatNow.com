# Prioritization Engine

The single formula that orders the queue. When in doubt, **trust the score** — it's calibrated to favor pages that combine real demand, real emotion, and a real path to ranking.

---

## The formula

```
priority_score =
    (search_volume_score        * 0.25) +
    ((11 - competition_score)   * 0.20) +   // inverted: low competition = high priority
    (emotional_intensity_score  * 0.20) +
    (virality_score             * 0.15) +
    (monetization_intent_score  * 0.10) +
    (recency_score              * 0.10)
```

Output is normalized to a 1–10 scale, rounded to one decimal.

### Why these weights

- **Volume (0.25)** — biggest lever, but not dominant. We do not chase "huge" keywords blindly; the cost of competing is too high.
- **Inverted competition (0.20)** — equal weight with volume. A 6/10 volume keyword with 2/10 competition beats a 10/10 keyword with 9/10 competition every time.
- **Emotional intensity (0.20)** — this site lives or dies on resonance. Struggle queries punch far above their volume because the searcher reads to the end.
- **Virality (0.15)** — how shareable the angle is. A piece that moves on Reddit/X earns links; links compound.
- **Monetization (0.10)** — likelihood of click-through to a recommended tool. Lower weight, deliberately, so we don't pollute the queue with product-shaped content.
- **Recency (0.10)** — how time-sensitive. AI-impact and 2026-trend pieces score high here and need to be refreshed quarterly.

---

## Tier thresholds

| Score | Tier | Action |
|---|---|---|
| 8.5+ | **Lead** | Hand-craft. Senior persona. Original quotes. ~1,000 words. |
| 7.0–8.4 | **Core** | Templated draft → human pass. Standard persona rotation. ~700 words. |
| 5.5–6.9 | **Long-tail** | Templated. Light review. ~600 words. |
| <5.5 | **Defer** | Park in the queue. Re-score quarterly. |

We will not publish below 5.5. Doing so dilutes topical authority on the rest.

---

## Quality checklist (pre-publish)

A row cannot flip to `uploaded = yes` until every box is true:

- [ ] Title matches a real query a human would type
- [ ] Lede addresses the emotional frustration in the first 3 sentences
- [ ] At least one of: real number, named source, scenario, or contrarian point
- [ ] No filler ("In today's competitive job market...") — cut on sight
- [ ] 3–5 internal links to related pages (cluster integrity)
- [ ] One external link to a credible source
- [ ] Conversion block placed contextually, not bolted on
- [ ] Persona voice readable — does it sound like one specific human?
- [ ] Reads cleanly out loud (the 30-second test)

If any box is empty, the row goes back to `status = generating`.

---

## Refresh policy

| Content type | Refresh cadence |
|---|---|
| Trend pieces (AI, layoffs, hiring stats) | Quarterly |
| Job role pages (demand outlook) | Every 6 months |
| Insights essays (evergreen-ish) | Annually |
| Guides (tactical) | Annually + after major platform shifts |

Refreshes update `last_updated` *and* the `dateModified` schema field. Google rewards genuinely updated content; punishes timestamp-only updates.

---

## Anti-cannibalization

Before any new row is added:

1. Search the master table for overlapping keywords (substring + fuzzy match).
2. If a similar row exists with `status != completed` → merge or reject.
3. If a similar row exists with `status == completed` → only add if the **angle**, **persona**, and **intent** are all different.

Two pages targeting the same query split each other's ranking signal. Avoid.
