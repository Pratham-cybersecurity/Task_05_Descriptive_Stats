import csv
import subprocess
import time
from bs4 import BeautifulSoup

GAMES = [
    ("2024-02-10", "Northwestern", "northwestern", "17096"),
    ("2024-02-14", "ARMY", "army", "17097"),
    ("2024-02-17", "Maryland", "maryland", "17098"),
    ("2024-02-24", "Notre Dame", "notre-dame", "17099"),
    ("2024-03-02", "Duke", "duke", "17100"),
    ("2024-03-05", "Stony Brook", "stony-brook", "17101"),
    ("2024-03-09", "Virginia Tech", "virginia-tech", "17102"),
    ("2024-03-16", "North Carolina", "north-carolina", "17103"),
    ("2024-03-19", "UAlbany", "ualbany", "17104"),
    ("2024-03-23", "Virginia", "virginia", "17105"),
    ("2024-03-27", "Loyola", "loyola", "17198"),
    ("2024-03-30", "Louisville", "louisville", "17107"),
    ("2024-04-02", "Cornell", "cornell", "17108"),
    ("2024-04-06", "Pittsburgh", "pittsburgh", "17109"),
    ("2024-04-13", "Clemson", "clemson", "17110"),
    ("2024-04-18", "Boston College", "boston-college", "17111"),
    ("2024-04-23", "Louisville", "louisville", "17940"),
    ("2024-04-26", "Virginia", "virginia", "17941"),
    ("2024-04-28", "Boston College", "boston-college", "17943"),
    ("2024-05-12", "Stony Brook", "stony-brook", "17945"),
    ("2024-05-16", "Yale", "yale", "17948"),
    ("2024-05-24", "Boston College", "boston-college", "17949"),
]

URL_TEMPLATE = "https://cuse.com/sports/womens-lacrosse/stats/2024/{slug}/boxscore/{gid}"
COLUMNS = ["#", "Player", "Pos", "G", "A", "P", "SH", "SOG", "GB", "TO", "CT", "DC", "FPS", "FOULS"]

def fetch_html(url, path):
    subprocess.run(["curl", "-s", "-A", "Mozilla/5.0", url, "-o", path], check=True)

def find_syracuse_table(soup):
    for t in soup.find_all("table"):
        rows = t.find_all("tr")
        if not rows:
            continue
        header = [c.get_text(strip=True) for c in rows[0].find_all(["th", "td"])]
        if header != COLUMNS:
            continue
        # Syracuse's table uses "Lastname, Firstname" -- check first data row
        if len(rows) > 1:
            first_player = rows[1].find_all(["th", "td"])[1].get_text(strip=True)
            if "," in first_player:
                return t
    return None

def parse_table(table):
    rows = table.find_all("tr")[1:]  # skip header
    out = []
    for r in rows:
        cells = [c.get_text(strip=True) for c in r.find_all(["th", "td"])]
        if len(cells) != len(COLUMNS):
            continue
        if cells[1].strip().lower() == "totals":
            continue
        out.append(cells)
    return out

def main():
    all_rows = []
    for date, opponent, slug, gid in GAMES:
        url = URL_TEMPLATE.format(slug=slug, gid=gid)
        path = f"/tmp/box_{gid}.html"
        fetch_html(url, path)
        with open(path, encoding="utf-8") as f:
            html = f.read()
        soup = BeautifulSoup(html, "lxml")
        table = find_syracuse_table(soup)
        if table is None:
            print(f"WARNING: could not find Syracuse table for {date} vs {opponent} ({gid})")
            continue
        player_rows = parse_table(table)
        for cells in player_rows:
            all_rows.append({
                "date": date, "opponent": opponent,
                "number": cells[0], "player": cells[1], "pos": cells[2],
                "g": cells[3], "a": cells[4], "pts": cells[5], "sh": cells[6],
                "sog": cells[7], "gb": cells[8], "to": cells[9], "ct": cells[10],
                "dc": cells[11], "fps": cells[12], "fouls": cells[13],
            })
        print(f"OK: {date} vs {opponent} ({gid}) -- {len(player_rows)} player rows")
        time.sleep(0.3)

    with open("player_game_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "opponent", "number", "player", "pos",
                                                "g", "a", "pts", "sh", "sog", "gb", "to", "ct",
                                                "dc", "fps", "fouls"])
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nDone. {len(all_rows)} total player-game rows written to player_game_log.csv")

if __name__ == "__main__":
    main()
