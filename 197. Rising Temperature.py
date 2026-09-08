# 197. Rising Temperature

**LeetCode:** [197. Rising Temperature](https://leetcode.com/problems/rising-temperature/)
**Difficulty:** Easy
**Language:** Python (Pandas)

---

## Problem

### Table: `Weather`

```text
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| recordDate    | date    |
| temperature   | int     |
+---------------+---------+
```

* `id` is the column with unique values.
* There are no different rows with the same `recordDate`.
* Each row contains the temperature recorded on a certain day.

Write a solution to find the `id` of every date where the temperature was **higher than the previous day (yesterday)**.

Return the result table in **any order**.

---

## Example 1

### Input

```text
Weather table:
+----+------------+-------------+
| id | recordDate | temperature |
+----+------------+-------------+
| 1  | 2015-01-01 | 10          |
| 2  | 2015-01-02 | 25          |
| 3  | 2015-01-03 | 20          |
| 4  | 2015-01-04 | 30          |
+----+------------+-------------+
```

### Output

```text
+----+
| id |
+----+
| 2  |
| 4  |
+----+
```

### Explanation

* `2015-01-02`: `25 > 10` → include `id = 2`
* `2015-01-03`: `20 > 25` → exclude
* `2015-01-04`: `30 > 20` → include `id = 4`

Therefore, the answer is:

```text
2
4
```

---

# Pandas Solution

```python id="p9k4mz"
import pandas as pd

def rising_temperature(weather: pd.DataFrame) -> pd.DataFrame:
    weather = weather.sort_values('recordDate')

    weather['previous_date'] = weather['recordDate'].shift(1)
    weather['previous_temp'] = weather['temperature'].shift(1)

    result = weather[
        (weather['recordDate'] - weather['previous_date']).dt.days.eq(1)
        & (weather['temperature'] > weather['previous_temp'])
    ]

    return result[['id']]
```

---

# Explanation

We need to compare each day's temperature with the temperature from **exactly one day earlier**.

We first sort by date, then use `shift(1)` to access the previous row.

## Step 1: Sort by Date

```python id="5s6v2r"
weather = weather.sort_values('recordDate')
```

This ensures the rows are in chronological order, so the previous row represents the previous recorded date.

---

## Step 2: Get the Previous Date and Temperature

```python id="z4p7cw"
weather['previous_date'] = weather['recordDate'].shift(1)
weather['previous_temp'] = weather['temperature'].shift(1)
```

`shift(1)` moves values down by one row, allowing each row to access the values from the previous row.

For example:

| recordDate | temperature | previous_date | previous_temp |
| ---------- | ----------: | ------------- | ------------: |
| 2015-01-01 |          10 | NaT           |           NaN |
| 2015-01-02 |          25 | 2015-01-01    |            10 |
| 2015-01-03 |          20 | 2015-01-02    |            25 |
| 2015-01-04 |          30 | 2015-01-03    |            20 |

---

## Step 3: Make Sure It Is Actually Yesterday

```python id="u8m2sd"
(weather['recordDate'] - weather['previous_date']).dt.days.eq(1)
```

The problem specifically asks for the **previous day**, not simply the previous available record.

For example, if the dates were:

```text
2015-01-01
2015-01-03
```

then `2015-01-03` should **not** be compared with `2015-01-01`, because January 2 is missing.

The date difference must therefore equal exactly `1` day.

---

## Step 4: Compare Temperatures

```python id="q2v7nx"
weather['temperature'] > weather['previous_temp']
```

This identifies days where the temperature is higher than the previous day's temperature.

---

## Step 5: Combine the Conditions

```python id="j6s4yc"
result = weather[
    (weather['recordDate'] - weather['previous_date']).dt.days.eq(1)
    & (weather['temperature'] > weather['previous_temp'])
]
```

Both conditions must be true:

```text
Previous date is exactly yesterday
                AND
Today's temperature > yesterday's temperature
```

---

## Step 6: Return the Required Column

```python id="n3r8kp"
return result[['id']]
```

The problem only requires the `id` column.

---

# Important Pandas Concepts

### `sort_values()`

```python id="f8q2mv"
weather.sort_values('recordDate')
```

Sorts the rows chronologically so that `shift(1)` can access the previous date.

### `shift(1)`

```python id="h3k7px"
weather['temperature'].shift(1)
```

moves values down one row, effectively giving each row access to the previous row's value.

This is useful for **comparing consecutive rows**.

### Date Difference

```python id="r5n9wc"
(weather['recordDate'] - weather['previous_date']).dt.days.eq(1)
```

checks whether the previous recorded date is exactly one day earlier.

### Boolean Filtering

```python id="w6m2kd"
condition1 & condition2
```

keeps rows where both conditions are `True`.

In Pandas, `&` is used for element-wise **AND** between conditions.

---

# SQL Equivalent

The same logic can be written using a self-join:

```sql id="c7x4pn"
SELECT
    w1.id
FROM Weather w1
JOIN Weather w2
    ON w1.recordDate = DATE_ADD(w2.recordDate, INTERVAL 1 DAY)
WHERE w1.temperature > w2.temperature;
```

Here:

```text
w1 = today's record
w2 = yesterday's record
```

The join ensures:

```text
w1.recordDate = w2.recordDate + 1 day
```

and the `WHERE` condition checks whether today's temperature is higher.

---

# Pandas vs SQL

| SQL                               | Pandas                              |
| --------------------------------- | ----------------------------------- |
| `DATE_ADD(..., INTERVAL 1 DAY)`   | Date subtraction + `.dt.days.eq(1)` |
| Self `JOIN`                       | `shift(1)`                          |
| `w1.temperature > w2.temperature` | `temperature > previous_temp`       |
| `SELECT w1.id`                    | `result[['id']]`                    |

---

# Common Mistakes

### 1. Using Only `shift()` Without Checking the Date

```python id="p6v8rm"
weather['temperature'] > weather['temperature'].shift(1)
```

This compares with the previous **row**, not necessarily yesterday.

If a date is missing, the comparison would be incorrect.

### 2. Forgetting to Sort by Date

Without:

```python id="a3n7qx"
weather.sort_values('recordDate')
```

`shift(1)` may compare rows that are not chronologically adjacent.

### 3. Using `>` in the Wrong Direction

We need:

```python id="m2c8vk"
today's temperature > yesterday's temperature
```

not:

```python id="v9r4js"
yesterday's temperature > today's temperature
```

---

# Key Takeaway

The core pattern is:

```text
Sort by date
    ↓
Use shift(1) to get the previous row
    ↓
Check that the previous date is exactly yesterday
    ↓
Compare today's temperature with yesterday's
    ↓
Return the qualifying IDs
```

> **`shift()` is useful for comparing consecutive rows, but when the problem requires consecutive dates, always verify that the date difference is exactly one day.**
