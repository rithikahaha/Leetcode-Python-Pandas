# 196. Delete Duplicate Emails
LeetCode: https://leetcode.com/problems/delete-duplicate-emails/ · Easy

## Problem
`Person(id, email)`. Delete duplicate emails in place, keeping only the row with the smallest `id` for each email.

## Solution
```python
import pandas as pd

def delete_duplicate_emails(person: pd.DataFrame) -> None:
    person.sort_values('id', inplace=True)
    person.drop_duplicates(subset='email', keep='first', inplace=True)
```

`drop_duplicates(keep='first')` keeps whichever row it sees first, so sorting by `id` beforehand is what guarantees "first" means "smallest id" rather than whatever order the rows happened to arrive in. Both calls use `inplace=True` because the problem requires mutating `Person` directly rather than returning a new DataFrame.

SQL equivalent (a DELETE, since SQL has no in-place drop_duplicates):
```sql
DELETE p1 FROM Person p1
JOIN Person p2 ON p1.email = p2.email AND p1.id > p2.id;
```
