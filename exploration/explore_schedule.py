from nba_api.stats.endpoints import scheduleleaguev2

schedule = scheduleleaguev2.ScheduleLeagueV2(season="2026-27", timeout=60)
df = schedule.get_data_frames()[0]

print(df.shape)
print(df.columns.tolist())
print(df.head())
print(df["gameId"].str[:3].value_counts())