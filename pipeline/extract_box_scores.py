from pathlib import Path
import pandas as pd
from nba_api.stats.endpoints import leaguegamelog

SEASON = "2026-27"
COLUMNS = [
    "SEASON_ID", "PLAYER_ID", "PLAYER_NAME", "TEAM_ID", "TEAM_ABBREVIATION",
    "GAME_ID", "GAME_DATE", "MATCHUP", "MIN",
    "PTS", "REB", "OREB", "DREB", "AST", "STL", "BLK", "TOV", "FGM", "FGA", "FG3M", "FTM", "FTA"
]

def section(title):
    print(f"\n{'=' * 50}\n{title}\n{'=' * 50}")

def extract(season):
    # 1. pull the season's player game logs (copy from explore script,
    #    but use the same parameter instead of a hardcoded string)
    logs = leaguegamelog.LeagueGameLog(
        season=season,
        player_or_team_abbreviation="P", # P = player rows, T = team rows
        season_type_all_star="Regular Season",
        timeout=60,
    )
    df = logs.get_data_frames()[0]
    # 2. keep only COLUMNS
    df = df[COLUMNS]
    # 3. return the dataframe
    return df

if __name__ == "__main__":
    df = extract(SEASON)
    # print the shape to sanity-check it
    section("Shape")
    print(f"{df.shape[0]:,} rows x {df.shape[1]} columns")
    
    # make sure data/raw exists (Path(...).mkdir)
    # save to data/raw/box_scores_{SEASON}.parquet with index=False
    Path("data/raw").mkdir(parents=True, exist_ok=True)         
    df.to_parquet(f"data/raw/box_scores_{SEASON}.parquet", index=False)  
    
    # print DB Head
    section("Saved file preview")
    print(pd.read_parquet(f"data/raw/box_scores_{SEASON}.parquet").head())