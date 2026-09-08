# 196. Delete Duplicate Emails

**LeetCode:** [196. Delete Duplicate Emails](https://leetcode.com/problems/delete-duplicate-emails/)
**Difficulty:** Easy
**Language:** Python (Pandas)

---

## Problem

### Table: `Person`

```text
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| email       | varchar |
+-------------+---------+
```

* `id` is the primary key (column with unique values) for this table.
* Each row contains an email.
* The emails will not contain uppercase letters.

Write a solution to **delete all duplicate emails**, keeping only one unique email with the **smallest `id`**.

For Pandas users, the `Person` DataFrame must be **modified in place**.

After running the script, the answer shown is the `Person` table. The final order of the table does not matter.

---

## Example 1

### Input

```text
Person table:
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
| 3  | john@example.com |
+----+------------------+
```

### Output

```text
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
```

### Explanation

`john@example.com` appears twice.

* `id = 1` → keep
* `id = 3` → delete

We keep the row with the **smallest ID**.

---

# Pandas Solution

```python id="j4q7sx"
import pandas as pd

def delete_duplicate_emails(person: pd.DataFrame) -> None:
    person.sort_values('id', inplace=True)
    person.drop_duplicates(
        subset='email',
        keep='first',
        inplace=True
    )
```

---

# Explanation

The goal is to keep the row with the **smallest `id` for each email** and delete the remaining duplicates.

We can achieve this in two steps.

## Step 1: Sort by `id`

```python id="m8v2kp"
person.sort_values('id', inplace=True)
```

Sorting by `id` in ascending order puts the smallest ID first for each email.

For example:

```text
Before:

id   email
1    john@example.com
2    bob@example.com
3    john@example.com
```

The duplicate `john@example.com` rows are ordered as:

```text
id = 1
id = 3
```

so `id = 1` comes first.

---

## Step 2: Remove Duplicate Emails

```python id="r6c3wn"
person.drop_duplicates(
    subset='email',
    keep='first',
    inplace=True
)
```

* `subset='email'` checks for duplicates based only on the email column.
* `keep='first'` keeps the first occurrence and removes subsequent ones.
* Because we sorted by `id` first, the first occurrence has the **smallest ID**.
* `inplace=True` directly modifies `person`, as required by the problem.

After this operation:

```text
+----+------------------+
| id | email            |
+----+------------------+
| 1  | john@example.com |
| 2  | bob@example.com  |
+----+------------------+
```

---

# Important Pandas Concepts

### `sort_values()`

```python
person.sort_values('id', inplace=True)
```

Sorts rows by `id` in ascending order by default.

This is important because `drop_duplicates(keep='first')` keeps whichever duplicate appears first. Sorting first ensures that the row with the smallest ID is kept.

### `drop_duplicates()`

```python
person.drop_duplicates(
    subset='email',
    keep='first',
    inplace=True
)
```

Removes duplicate rows based on the specified column.

Here:

```text
subset='email'
```

means emails are used to determine duplicates.

```text
keep='first'
```

means the first occurrence is retained.

### `inplace=True`

The problem specifically requires modifying `Person` **in place**.

Therefore, instead of:

```python
person = person.drop_duplicates(...)
```

we use:

```python
person.drop_duplicates(..., inplace=True)
```

so the original DataFrame is directly changed.

---

# Why Do We Sort First?

Consider:

```text
id   email
3    john@example.com
1    john@example.com
2    bob@example.com
```

If we immediately use:

```python
person.drop_duplicates(subset='email', keep='first')
```

Pandas would keep `id = 3` because it happens to appear first.

But the problem requires the **smallest ID**, which is `1`.

Therefore:

```python
person.sort_values('id', inplace=True)
```

must happen first.

Then:

```text
id   email
1    john@example.com
2    bob@example.com
3    john@example.com
```

and `keep='first'` correctly keeps `id = 1`.

---

# SQL Equivalent

The SQL version requires a `DELETE` statement:

```sql id="t8p4vz"
DELETE p1
FROM Person p1
JOIN Person p2
    ON p1.email = p2.email
   AND p1.id > p2.id;
```

### How It Works

The table is joined with itself.

For duplicate emails:

```text
p1.email = p2.email
```

identifies rows containing the same email.

Then:

```text
p1.id > p2.id
```

identifies the row with the larger ID.

That larger-ID row is deleted, leaving the row with the smallest ID.

---

# Pandas vs SQL

| SQL                   | Pandas                               |
| --------------------- | ------------------------------------ |
| Self `JOIN`           | Not needed                           |
| `p1.email = p2.email` | `subset='email'`                     |
| Delete larger ID      | Keep first after sorting             |
| `p1.id > p2.id`       | `sort_values('id')`                  |
| `DELETE`              | `drop_duplicates(..., inplace=True)` |

---

# Common Mistakes

### 1. Using `drop_duplicates()` without sorting

```python
person.drop_duplicates(subset='email', inplace=True)
```

This may keep an arbitrary occurrence rather than the one with the smallest ID.

Sort by `id` first.

### 2. Using `keep='last'`

```python
keep='last'
```

would keep the row with the **largest ID** after ascending sorting.

We need:

```python
keep='first'
```

### 3. Forgetting `inplace=True`

The problem explicitly requires modifying `Person` in place.

Use:

```python
person.drop_duplicates(..., inplace=True)
```

rather than creating a separate result DataFrame.

---

# Key Takeaway

The core pattern is:

```text
Sort by ID
    ↓
Smallest ID appears first
    ↓
Drop duplicate emails
    ↓
Keep first occurrence
    ↓
Modify DataFrame in place
```

> **When you need to keep the row with the smallest value for each duplicate group, sort by that value first, then use `drop_duplicates(keep='first')`.**
