# 512. Game Play Analysis II

**LeetCode:** [512. Game Play Analysis II](https://leetcode.com/problems/game-play-analysis-ii/)
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

* `(player_id, event_date)` is the primary key (combination of columns with unique values) for this table.
* Each row records a player who logged in and played a number of games before logging out on a particular day.
* A player can use different devices on different days.

Write a solution to find the **device that each player used on their first login day**.

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

+-----------+-----------+
| player_id | device_id |
+-----------+-----------+
| 1         | 2         |
| 2         | 3         |
| 3         | 1         |
+-----------+-----------+
```

### Explanation

* Player 1 first logged in on `2016-03-01` using device `2`.
* Player 2 first logged in on `2017-06-25` using device `3`.
* Player 3 first logged in on `2016-03-02` using device `1`.

---

# Pandas Solution

import pandas as pd

def game_play_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    first_login = activity.groupby('player_id')['event_date'].transform('min')

    result = activity[
        activity['event_date'] == first_login
    ]

    return result[['player_id', 'device_id']]
```

---

# Explanation

We need to find each player's **earliest login date**, then return the `device_id` from that same row.

Unlike LeetCode 511, where we only needed the first date, this problem also requires another column from the original row. Therefore, `transform('min')` is useful because it calculates each player's minimum date while keeping the original DataFrame's row structure.

## Step 1: Find Each Player's First Login Date

first_login = activity.groupby('player_id')['event_date'].transform('min')
```

* `groupby('player_id')` groups the activity records by player.
* `transform('min')` finds the earliest `event_date` for each player and places that value alongside **every row belonging to that player**.

This produces values like:

| player_id | event_date | first_login |
| --------: | ---------- | ----------- |
|         1 | 2016-03-01 | 2016-03-01  |
|         1 | 2016-05-02 | 2016-03-01  |
|         2 | 2017-06-25 | 2017-06-25  |
|         3 | 2016-03-02 | 2016-03-02  |
|         3 | 2018-07-03 | 2016-03-02  |

---

## Step 2: Keep the First-Login Rows
    
result = activity[
    activity['event_date'] == first_login
]
```

This compares each activity date with that player's earliest date.

Only the first-login rows remain:

| player_id | device_id | event_date |
| --------: | --------: | ---------- |
|         1 |         2 | 2016-03-01 |
|         2 |         3 | 2017-06-25 |
|         3 |         1 | 2016-03-02 |

---

## Step 3: Select the Required Columns

return result[['player_id', 'device_id']]
```

The problem only requires `player_id` and `device_id`.

---

# Important Pandas Concepts

### `groupby() + transform()`

activity.groupby('player_id')['event_date'].transform('min')
```

`groupby()` performs the calculation separately for each player.

`transform()` is important because it returns a Series with the **same number of rows as the original DataFrame**.

This allows the calculated first-login date to be compared directly with the original `event_date` column.

### Why Not `groupby().min()`?

This:

activity.groupby('player_id')['event_date'].min()
```

would return only one date per player.

That works for finding the first date, but we also need the `device_id` from the original row. `transform()` allows us to identify and retain that original row.

### Boolean Filtering

activity['event_date'] == first_login
```

creates a Boolean condition that identifies the rows occurring on each player's first login date.

---

# SQL Equivalent

SELECT
    player_id,
    device_id
FROM Activity
WHERE (player_id, event_date) IN (
    SELECT
        player_id,
        MIN(event_date)
    FROM Activity
    GROUP BY player_id
);
```

The subquery finds each player's earliest login date. The outer query then retrieves the device used on that date.

---

# Pandas vs SQL

| SQL                           | Pandas                         |
| ----------------------------- | ------------------------------ |
| `GROUP BY player_id`          | `groupby('player_id')`         |
| `MIN(event_date)`             | `transform('min')`             |
| Match first-login date        | Boolean filtering              |
| `SELECT player_id, device_id` | `[['player_id', 'device_id']]` |

---

# Common Mistakes

### 1. Using `groupby().min()` and losing the original row

```python
activity.groupby('player_id')['event_date'].min()
```

returns the dates but not the corresponding `device_id`.

Use `transform('min')` when you need to use the group-level result to filter the original DataFrame.

### 2. Using `max()` instead of `min()`

```python
transform('max')
```

would find the **last** login date.

The problem asks for the **first** login, so use:

```python
transform('min')
```

### 3. Grouping by `device_id`

A player can use different devices, so the grouping must be based on:

```python
'player_id'
```

not:

```python
['player_id', 'device_id']
```

# Key Takeaway

The core pattern is:

Group by player
    ↓
Find minimum date with transform()
    ↓
Compare with original dates
    ↓
Keep first-login rows
    ↓
Return player_id + device_id

> **Use `groupby().transform()` when you need a group-level calculation while keeping the original rows available for filtering or retrieving other columns.**
