# Phase B: Judgment Questions to Ask (fresh LLM conversation, same rules as Phase A)

**Data to provide:** `player_stats.csv`, `game_log.csv`, `player_game_log.csv`
(raw files only — do not paste `PHASE_B_METRICS.md`, that's the answer key)

**Opening prompt:**

> I'm giving you three CSV files from a real Syracuse Women's Lacrosse
> season (2024): player_stats.csv (season totals), game_log.csv (one row
> per game), and player_game_log.csv (one row per player per game). I'm
> going to define some metrics, then ask you questions that require
> judgment, not just lookup. Please show your reasoning and compute
> things directly from the data rather than guessing.

Ask these one at a time, in order:

## Q1 (warm-up judgment question, no defined metric yet)
"Based on this data, who would you say had the biggest offensive impact
this season, and why?" — see what the model reaches for unprompted
before you give it a metric definition.

## Q2 (give it the "most improved" metric explicitly)
"Define 'most improved player' as: the largest increase in
points-per-game between the first half of the season (games 1-11) and
the second half (games 12-22), among players who played at least 5
games in each half. Using that exact definition, who was the most
improved player, and by how much?"

*(Ground truth: Emma Tyrrell, +1.09 PPG, 3.64 → 4.73)*

## Q3 (give it the "game changer" metric explicitly)
"Now define 'game changer' as: average points-per-game multiplied by
the team's win rate in games where that player scored at least 1
point. Using that exact definition, who was the game changer this
season?"

*(Ground truth: Emma Tyrrell, score 2.987)*

## Q4 (the advisory coach question — the target question from the assignment)
"As a coach, if I wanted to win two more games this coming season,
should I focus on offense or defense? And if so, what is the one
player I should work with to be a game changer, and why?"

*(No single ground truth — this is the open-ended judgment call. Push
back if the model's reasoning doesn't hold up against the real numbers,
or if it recommends a different player than the metrics above support.)*

---

## Prompt engineering notes (fill in as you go)

- Did the model drift back to its own definition of "most improved" or
  "game changer" instead of using yours exactly? Note where.
- Did it compute the numbers itself (via written-out arithmetic or
  code) or just assert an answer?
- If Q4's answer seemed weak or generic, what did you change in the
  follow-up prompt that got a stronger, more specific answer? (e.g.
  asking it to cite specific numbers, asking it to consider defense
  separately, asking it to show its work)

## Validation checklist (after you get responses)

For each claim the model makes in Q4:
- [x] Does the player it names actually have the numbers to back up
      the recommendation? (cross-check against `PHASE_B_METRICS.md`
      and the raw data)
- [x] Does its offense-vs-defense reasoning hold up against the team's
      actual goals-scored vs. goals-allowed trends across the season?
- [x] If it disagrees with the metrics above, is that disagreement
      defensible (a genuinely different but reasonable way of reading
      the data) or is it just wrong?

---

## ACTUAL RESULTS (completed)

**Model tested:** Claude Sonnet 5 (extended thinking: High), claude.ai
web interface, fresh conversation titled "Syracuse women's lacrosse
2024 season analysis"
**Date:** 2026-08-04

### Q1 (warm-up) — skipped
Went directly to Q2 since the metric-definition questions were the
priority; the warm-up wasn't essential to the graded deliverable.

### Q2: Most Improved Player
**Model's answer:** Emma Tyrrell, +1.09 PPG (3.64 in games 1-11 → 4.73
in games 12-22). Correctly showed the underlying totals (40 pts/11
games, 52 pts/11 games) and named the correct runners-up (Sweitzer
+0.71, Britton +0.61) with their exact underlying numbers.
**Verdict:** Correct in full — matches `PHASE_B_METRICS.md` exactly,
including all secondary figures.
**How it got there:** Computed directly from the data (showed totals
and per-half game counts), not asserted.

### Q3: Game Changer
**Model's answer:** Emma Tyrrell, score 2.99 (4.18 ppg × 71.4% win
rate = 2.99). Provided a full ranked table (Adamson 2.74, Ward 2.68,
Smith 1.84, Rowley 1.63) with every intermediate number shown.
**Verdict:** Correct in full — every figure in the table matches
`derived_metrics.py`'s output to two decimal places.
**Bonus:** The model proactively flagged a real limitation of the
metric itself (ppg is uncapped but win rate is capped at 1.0, so the
formula rewards volume more than "clutch" performance) — this is
exactly the kind of critical engagement with a *given* definition the
assignment is looking for, not just plugging in numbers.

### Q4: The advisory coach question
**Model's answer:** Focus on offense. Recommends working with Emma
Tyrrell specifically on finishing under defensive pressure, citing a
large shooting-percentage drop in losses (57.4% → 29.6%) and an
especially severe drop against Boston College (14.3% across all three
meetings, the team that beat Syracuse three times).

**Verdict: mostly correct, one real overreach.** Every specific number
checked out exactly against the raw data:

| Claim | Verified? |
|---|---|
| Season margin +5.5 (15.2 scored / 9.7 allowed) | ✅ exact (15.23/9.68) |
| Scored/allowed split, wins (17.2/8.6) vs losses (10.0/12.7) | ✅ exact |
| 5 of 6 losses decided by 1 or 3 goals | ✅ confirmed |
| Tyrrell season shooting 51.9% | ✅ exact |
| Tyrrell shooting: 57.4% in wins, 29.6% in losses | ✅ exact |
| Tyrrell vs. Boston College: 2 goals on 14 shots (14.3%) | ✅ exact |
| Hypothetical "+6 goals" if shooting at season rate on loss-game volume | ✅ arithmetically exact (27 × 0.519 ≈ 14.0, minus 8 actual = 6.0) |
| **"Comparable shot volume" between wins and losses** | ❌ **overstated** — actually 6.75 shots/game in wins vs. 4.5/game in losses, a 33% drop |

**Why this matters:** the model built its entire recommendation on a
"finishing problem, not a volume problem" framing — but Tyrrell is
demonstrably getting meaningfully fewer looks per game in losses, not
a comparable number of looks she's simply missing. The real story is
probably both: the team's collective offense generates fewer chances
for her when the game is going badly, AND she converts a lower share
of the chances she does get. The model's recommendation to work with
Tyrrell may still be reasonable, but the reasoning oversold the
"she's still getting the shots" half of its own argument. This is
exactly the kind of "confident, well-written answer that does not
fully survive validation" the assignment asks us to document as a
finding, not paper over.

## Prompt engineering notes

- No follow-up prompting was needed to reach a strong, specific answer
  to Q4 on the first attempt — the model went directly to per-half and
  per-opponent shooting splits without being asked to "show its work"
  or "consider defense separately." This differs from the assignment's
  expectation that reaching a defensible answer would likely take
  iteration; here it didn't.
- The model did not write or execute code for any of these answers —
  everything was conversational arithmetic, narrated inline. Given
  that every checked number was exact, this suggests the model was
  genuinely computing over the provided data rather than guessing,
  even without being told to "compute, don't guess" explicitly (that
  instruction was in the opening prompt, so it's possible that alone
  was sufficient).
- The one weak point (shot volume framing) wasn't caught by asking a
  follow-up question — it was caught by our own independent
  recomputation. This is itself a useful data point for the
  assignment's "where would you trust conversational answers vs.
  insist on validation" research question: a well-organized,
  well-cited answer with 8 of 9 checkable claims exactly right can
  still contain one meaningfully misleading framing, and there was no
  surface-level signal (hedging, vagueness, internal inconsistency)
  that would have tipped us off without independently recomputing it.

