from nba_api.stats.endpoints import leaguegamelog
# Information on the data
# 26,651 rows including player individual game stats 
# 582 unique players
# 1,230 unique games

logs = leaguegamelog.LeagueGameLog(
    season="2025-26",
    player_or_team_abbreviation="P", # P = player rows, T = team rows
    season_type_all_star="Regular Season",
    timeout=60,
)
df = logs.get_data_frames()[0]

print(df.shape)
print(df.columns.tolist())
print(df.head())

print(df["PLAYER_ID"].nunique(), "unique players")
print(df["GAME_ID"].nunique(), "unique games")
print(df.duplicated(subset=["PLAYER_ID", "GAME_ID"]).sum(), "duplicate player-games")
