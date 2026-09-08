# 183. Customers Who Never Order

**LeetCode:** [183. Customers Who Never Order](https://leetcode.com/problems/customers-who-never-order/)
**Difficulty:** Easy
**Language:** Python (Pandas)

---

## Problem

### Table: `Customers`

```text
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
```

* `id` is the primary key (column with unique values) for this table.
* Each row indicates the ID and name of a customer.

### Table: `Orders`

```text
+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| customerId  | int  |
+-------------+------+
```

* `id` is the primary key (column with unique values) for this table.
* `customerId` is a foreign key referencing the `id` column in `Customers`.
* Each row indicates the ID of an order and the customer who placed it.

Write a solution to find all customers who **never order anything**.

Return the result table in **any order**.

---

## Example 1

### Input

```text
Customers table:
+----+-------+
| id | name  |
+----+-------+
| 1  | Joe   |
| 2  | Henry |
| 3  | Sam   |
| 4  | Max   |
+----+-------+

Orders table:
+----+------------+
| id | customerId |
+----+------------+
| 1  | 3          |
| 2  | 1          |
+----+------------+
```

### Output

```text
+-----------+
| Customers |
+-----------+
| Henry     |
| Max       |
+-----------+
```

### Explanation

* Joe (`id = 1`) has an order → exclude.
* Henry (`id = 2`) has no order → include.
* Sam (`id = 3`) has an order → exclude.
* Max (`id = 4`) has no order → include.

Therefore, the customers who never ordered are **Henry** and **Max**.

---

# Pandas Solution

```python id="7wq4rm"
import pandas as pd

def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    result = pd.merge(
        customers,
        orders,
        left_on='id',
        right_on='customerId',
        how='left'
    )

    result = result[result['customerId'].isna()]

    return result[['name']].rename(
        columns={'name': 'Customers'}
    )
```

---

# Explanation

We need to keep **all customers**, then identify which ones have no matching order.

A **left merge** is appropriate because every customer must be preserved, including customers who have no orders:

```python id="e3t1r5"
result = pd.merge(
    customers,
    orders,
    left_on='id',
    right_on='customerId',
    how='left'
)
```

The relationship is:

```text id="f2s8qa"
customers.id → orders.customerId
```

For customers without an order, the order columns contain `NaN`.

---

## Step 1: Keep Customers Without Orders

```python id="0wz2x6"
result = result[result['customerId'].isna()]
```

`isna()` identifies missing values.

After the left merge, customers with no matching order have:

```text
customerId = NaN
```

So filtering for `isna()` gives only customers who never ordered.

For the example:

| name  | customerId |
| ----- | ---------: |
| Joe   |          1 |
| Henry |        NaN |
| Sam   |          3 |
| Max   |        NaN |

After filtering:

| name  | customerId |
| ----- | ---------: |
| Henry |        NaN |
| Max   |        NaN |

---

## Step 2: Select and Rename the Required Column

The problem requires the column to be named `Customers`:

```python id="8u5x2n"
return result[['name']].rename(
    columns={'name': 'Customers'}
)
```

Final result:

```text
+-----------+
| Customers |
+-----------+
| Henry     |
| Max       |
+-----------+
```

---

# Important Pandas Concepts

### Left Merge + Missing Values

This problem follows a common pattern for finding rows with **no matching record** in another DataFrame:

```python id="m4s2vd"
pd.merge(
    left_df,
    right_df,
    left_on='left_key',
    right_on='right_key',
    how='left'
)
```

A left merge preserves every row from the left DataFrame. If no match exists in the right DataFrame, the right-side columns become `NaN`.

We can then identify unmatched rows using:

```python id="f4r8dp"
result['column'].isna()
```

For this problem:

```text id="q3qz7k"
Customers.id → Orders.customerId
                       ↓
                 no match → NaN
```

### `isna()`

```python id="7f6kq2"
result['customerId'].isna()
```

returns `True` for missing values and `False` otherwise.

It is commonly used after a left merge to find records that have **no match**.

---

# Why Not Use an Inner Merge?

An inner merge keeps only rows that have a match.

```python id="p9l4cc"
how='inner'
```

would return only customers who **have placed orders**, which is the opposite of what we need.

We need:

```text
All customers
    ↓
Left merge with orders
    ↓
Find missing order matches
    ↓
Customers who never ordered
```

---

# SQL Equivalent

The same logic can be written in SQL as:

```sql id="q8o7nj"
SELECT
    c.name AS Customers
FROM Customers c
LEFT JOIN Orders o
    ON c.id = o.customerId
WHERE o.customerId IS NULL;
```

| SQL                          | Pandas                                |
| ---------------------------- | ------------------------------------- |
| `LEFT JOIN`                  | `pd.merge(..., how='left')`           |
| `ON c.id = o.customerId`     | `left_on='id', right_on='customerId'` |
| `WHERE o.customerId IS NULL` | `result['customerId'].isna()`         |
| `c.name AS Customers`        | Select + rename                       |

---

# Common Mistake

### Using an Inner Merge

```python id="1q8k0j"
pd.merge(customers, orders, ...)
```

without specifying:

```python id="b7n4sf"
how='left'
```

uses an inner merge by default.

That would remove customers without orders before we have a chance to identify them.

For this problem, **preserving unmatched customers is essential**, so we need:

```python id="k2f9vz"
how='left'
```

---

# Key Takeaway

The core pattern for finding records that **don't have a match** is:

```text id="w7m2px"
Left merge
    ↓
Preserve all rows from the main table
    ↓
Look for NaN in the matched table's column
    ↓
Return unmatched rows
```

> **Left merge + `isna()` is a fundamental Pandas pattern for finding records with no corresponding match in another DataFrame.**
