# 512. Game Play Analysis II
LeetCode: https://leetcode.com/problems/game-play-analysis-ii/ · Easy

## Problem
Return the `device_id` each player used on their first login day. Same `Activity` table as 511.

**Activity**
| Column | Type | Notes |
|---|---|---|
| player_id | int | part of the primary key |
| device_id | int | |
| event_date | date | part of the primary key |
| games_played | int | |

**Example**
```
player_id | device_id | event_date | games_played
1         | 2         | 2016-03-01 | 5
1         | 2         | 2016-05-02 | 6
2         | 3         | 2017-06-25 | 1
3         | 1         | 2016-03-02 | 0
3         | 4         | 2018-07-03 | 5

Output:
player_id | device_id
1         | 2
2         | 3
3         | 1
```
Player 1's first login was 03-01, on device 2, so the row for 05-02 (also device 2, but not the first day) doesn't matter here. Player 3's first login was 03-02, on device 1, not the 07-03 row on device 4.

## Solution
```python
import pandas as pd

def game_play_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    first_login = activity.groupby('player_id')['event_date'].transform('min')
    result = activity[activity['event_date'] == first_login]
    return result[['player_id', 'device_id']]
```

Tracing the example above:

1. `activity.groupby('player_id')['event_date'].transform('min')` computes each player's earliest date, same as in 511, but instead of collapsing to one row per player, it broadcasts that minimum back onto **every** row belonging to that player. So both of player 1's rows get `first_login = 2016-03-01` attached, not just one of them.
2. This is the key difference from 511: `groupby().min()` alone would give you the dates but lose the `device_id` that goes with them, since it collapses each group into a single row. `transform()` keeps the original row count so `device_id` is still there to grab.
3. `activity['event_date'] == first_login` keeps only the row where a player's actual `event_date` matches their computed minimum. For player 1 that's the 03-01 row (device 2); the 05-02 row fails the check and is dropped.
4. `result[['player_id', 'device_id']]` selects just the two required columns.

SQL equivalent:
```sql
SELECT player_id, device_id
FROM Activity
WHERE (player_id, event_date) IN (
    SELECT player_id, MIN(event_date) FROM Activity GROUP BY player_id
);
```
