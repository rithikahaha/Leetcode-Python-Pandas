# 512. Game Play Analysis II
LeetCode: https://leetcode.com/problems/game-play-analysis-ii/ · Easy

## Problem
Same `Activity` table as 511. Return the `device_id` each player used on their first login day.

## Solution
```python
import pandas as pd

def game_play_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    first_login = activity.groupby('player_id')['event_date'].transform('min')
    result = activity[activity['event_date'] == first_login]
    return result[['player_id', 'device_id']]
```

The difference from 511 is that this one needs a column (`device_id`) from the original row, not just the aggregated date. Plain `groupby().min()` collapses to one row per player and loses that. `transform('min')` instead broadcasts each player's minimum date back onto every one of their rows, so it can be compared directly against `event_date` to pick out the matching row.

SQL equivalent:
```sql
SELECT player_id, device_id
FROM Activity
WHERE (player_id, event_date) IN (
    SELECT player_id, MIN(event_date) FROM Activity GROUP BY player_id
);
```
