from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data"

SAVE_PATH = BASE_DIR / "out"

def process_season_history(player):
    season_data = []
    player_name = player['name']
    player_data = {
        "name": player['name'],
        "position": player["position"],
        "dob": player["dob"],
        "height": player["height"],
        "weight": player["weight"],
        "contract": player["contract"],
        "raw_price": player["raw_price"],
    }
    playing_history = player["playing_history"]
    for season in playing_history:
        season['player'] = player_name
        season_data.append(season)
    return (player_data, season_data)
    
def format_player_data(player_data):
    player_array = []
    season_data = []
    for obj in player_data:
        for key in obj:
            for player in obj[key]:
                pd, sd = process_season_history(player)
                pd['team'] = key
                player_array.append(pd)
                for o in sd:
                    season_data.append(o)
    return (player_array, season_data)

def read_player_data():
    try:
        with open(DATA_PATH / "player_data.json") as f:
            d = json.load(f)
            return d
    except:
        print("Error reading data from player_data.json file")

def save_new_data(player_data, season_data):
    try:
        with open(f"{SAVE_PATH}/player_data.json", 'w') as f:
            json.dump(player_data, f, ensure_ascii=False, indent=4)
        with open(f"{SAVE_PATH}/season_data.json", 'w') as file:
            json.dump(season_data, file, ensure_ascii=False, indent=4)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except FileExistsError as e:
        print(f"Error: {e}")

def main():
    input_player_data = read_player_data()
    player_data, season_data = format_player_data(input_player_data)
    save_new_data(player_data, season_data)

if __name__ == "__main__":
    main()