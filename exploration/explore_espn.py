import os 
from dotenv import load_dotenv
from espn_api.basketball import League

load_dotenv()

league = League(
    league_id=2123524863,
    year=2027,
    espn_s2=os.getenv("ESPN_S2"),
    swid=os.getenv("ESPN_SWID"),
)

print("Teams:", len(league.teams))

my_team = next(t for t in league.teams if t.team_id == 7)
print("My team:", my_team.team_name)
for player in my_team.roster:
    print(player.name, player.position, player.proTeam, player.injuryStatus)
    
print("\nScoring settings:")
print(league.settings.scoring_type if hasattr(league.settings, "scoring_type") else league.settings.__dict__.keys())

print("\nTop free agents:")
for player in league.free_agents(size=10):
    print(player.name, player.position, player.proTeam, player.injuryStatus)