from pathlib import Path
import pandas as pd
from nba_api.stats.endpoints import scheduleleaguev2

SEASON = "2026-27"
COLUMNS = [
    "gameId", "gameDate", "gameStatus", "weekNumber",
    "homeTeam_teamId", "homeTeam_teamTricode",
    "awayTeam_teamId", "awayTeam_teamTricode",
]

def section(title):
    print(f"\n{'=' * 50}\n{title}\n{'=' * 50}")

def extract(season):
    # 1. pull the schedule (from explore script, using season as parameter)
    schedule = scheduleleaguev2.ScheduleLeagueV2(season=season, timeout=60)
    df = schedule.get_data_frames()[0]
    
    # 2. keep only regular season games
    is_regular = df["gameId"].str.startswith("002")
    df = df[is_regular]
    
    # 3. keep only COLUMNS
    df = df[COLUMNS]
    
    return df

if __name__ == "__main__":
    df = extract(SEASON)
    section("Shape")
    print(f"{df.shape[0]:,} rows x {df.shape[1]} columns")
    
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    df.to_parquet(f"data/raw/schedule_{SEASON}.parquet", index=False)
    
    section("Saved file preview")
    print(pd.read_parquet(f"data/raw/schedule_{SEASON}.parquet").head())