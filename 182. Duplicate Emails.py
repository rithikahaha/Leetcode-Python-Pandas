# 182. Duplicate Emails
LeetCode: https://leetcode.com/problems/duplicate-emails/ · Easy

## Problem
Return every email that appears more than once in `Person`.

**Person**
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| email | varchar | no uppercase letters, never null |

**Example**
```
id | email
1  | a@b.com
2  | c@d.com
3  | a@b.com

Output: Email = a@b.com
```
`a@b.com` shows up on rows 1 and 3, so it's a duplicate. `c@d.com` only shows up once, so it's excluded.

## Solution
```python
import pandas as pd

def duplicate_emails(person: pd.DataFrame) -> pd.DataFrame:
    counts = person.groupby('email').size().reset_index(name='count')
    result = counts[counts['count'] > 1]
    return result[['email']].rename(columns={'email': 'Email'})
```

Tracing the example above:

1. `person.groupby('email').size()` buckets rows by email and counts them: `a@b.com` has 2 rows, `c@d.com` has 1. (`.size()` counts rows per group regardless of nulls; `.count()` would instead count non-null values per column, which isn't what's needed here.)
2. `.reset_index(name='count')` turns that grouped result, which starts out as a Series indexed by `email`, back into a normal two-column DataFrame: `email | count`.
3. `counts[counts['count'] > 1]` keeps only `a@b.com`, since it's the only row with count 2.
4. `rename(columns={'email': 'Email'})` matches LeetCode's expected output column name.

A one-liner alternative: `person[person['email'].duplicated(keep=False)][['email']].drop_duplicates()`. The `keep=False` part matters there too: plain `duplicated()` only flags the second and later occurrences of a value, so on its own it would miss the very first `a@b.com` row.

SQL equivalent:
```sql
SELECT email AS Email FROM Person GROUP BY email HAVING COUNT(*) > 1;
```
