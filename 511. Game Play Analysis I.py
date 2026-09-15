# 511. Game Play Analysis I
LeetCode: https://leetcode.com/problems/game-play-analysis-i/ · Easy

## Problem
`Activity(player_id, device_id, event_date, games_played)`, primary key `(player_id, event_date)`. Return each player's first login date.

## Solution
```python
import pandas as pd

def game_play_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    return (
        activity.groupby('player_id')['event_date']
        .min()
        .reset_index(name='first_login')
    )
```

Straightforward `groupby` + `min`, mirroring `GROUP BY player_id, MIN(event_date)` in SQL. `reset_index(name='first_login')` turns the grouped Series back into a two-column DataFrame with the right output name; without it, `player_id` would stay stuck as the index instead of becoming a column.

SQL equivalent:
```sql
SELECT player_id, MIN(event_date) AS first_login
FROM Activity
GROUP BY player_id;
```
