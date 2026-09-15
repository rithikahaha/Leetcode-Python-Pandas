# 196. Delete Duplicate Emails
LeetCode: https://leetcode.com/problems/delete-duplicate-emails/ · Easy

## Problem
Delete duplicate emails from `Person` **in place**, keeping only the row with the smallest `id` for each email. Row order in the final table doesn't matter.

**Person**
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| email | varchar | no uppercase letters |

**Example**
```
id | email
1  | john@example.com
2  | bob@example.com
3  | john@example.com

Output (after deletion):
id | email
1  | john@example.com
2  | bob@example.com
```
`john@example.com` appears on rows 1 and 3. Row 1 has the smaller id, so row 3 gets deleted.

## Solution
```python
import pandas as pd

def delete_duplicate_emails(person: pd.DataFrame) -> None:
    person.sort_values('id', inplace=True)
    person.drop_duplicates(subset='email', keep='first', inplace=True)
```

Tracing the example above (imagine the rows arrived out of order, as `id=3` first, then `id=1`, then `id=2`, to see why the sort matters):

1. `person.sort_values('id', inplace=True)` puts the rows back in ascending `id` order: 1, 2, 3. Now the first time Pandas encounters `john@example.com` while scanning top to bottom is guaranteed to be the smallest-id copy.
2. `drop_duplicates(subset='email', keep='first', inplace=True)` scans in that order and, for each email, keeps only the first row it sees and drops the rest. For `john@example.com` that keeps `id=1` and drops `id=3`. `bob@example.com` only appears once, so it's untouched.
3. `inplace=True` on both calls is what makes this mutate the `person` DataFrame directly, since the problem asks for an in-place edit rather than a new returned table.

SQL equivalent (a DELETE, since SQL has no in-place drop_duplicates):
```sql
DELETE p1 FROM Person p1
JOIN Person p2 ON p1.email = p2.email AND p1.id > p2.id;
```
