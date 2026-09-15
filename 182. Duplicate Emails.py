# 182. Duplicate Emails
LeetCode: https://leetcode.com/problems/duplicate-emails/ · Easy

## Problem
`Person(id, email)`. Return every email that appears more than once.

## Solution
```python
import pandas as pd

def duplicate_emails(person: pd.DataFrame) -> pd.DataFrame:
    counts = person.groupby('email').size().reset_index(name='count')
    result = counts[counts['count'] > 1]
    return result[['email']].rename(columns={'email': 'Email'})
```

`groupby('email').size()` counts rows per email (`.size()` counts rows regardless of nulls, unlike `.count()`), and `reset_index()` turns the grouped Series back into a DataFrame so it can be filtered and renamed like a normal one.

A one-liner alternative: `person[person['email'].duplicated(keep=False)][['email']].drop_duplicates()`. The `keep=False` part matters there too: plain `duplicated()` only flags the second and later occurrences of a value, so it misses the first one.

SQL equivalent:
```sql
SELECT email AS Email FROM Person GROUP BY email HAVING COUNT(*) > 1;
```
