# 197. Rising Temperature
LeetCode: https://leetcode.com/problems/rising-temperature/ · Easy

## Problem
Return the `id`s of every day whose temperature is higher than the temperature exactly one calendar day earlier.

**Weather**
| Column | Type | Notes |
|---|---|---|
| id | int | unique |
| recordDate | date | no two rows share the same date |
| temperature | int | |

**Example**
```
id | recordDate | temperature
1  | 2015-01-01 | 10
2  | 2015-01-02 | 25
3  | 2015-01-03 | 20
4  | 2015-01-04 | 30

Output: id = 2, 4
```
01-02 (25) is warmer than 01-01 (10), so id 2 qualifies. 01-03 (20) is cooler than 01-02 (25), so it doesn't. 01-04 (30) is warmer than 01-03 (20), so id 4 qualifies.

## Solution
```python
import pandas as pd

def rising_temperature(weather: pd.DataFrame) -> pd.DataFrame:
    weather = weather.sort_values('recordDate')
    prev_date = weather['recordDate'].shift(1)
    prev_temp = weather['temperature'].shift(1)

    result = weather[
        (weather['recordDate'] - prev_date).dt.days.eq(1)
        & (weather['temperature'] > prev_temp)
    ]
    return result[['id']]
```

Tracing the example above:

1. `weather.sort_values('recordDate')` puts the rows in chronological order (already true here, but essential if the input weren't sorted), so that "the previous row" actually means "the previous day."
2. `shift(1)` moves each column down by one row. So the row for 01-02 picks up `prev_date=01-01` and `prev_temp=10`, the row for 01-03 picks up `prev_date=01-02, prev_temp=25`, and so on. The very first row (01-01) has nothing above it, so its `prev_date`/`prev_temp` come out as NaT/NaN.
3. `(recordDate - prev_date).dt.days.eq(1)` checks that the previous row really is exactly one day earlier, not just whatever row happens to sit above it. If the table skipped 01-02 entirely and jumped straight to 01-03, this check would correctly refuse to compare 01-03 against 01-01, since they're two days apart.
4. `temperature > prev_temp` is the actual comparison. For 01-02: 25 > 10 and exactly one day after 01-01, so it's kept. For 01-03: 20 is not > 25, so it's dropped regardless of the date check. For 01-04: 30 > 20 and one day after 01-03, so it's kept.
5. `result[['id']]` returns just the `id` column, giving `2, 4`.

SQL equivalent:
```sql
SELECT w1.id
FROM Weather w1
JOIN Weather w2 ON w1.recordDate = DATE_ADD(w2.recordDate, INTERVAL 1 DAY)
WHERE w1.temperature > w2.temperature;
```
