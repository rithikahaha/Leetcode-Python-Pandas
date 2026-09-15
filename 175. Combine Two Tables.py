# 175. Combine Two Tables
LeetCode: https://leetcode.com/problems/combine-two-tables/ · Easy

## Problem
Return `firstName, lastName, city, state` for every person in `Person`, even if they have no row in `Address` (city/state should be null in that case).

- **Person**: personId (PK), lastName, firstName
- **Address**: addressId (PK), personId (FK), city, state

## Solution
```python
import pandas as pd

def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    result = pd.merge(person, address, on='personId', how='left')
    return result[['firstName', 'lastName', 'city', 'state']]
```

`person` has to be the left side of the merge since it's the table whose rows must survive regardless of a match. `how='left'` keeps every person and fills `city`/`state` with NaN when there's no matching address; an inner join would silently drop anyone without one. Double brackets on the final select matter too, since a single bracket returns a Series instead of a DataFrame.

SQL equivalent:
```sql
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person p
LEFT JOIN Address a ON p.personId = a.personId;
```
