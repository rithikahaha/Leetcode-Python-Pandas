# 511. Game Play Analysis I

**LeetCode:** [511. Game Play Analysis I](https://leetcode.com/problems/game-play-analysis-i/)
**Difficulty:** Easy
**Language:** Python (Pandas)

---

## Problem

### Table: `Activity`

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| player_id    | int     |
| device_id    | int     |
| event_date   | date    |
| games_played | int     |
+--------------+---------+
```

* `(player_id, event_date)` is the primary key.
* Each row records a player who logged in and played some number of games before logging out.
* A player may use different devices on different dates.

Write a solution to find the **first login date** for each player.

Return the result table in **any order**.

---

## Example 1

### Input

Activity table:
+-----------+-----------+------------+--------------+
| player_id | device_id | event_date | games_played |
+-----------+-----------+------------+--------------+
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-05-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |
+-----------+-----------+------------+--------------+
```

### Output

+-----------+-------------+
| player_id | first_login |
+-----------+-------------+
| 1         | 2016-03-01  |
| 2         | 2017-06-25  |
| 3         | 2016-03-02  |
+-----------+-------------+
```

### Explanation

For each player, find the earliest `event_date`:

* Player 1 → `2016-03-01`
* Player 2 → `2017-06-25`
* Player 3 → `2016-03-02`

---

# Pandas Solution

import pandas as pd

def game_play_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    result = (
        activity.groupby('player_id')['event_date']
        .min()
        .reset_index(name='first_login')
    )

    return result
```

---

# Explanation

We need to find the **minimum login date for each player**.

The combination of `groupby()` and `min()` directly matches the SQL logic of:

GROUP BY player_id
MIN(event_date)
```

## Step 1: Group by Player

activity.groupby('player_id')['event_date']
```

This groups all activity records belonging to the same player and selects the `event_date` column.

For example:

Player 1 → 2016-03-01, 2016-05-02
Player 2 → 2017-06-25
Player 3 → 2016-03-02, 2018-07-03
```

## Step 2: Find the Earliest Date

.min()
```

returns the earliest date within each player's group.

This gives:

| player_id | event_date |
| --------: | ---------- |
|         1 | 2016-03-01 |
|         2 | 2017-06-25 |
|         3 | 2016-03-02 |

## Step 3: Convert the Result to a DataFrame

.reset_index(name='first_login')
```

`groupby()` produces a Series with `player_id` as its index. `reset_index()` converts it back into a DataFrame and names the resulting date column `first_login`.

---

# Important Pandas Concepts

### `groupby() + min()`

This is a common pattern for finding the minimum value within each group:

df.groupby('group_column')['value_column'].min()
```

Here:

activity.groupby('player_id')['event_date'].min()
```

means:

> For each player, find their earliest event date.

### `reset_index()`

After `groupby()`, the grouping column becomes the index.

.reset_index(name='first_login')
```

turns it back into a regular column and gives the aggregated column its required name.

---

# SQL Equivalent

SELECT
    player_id,
    MIN(event_date) AS first_login
FROM Activity
GROUP BY player_id;
```

| SQL                  | Pandas                            |
| -------------------- | --------------------------------- |
| `GROUP BY player_id` | `groupby('player_id')`            |
| `MIN(event_date)`    | `.min()`                          |
| `AS first_login`     | `reset_index(name='first_login')` |

---

# Common Mistakes

### 1. Using `MAX()` Instead of `MIN()`

activity.groupby('player_id')['event_date'].max()
```

would return the **last** login date.

The problem asks for the **first**, so use:

.min()
```

### 2. Grouping by `device_id`

A player can use multiple devices, so the grouping should be based only on:

'player_id'
```

not:

['player_id', 'device_id']
```

### 3. Forgetting to Group

Simply using:

activity['event_date'].min()
```

would return one earliest date for the **entire DataFrame**, rather than one date for each player.

---

# Key Takeaway

The core pattern is:

Group by player
    ↓
Find minimum event_date
    ↓
Rename it first_login
```

> **`groupby() + min()` is the standard Pandas pattern for finding the earliest value for each group.**
