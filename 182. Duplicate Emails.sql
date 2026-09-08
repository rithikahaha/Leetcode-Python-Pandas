# 182. Duplicate Emails

**LeetCode:** [182. Duplicate Emails](https://leetcode.com/problems/duplicate-emails/)
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
* The `email` field is guaranteed to be **NOT NULL**.

Write a solution to report all the **duplicate emails**.

Return the result table in **any order**.

---

## Example 1

### Input

```text
Person table:
+----+---------+
| id | email   |
+----+---------+
| 1  | a@b.com |
| 2  | c@d.com |
| 3  | a@b.com |
+----+---------+
```

### Output

```text
+---------+
| Email   |
+---------+
| a@b.com |
+---------+
```

### Explanation

`a@b.com` appears twice in the table, so it is a duplicate.

`c@d.com` appears only once, so it is not included.

---

# Pandas Solution

```python id="q2p7kd"
import pandas as pd

def duplicate_emails(person: pd.DataFrame) -> pd.DataFrame:
    result = (
        person.groupby('email')
        .size()
        .reset_index(name='count')
    )

    result = result[result['count'] > 1]

    return result[['email']].rename(
        columns={'email': 'Email'}
    )
```

---

# Explanation

We need to find emails that occur **more than once**.

The simplest approach is to group the DataFrame by `email`, count how many rows belong to each email, and keep only counts greater than 1.

---

## Step 1: Group Emails and Count Occurrences

```python id="7v9n4s"
result = (
    person.groupby('email')
    .size()
    .reset_index(name='count')
)
```

### `groupby('email')`

Groups all rows with the same email together.

For the example:

```text
a@b.com → 2 rows
c@d.com → 1 row
```

### `.size()`

Counts the number of rows in each group.

Unlike `count()`, `.size()` counts rows regardless of whether individual columns contain missing values.

Here, it produces:

| email                     | count |
| ------------------------- | ----: |
| [a@b.com](mailto:a@b.com) |     2 |
| [c@d.com](mailto:c@d.com) |     1 |

### `.reset_index(name='count')`

`groupby().size()` initially returns a Series with `email` as its index.

`reset_index()` converts it back into a DataFrame and names the count column `count`.

---

## Step 2: Keep Only Duplicates

```python id="xj4m8n"
result = result[result['count'] > 1]
```

An email is a duplicate when it appears **more than once**.

Therefore:

```text
count > 1
```

keeps only:

| email                     | count |
| ------------------------- | ----: |
| [a@b.com](mailto:a@b.com) |     2 |

---

## Step 3: Select and Rename the Column

The required output contains only the email, with the column name `Email`:

```python id="z6w3kp"
return result[['email']].rename(
    columns={'email': 'Email'}
)
```

Final result:

```text
+---------+
| Email   |
+---------+
| a@b.com |
+---------+
```

---

# Important Pandas Concepts

### `groupby() + size()`

This is a common pattern for finding values that occur a certain number of times:

```python
df.groupby('column').size()
```

For duplicates, filter the resulting counts:

```python
df.groupby('column').size() > 1
```

### `reset_index()`

Converts grouped index values back into regular DataFrame columns.

```python
.reset_index(name='count')
```

also gives the resulting count column a meaningful name.

### Boolean Filtering

```python
result[result['count'] > 1]
```

keeps only rows satisfying the condition.

---

# Alternative Pandas Solution

We can also use `duplicated()`:

```python id="r5j9wx"
import pandas as pd

def duplicate_emails(person: pd.DataFrame) -> pd.DataFrame:
    result = person[person['email'].duplicated(keep=False)]

    return result[['email']].drop_duplicates().rename(
        columns={'email': 'Email'}
    )
```

### How It Works

```python
person['email'].duplicated(keep=False)
```

marks **every occurrence** of an email that appears more than once as `True`.

`keep=False` is important because the default behavior marks only later occurrences as duplicates.

For example:

```text
a@b.com → True
c@d.com → False
a@b.com → True
```

Then:

```python
.drop_duplicates()
```

ensures that each duplicate email appears only once in the output.

---

# SQL Equivalent

The same logic can be written in SQL as:

```sql
SELECT
    email AS Email
FROM Person
GROUP BY email
HAVING COUNT(*) > 1;
```

| SQL                   | Pandas             |
| --------------------- | ------------------ |
| `GROUP BY email`      | `groupby('email')` |
| `COUNT(*)`            | `.size()`          |
| `HAVING COUNT(*) > 1` | Boolean filtering  |
| `email AS Email`      | Select + rename    |

---

# Common Mistakes

### 1. Using `COUNT`-style logic without grouping

You need to determine the frequency **for each email**, so the emails must first be grouped.

### 2. Forgetting to remove repeated output rows

If using `duplicated(keep=False)`, every occurrence of a duplicate is retained. Use:

```python
.drop_duplicates()
```

to return each duplicate email only once.

### 3. Using `duplicated()` without `keep=False`

```python
person['email'].duplicated()
```

marks only subsequent occurrences as duplicates.

For example:

```text
a@b.com → False
c@d.com → False
a@b.com → True
```

That would miss the first occurrence of `a@b.com`.

---

# Key Takeaway

The main pattern is:

```text
Group by email
    ↓
Count occurrences
    ↓
Keep count > 1
    ↓
Return each duplicate email
```

The most SQL-like Pandas solution is:

```python
person.groupby('email').size()
```

> **`groupby() + size() + filtering` is a fundamental Pandas pattern for finding duplicate or frequently occurring values.**
