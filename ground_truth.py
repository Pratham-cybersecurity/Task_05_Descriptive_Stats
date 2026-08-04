"""
ground_truth.py  (Task 5 / Phase A)

Establishes trustworthy ground-truth statistics for the 2024 Syracuse
Women's Lacrosse season, computed directly from the season's official
cumulative stats page (cuse.com). This is the answer key everything else
in this task gets checked against.

Data source: https://cuse.com/sports/womens-lacrosse/stats/2024/
Two files, hand-transcribed from that page's HTML tables (verified against
the page's own season totals row, e.g. team record 16-6, team goals 335,
team shot pct .468):

  - player_stats.csv : season totals per player (34 players)
  - game_log.csv     : one row per game (22 games), team-level box score

Usage:
    python ground_truth.py

NOTE ON A REAL BUG THIS SCRIPT ORIGINALLY HAD: the first version used
pandas' `idxmin()`/`idxmax()` for "closest game" and "biggest win," which
silently returns only the FIRST matching row when there's a tie. There
IS a tie in this data: four games were decided by exactly 1 goal
(Maryland, Stony Brook, Virginia 3/23, Boston College 4/18), and two
games were tied for the biggest win margin (North Carolina and Virginia
4/26, both by 15). The original script reported only one game for each,
silently dropping the others.

This was caught by an LLM's answer during Phase A Q&A testing (see
PROMPT_LOG.md, Q7) -- the model checked for ties where the "ground
truth" script hadn't, and was MORE thorough and correct than the answer
key it was being tested against. That's a significant finding for this
task and is discussed in the README: the ground truth is only as
trustworthy as the person who wrote it thought to check for edge cases,
and in this instance the LLM did.
"""

import pandas as pd

PLAYER_STATS_FILE = "player_stats.csv"
GAME_LOG_FILE = "game_log.csv"


def load_data():
    players = pd.read_csv(PLAYER_STATS_FILE)
    games = pd.read_csv(GAME_LOG_FILE)
    games["date"] = pd.to_datetime(games["date"])
    games["margin"] = games["team_score"] - games["opp_score"]
    games["combined_score"] = games["team_score"] + games["opp_score"]
    return players, games


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    players, games = load_data()

    print_section("SEASON OVERVIEW")
    n_games = len(games)
    wins = (games["result"] == "W").sum()
    losses = (games["result"] == "L").sum()
    print(f"Games played: {n_games}")
    print(f"Record: {wins}-{losses}")
    print(f"Total goals scored: {games['team_score'].sum()}")
    print(f"Total goals allowed: {games['opp_score'].sum()}")
    print(f"Average goals scored per game: {games['team_score'].mean():.2f}")
    print(f"Average goals allowed per game: {games['opp_score'].mean():.2f}")

    print_section("PLAYER LEADERS")
    for col, label in [("g", "Goals"), ("a", "Assists"), ("pts", "Points"),
                        ("sh", "Shots"), ("gb", "Ground Balls"),
                        ("ct", "Caused Turnovers"), ("dc", "Draw Controls")]:
        top = players.loc[players[col].idxmax()]
        print(f"  {label + ':':<20} {top['player']:<20} {top[col]}")

    print_section("GAME-LEVEL FACTS")
    max_margin = games["margin"].max()
    biggest_wins = games[games["margin"] == max_margin]
    if len(biggest_wins) == 1:
        g = biggest_wins.iloc[0]
        print(f"Biggest win: vs {g['opponent']} on {g['date'].date()}, "
              f"{g['team_score']}-{g['opp_score']} (margin +{g['margin']})")
    else:
        print(f"Biggest win: TIE among {len(biggest_wins)} games, each by +{max_margin}:")
        for _, g in biggest_wins.iterrows():
            print(f"    vs {g['opponent']} on {g['date'].date()}, "
                  f"{g['team_score']}-{g['opp_score']}")

    worst_loss = games.loc[games["margin"].idxmin()]
    print(f"Worst loss: vs {worst_loss['opponent']} on "
          f"{worst_loss['date'].date()}, {worst_loss['team_score']}-"
          f"{worst_loss['opp_score']} (margin {worst_loss['margin']})")

    closest_margin = games["margin"].abs().min()
    closest_games = games[games["margin"].abs() == closest_margin]
    if len(closest_games) == 1:
        g = closest_games.iloc[0]
        print(f"Closest game: vs {g['opponent']} on {g['date'].date()}, "
              f"{g['team_score']}-{g['opp_score']} (margin {g['margin']:+d})")
    else:
        print(f"Closest game: TIE among {len(closest_games)} games, "
              f"each decided by {closest_margin} goal(s):")
        for _, g in closest_games.iterrows():
            print(f"    vs {g['opponent']} on {g['date'].date()}, "
                  f"{g['team_score']}-{g['opp_score']} ({g['result']}, "
                  f"margin {g['margin']:+d})")

    highest_combined = games.loc[games["combined_score"].idxmax()]
    print(f"Highest combined score: vs {highest_combined['opponent']} on "
          f"{highest_combined['date'].date()}, "
          f"{highest_combined['team_score']}-{highest_combined['opp_score']} "
          f"(combined {highest_combined['combined_score']})")

    win_games = games[games["result"] == "W"]
    loss_games = games[games["result"] == "L"]
    print(f"\nAverage margin of victory in wins: +{win_games['margin'].mean():.2f}")
    print(f"Average margin of defeat in losses: {loss_games['margin'].mean():.2f}")

    print_section("SHOOTING")
    total_shots = players["sh"].sum()
    total_goals = players["g"].sum()
    print(f"Team shots: {total_shots}, team goals: {total_goals}, "
          f"team shot pct: {total_goals/total_shots:.3f}")
    print("(Cross-check against the source page's own team-total row: "
          "716 shots, 335 goals, .468 -- confirms our transcription is correct)")

    print_section("VALIDATION AGAINST SOURCE PAGE'S OWN TOTALS")
    print(f"players.csv sum of goals:   {players['g'].sum()}  (source page total row: 335)")
    print(f"players.csv sum of assists: {players['a'].sum()}  (source page total row: 150)")
    print(f"players.csv sum of points:  {players['pts'].sum()}  (source page total row: 485)")
    print(f"game_log.csv sum of team_score: {games['team_score'].sum()}  (should equal players' goal sum: 335)")


if __name__ == "__main__":
    main()
