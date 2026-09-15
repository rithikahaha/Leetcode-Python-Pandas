# 175. Combine Two Tables
LeetCode: https://leetcode.com/problems/combine-two-tables/ · Easy

## Problem
Return `firstName, lastName, city, state` for every person in `Person`, even if they have no row in `Address` (city/state should be null in that case).

**Person**
| Column | Type | Notes |
|---|---|---|
| personId | int | primary key |
| lastName | varchar | |
| firstName | varchar | |

**Address**
| Column | Type | Notes |
|---|---|---|
| addressId | int | primary key |
| personId | int | foreign key to Person.personId |
| city | varchar | |
| state | varchar | |

**Example**
```
Person:  (1, Allen, Wang), (2, Bob, Alice)
Address: (1, personId=2, New York City, New York), (2, personId=3, Leetcode, California)

Output:
firstName | lastName | city          | state
Allen     | Wang     | null          | null
Bob       | Alice    | New York City | New York
```
Person 1 (Allen) has no address row, so city/state are null. Person 2 (Bob) matches address row 1. The address row for personId 3 doesn't correspond to anyone in Person, so it's irrelevant here.

## Solution
```python
import pandas as pd

def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    result = pd.merge(person, address, on='personId', how='left')
    return result[['firstName', 'lastName', 'city', 'state']]
```

Tracing the example above:

1. `pd.merge(person, address, on='personId', how='left')` matches `personId=2` to its address row, giving Bob the New York City/New York values.
2. `personId=1` has no match in `Address`. Because this is a **left** join, Allen's row is kept anyway; the merge just fills `city`/`state` with `NaN` for him instead of dropping the row. An inner join would have dropped Allen entirely.
3. The merged frame still carries `personId` and `addressId`, which aren't part of the required output, so `result[['firstName', 'lastName', 'city', 'state']]` narrows it down to just the four columns asked for.

SQL equivalent:
```sql
SELECT p.firstName, p.lastName, a.city, a.state
FROM Person p
LEFT JOIN Address a ON p.personId = a.personId;
```
