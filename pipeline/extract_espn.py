import os
from pathlib import Path
import pandas as pd
import yaml
from dotenv import load_dotenv
from espn_api.basketball import League

load_dotenv()


def player_row(player, lg, roster_type):
    return {
        "platform": lg["platform"],
        "league_id": lg["league_id"],
        "league_name": lg["league_name"],
        "roster_type": roster_type,
        "espn_player_id": player.playerId,
        "player_name": player.name,
        "pro_team": player.proTeam,
        "position": player.position,
        "eligible_slots": player.eligibleSlots,
        "lineup_slot": player.lineupSlot,
        "injury_status": player.injuryStatus,
        "expected_return_date": player.expected_return_date,
        "espn_avg_points": player.avg_points,
        # ... fill in the rest from the table above
    }
    

def extract():
    with open("leagues.yml") as f:
        config = yaml.safe_load(f) # turns the YAML file into a Python dict
        
    rows = []
    for lg in config["leagues"]:
        league = League(
            league_id=int(lg["league_id"]),
            year=lg["season"],
            espn_s2=os.getenv("ESPN_S2"),
            swid=os.getenv("ESPN_SWID"),
        )
        my_team = next(t for t in league.teams if t.team_id == lg["my_team_id"])
        
        for player in my_team.roster:
            rows.append(player_row(player, lg, "my_team"))
        for player in league.free_agents(size=150):
            rows.append(player_row(player, lg, "free_agent"))
    
    return pd.DataFrame(rows)



if __name__ == "__main__":
    df = extract()
    print(df.shape)
    print(df["roster_type"].value_counts())
    print(df.groupby(["league_name", "roster_type"]).size())
    print(df.duplicated(subset=["league_id", "espn_player_id"]).sum(), "duplicate player_league rows")
    Path("data/raw").mkdir(parents=True, exist_ok=True)
    df.to_parquet("data/raw/espn_players.parquet", index=False)
    
