# 175. Combine Two Tables

> **Difficulty:** Easy
> **Language:** Python (Pandas)

## Problem

We need to combine the `Person` and `Address` tables and return:

* `firstName`
* `lastName`
* `city`
* `state`

The important requirement is:

> **Every person in the `Person` table must appear in the result, even if they don't have an address.**

If a person has no matching address, `city` and `state` should be `null`.

### Table: `Person`

| Column Name | Type    | Description         |
| ----------- | ------- | ------------------- |
| `personId`  | int     | Primary key         |
| `lastName`  | varchar | Person's last name  |
| `firstName` | varchar | Person's first name |

### Table: `Address`

| Column Name | Type    | Description      |
| ----------- | ------- | ---------------- |
| `addressId` | int     | Primary key      |
| `personId`  | int     | ID of the person |
| `city`      | varchar | City             |
| `state`     | varchar | State            |

---

# Solution: `pd.merge()` with a `LEFT JOIN`

```python
import pandas as pd

def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    result = pd.merge(
        person,
        address,
        on='personId',
        how='left'
    )

    return result[['firstName', 'lastName', 'city', 'state']]
```

### Explanation

The main operation we need is:

```python
pd.merge()
```

`pd.merge()` is Pandas' equivalent of performing a SQL-style `JOIN`.

The key is that we need a **LEFT JOIN**, because every person must remain in the result.

---

# Step 1: Merge the two DataFrames

```python
result = pd.merge(
    person,
    address,
    on='personId',
    how='left'
)
```

Let's understand each argument.

---

## `person`

```python
pd.merge(person, ...)
```

This is the first DataFrame.

We use `Person` as the left DataFrame because the problem says:

> report ... **each person in the `Person` table**

So `Person` is the table whose rows we must preserve.

---

## `on='personId'`

```python
on='personId'
```

This tells Pandas:

> Match rows where `personId` is the same in both DataFrames.

For example:

### Person

| personId | firstName | lastName |
| -------: | --------- | -------- |
|        1 | Allen     | Wang     |
|        2 | Bob       | Alice    |

### Address

| addressId | personId | city          | state      |
| --------: | -------: | ------------- | ---------- |
|         1 |        2 | New York City | New York   |
|         2 |        3 | Leetcode      | California |

Pandas matches:

```text
Person.personId = Address.personId
```

So:

```text
personId = 2
```

matches the New York City address.

---

# Step 2: Why `how='left'`?

```python
how='left'
```

means:

> Keep **every row from the left DataFrame**, even if there is no match in the right DataFrame.

Our left DataFrame is:

```python
person
```

Therefore, every person remains in the output.

This is exactly what the problem requires.

---

# What happens to person 1?

Person 1 is:

```text
personId = 1
firstName = Allen
lastName = Wang
```

But there is no:

```text
personId = 1
```

in `Address`.

Because we're using a left join, Pandas still keeps person 1.

There is simply no matching value for:

```text
city
state
```

so Pandas fills them with:

```text
NaN
```

Conceptually:

| firstName | lastName | city | state |
| --------- | -------- | ---- | ----- |
| Allen     | Wang     | NaN  | NaN   |

On LeetCode, this corresponds to the requested `null`.

---

# What happens to person 2?

Person 2 has:

```text
personId = 2
```

and the `Address` table contains:

| personId | city          | state    |
| -------: | ------------- | -------- |
|        2 | New York City | New York |

So the merge produces:

| firstName | lastName | city          | state    |
| --------- | -------- | ------------- | -------- |
| Bob       | Alice    | New York City | New York |

---

# Step 3: Select only the required columns

After the merge, `result` contains more columns than the problem asks for.

Conceptually:

```text
personId
lastName
firstName
addressId
city
state
```

But the required output is:

```text
firstName
lastName
city
state
```

So we use:

```python
return result[['firstName', 'lastName', 'city', 'state']]
```

The double brackets are important.

### Single brackets

```python
result['firstName']
```

selects one column and returns a Series.

### Double brackets

```python
result[['firstName', 'lastName', 'city', 'state']]
```

select multiple columns and return a DataFrame.

Since LeetCode expects a DataFrame, we use double brackets.

---

# Full Walkthrough

Starting DataFrames:

### `person`

| personId | firstName | lastName |
| -------: | --------- | -------- |
|        1 | Allen     | Wang     |
|        2 | Bob       | Alice    |

### `address`

| addressId | personId | city          | state      |
| --------: | -------: | ------------- | ---------- |
|         1 |        2 | New York City | New York   |
|         2 |        3 | Leetcode      | California |

We perform:

```python
pd.merge(
    person,
    address,
    on='personId',
    how='left'
)
```

The result conceptually becomes:

| personId | firstName | lastName | addressId | city          | state    |
| -------: | --------- | -------- | --------: | ------------- | -------- |
|        1 | Allen     | Wang     |       NaN | NaN           | NaN      |
|        2 | Bob       | Alice    |         1 | New York City | New York |

Then:

```python
result[['firstName', 'lastName', 'city', 'state']]
```

gives:

| firstName | lastName | city          | state    |
| --------- | -------- | ------------- | -------- |
| Allen     | Wang     | NaN           | NaN      |
| Bob       | Alice    | New York City | New York |

---

# Why Not Use `how='inner'`?

An `inner` merge keeps only rows that have a match in **both** DataFrames.

```python
pd.merge(
    person,
    address,
    on='personId',
    how='inner'
)
```

would produce only:

| firstName | lastName | city          | state    |
| --------- | -------- | ------------- | -------- |
| Bob       | Alice    | New York City | New York |

Person 1 would disappear because they don't have an address.

That violates the problem requirement.

### Remember:

```text
LEFT JOIN
→ keep everything from the left table

INNER JOIN
→ keep only matching rows
```

Because we need **every person**, we need:

```python
how='left'
```

---

# Why Is `Person` on the Left?

These two are not equivalent for this problem:

```python
pd.merge(person, address, on='personId', how='left')
```

and:

```python
pd.merge(address, person, on='personId', how='left')
```

The first one means:

> Keep every person.

The second one means:

> Keep every address.

The problem asks for every **person**, so:

```python
person
```

must be the left DataFrame.

A useful way to remember this:

```text
LEFT JOIN
    ↓
Keep everything from LEFT
```

Therefore:

```python
pd.merge(person, address, how='left')
```

means:

```text
Keep every person
+ attach their address if one exists
```

---

# SQL Equivalent

The Pandas solution is directly equivalent to this SQL:

```sql
SELECT
    p.firstName,
    p.lastName,
    a.city,
    a.state
FROM Person p
LEFT JOIN Address a
    ON p.personId = a.personId;
```

The correspondence is:

| SQL              | Pandas          |
| ---------------- | --------------- |
| `JOIN`           | `pd.merge()`    |
| `ON personId`    | `on='personId'` |
| `LEFT JOIN`      | `how='left'`    |
| `SELECT columns` | `df[[columns]]` |
| `NULL`           | `NaN`           |

So if you already understand SQL joins, Pandas `merge()` becomes much easier.

---

# Important Pandas Concepts

## 1. `pd.merge()`

General syntax:

```python
pd.merge(
    left_dataframe,
    right_dataframe,
    on='column',
    how='join_type'
)
```

For example:

```python
pd.merge(
    customers,
    orders,
    on='customer_id',
    how='left'
)
```

means:

> Match customers and orders using `customer_id`, while keeping every customer.

---

## 2. `how='left'`

```python
how='left'
```

means:

> Keep all rows from the left DataFrame.

Matching rows from the right DataFrame are attached.

If there is no match, the right-side columns become `NaN`.

---

## 3. `on=`

```python
on='personId'
```

specifies the column used to match the two DataFrames.

It's equivalent to:

```sql
ON p.personId = a.personId
```

in SQL.

---

## 4. Selecting multiple columns

```python
df[['firstName', 'lastName', 'city', 'state']]
```

returns a DataFrame containing only those columns.

Remember:

```python
df['column']
```

→ one column / Series

```python
df[['column1', 'column2']]
```

→ multiple columns / DataFrame

---

## 5. `NaN` vs `NULL`

SQL uses:

```text
NULL
```

to represent a missing value.

Pandas commonly represents missing values as:

```text
NaN
```

So when the address doesn't exist:

```text
SQL      → NULL
Pandas   → NaN
```

LeetCode accepts this as the missing value required by the problem.

---

# Key Takeaway

This problem is essentially a **LEFT JOIN problem**.

The SQL mental model:

```text
Person
  ↓
LEFT JOIN
  ↓
Address
  ↓
Match using personId
  ↓
Keep every person
  ↓
Missing address → NULL
```

The Pandas equivalent is:

```python
pd.merge(
    person,
    address,
    on='personId',
    how='left'
)
```

Then select the required columns:

```python
result[['firstName', 'lastName', 'city', 'state']]
```

### The main Pandas pattern to remember

```python
result = pd.merge(
    left_df,
    right_df,
    on='common_column',
    how='left'
)

result[['column1', 'column2', 'column3']]
```

### Most important rule

> **If the problem says "include every row from table A, even if there is no matching row in table B," use a LEFT JOIN — `how='left'` in Pandas.**
