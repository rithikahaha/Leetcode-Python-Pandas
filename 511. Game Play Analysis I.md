# 511. Game Play Analysis I
LeetCode: https://leetcode.com/problems/game-play-analysis-i/ · Easy

## Problem
Return each player's first login date.

**Activity**
| Column | Type | Notes |
|---|---|---|
| player_id | int | part of the primary key |
| device_id | int | |
| event_date | date | part of the primary key |
| games_played | int | |

Primary key is `(player_id, event_date)`. A player can use different devices on different days.

**Example**
```
player_id | device_id | event_date | games_played
1         | 2         | 2016-03-01 | 5
1         | 2         | 2016-05-02 | 6
2         | 3         | 2017-06-25 | 1
3         | 1         | 2016-03-02 | 0
3         | 4         | 2018-07-03 | 5

Output:
player_id | first_login
1         | 2016-03-01
2         | 2017-06-25
3         | 2016-03-02
```
Player 1 has two rows (03-01 and 05-02); the earlier one is 03-01. Players 2 and 3 follow the same logic.

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

Tracing the example above:

1. `activity.groupby('player_id')` buckets the rows by player: player 1's two rows (03-01, 05-02) end up in one group, player 3's two rows (03-02, 07-03) in another.
2. `['event_date'].min()` takes the earliest date within each group: `2016-03-01` for player 1, `2016-03-02` for player 3.
3. `.reset_index(name='first_login')` converts the grouped result, which starts as a Series indexed by `player_id`, into a proper two-column DataFrame named `player_id | first_login`. Without it, `player_id` would be stuck as the index instead of an actual column.

SQL equivalent:
```sql
SELECT player_id, MIN(event_date) AS first_login
FROM Activity
GROUP BY player_id;
```
