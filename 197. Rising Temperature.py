# 197. Rising Temperature
LeetCode: https://leetcode.com/problems/rising-temperature/ · Easy

## Problem
`Weather(id, recordDate, temperature)`. Return the `id`s of every day whose temperature is higher than the previous calendar day's.

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

Sort by date first so `shift(1)` actually lines up each row with yesterday's row rather than an arbitrary one. The date-difference check matters because the table can have gaps. If Jan 2 is missing, Jan 3 shouldn't get compared against Jan 1 just because it happens to be the previous row. Both conditions, exactly one day apart and a higher temperature, have to hold together.

SQL equivalent:
```sql
SELECT w1.id
FROM Weather w1
JOIN Weather w2 ON w1.recordDate = DATE_ADD(w2.recordDate, INTERVAL 1 DAY)
WHERE w1.temperature > w2.temperature;
```
