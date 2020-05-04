from os.path import exists
import requests
import json
from pathlib import Path
import pandas as pd
import warnings

warnings.filterwarnings("ignore")


def load_games(user_name, month, year):
    folder = f"data/{user_name}"
    filepath = f"{folder}/{year}_{month}.txt"
    Path(folder).mkdir(parents=True, exist_ok=True)
    if exists(filepath):
        content = open(filepath).read()
    else:
        print("Download games...")
        r = requests.get(url)
        content = r.text
        open(filepath, "w").write(content)
    games = json.loads(content)["games"]

    games_data = []
    for game in games:
        game_data = {}
        game_data["url"] = game["url"]
        ECOurl = game['pgn'].split("\n")[8]
        game_data["Opening"] = ECOurl[9:-2]

        termination = game['pgn'].split("\n")[16]
        if termination[14:26] == "rain1024 won":
            game_data["Result"] = "Won"
        elif termination[14:24] == "Game drawn":
            game_data["Result"] = "Draw"
        else:
            game_data["Result"] = "Lose"
        games_data.append(game_data)

    games_df = pd.DataFrame(games_data)
    return games_df


user_name = "rain1024"
month = "04"
year = "2020"
url = f"https://api.chess.com/pub/player/{user_name}/games/{year}/{month}"
games_df = load_games(user_name, month, year)

n = games_df.shape[0]
print(f"Analyze {n} games in {month}/{year}")

print()
print(games_df.groupby("Result").size().to_string())

print()
print("Most Opening when lose")
print(games_df[games_df["Result"] == "Lose"].groupby("Opening").size().sort_values(ascending=False)[:20].to_string())

print()
print("Most Opening when win")
print(games_df[games_df["Result"] == "Won"].groupby("Opening").size().sort_values(ascending=False)[:20].to_string())

print()
opening = "https://www.chess.com/openings/Scotch-Game...4.Nxd4-Nxd4-5.Qxd4-d6"
print(f"Game with opening {opening} when lose")
print(games_df[games_df["Opening"] == opening][games_df["Result"] == "Lose"]["url"].to_string(index=False))
