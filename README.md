# Task 05: Descriptive Statistics and Large Language Models

*From Ground Truth to LLM Judgment*

## Dataset

**2024 Syracuse University Women's Lacrosse season** — 22 games, 34
players. Source: [cuse.com 2024 Women's Lacrosse Cumulative
Statistics](https://cuse.com/sports/womens-lacrosse/stats/2024/)
(official season stats page).

This repo does not need external data download — `player_stats.csv` and
`game_log.csv` were transcribed directly from the source page's HTML
tables and are included here (this is public sports statistics, small
and appropriate to include per the assignment; unlike Tasks 1-3 there is
no separate large download step required).

- `player_stats.csv` — season totals for all 34 players who saw the
  field (goals, assists, points, shots, ground balls, turnovers, etc.)
- `game_log.csv` — one row per game (22 rows): opponent, result, score,
  and team-level box score stats for that game.

## Reproducing the ground truth

```bash
pip install pandas
python ground_truth.py
```

This prints season overview stats, player leaders, game-level facts
(biggest win, closest game, highest combined score), and a validation
check against the source page's own season-total row (confirms the
transcription is accurate: 335 goals, 150 assists, 485 points, .468 team
shot percentage all match exactly).

See `GROUND_TRUTH_ANSWER_KEY.md` for the full answer key used to grade
the LLM's responses.

## Phase A: Baseline Factual Q&A

See `PROMPT_LOG.md` for the full prompt-and-response log.

**Methodology:** the ground truth (`ground_truth.py`, `GROUND_TRUTH_ANSWER_KEY.md`)
was established with Claude in one conversation. The actual LLM test then
happened in a **separate, fresh conversation** with Claude — no memory of
the ground-truth work — given only the raw CSVs, never the answer key.
This keeps the test honest: the model had to actually reason over the
data, not recite an answer key it had just helped compute.

**Result: 9 for 9 questions correct**, including the two hardest
(computing an assist-to-turnover ratio not present as any column, after
filtering; averaging a derived per-game margin across 16 wins). The
model consistently showed its work — narrating which rows/columns it
used and the arithmetic performed — rather than simply asserting a
number, for every single answer.

**The most interesting finding wasn't a model failure — it was a ground
truth failure.** Asked for "the closest game," the model found a
four-way tie at a 1-goal margin. My own `ground_truth.py` had only ever
reported one game (using pandas' `idxmin()`, which silently returns just
the first tied row). The model was more careful than the reference
script it was ostensibly being graded against. The script has since been
corrected (see the note at the top of `ground_truth.py`), and the same
class of bug turned out to also be hiding in "biggest win" (also a tie,
also originally under-reported).

This reframes the phase's central question a little: the interesting
risk with LLM-assisted analysis in this test wasn't the model being
confidently wrong — it was that *my own ground truth*, the thing I was
trusting completely because I'd written it myself, had an unexamined
edge case. "I computed it myself" is not the same guarantee of
correctness it can feel like; it's only as good as the edge cases the
author thought to check.

## Phase B: Derived Metrics and Judgment Questions

_(To be completed in the second reporting period — metric definitions,
prompt engineering log, and the advisory "coach" question.)_

## Reflections

_(To be completed — where the model succeeded, where it failed, and
what that suggests about trusting LLMs with real analytical work.)_
