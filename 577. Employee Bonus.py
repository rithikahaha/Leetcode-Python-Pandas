# 577. Employee Bonus

**LeetCode:** [577. Employee Bonus](https://leetcode.com/problems/employee-bonus/)
**Difficulty:** Easy
**Language:** Python (Pandas)

---

## Problem

### Table: `Employee`

```text id="4l0f2q"
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| empId       | int     |
| name        | varchar |
| supervisor  | int     |
| salary      | int     |
+-------------+---------+
```

* `empId` is the column with unique values.
* Each row contains an employee's ID, name, supervisor ID, and salary.

### Table: `Bonus`

```text id="bq7m5j"
+-------------+------+
| Column Name | Type |
+-------------+------+
| empId       | int  |
| bonus       | int  |
+-------------+------+
```

* `empId` is unique.
* `empId` is a foreign key referencing `Employee.empId`.
* Each row contains an employee's bonus amount.

Write a solution to report the **name and bonus amount** of each employee who satisfies either condition:

* The employee has a bonus **less than `1000`**.
* The employee **did not get any bonus**.

Return the result table in **any order**.

---

## Example 1

### Input

```text id="4s1z0n"
Employee table:
+-------+--------+------------+--------+
| empId | name   | supervisor | salary |
+-------+--------+------------+--------+
| 3     | Brad   | null       | 4000   |
| 1     | John   | 3          | 1000   |
| 2     | Dan    | 3          | 2000   |
| 4     | Thomas | 3          | 4000   |
+-------+--------+------------+--------+

Bonus table:
+-------+-------+
| empId | bonus |
+-------+-------+
| 2     | 500   |
| 4     | 2000  |
+-------+-------+
```

### Output

```text id="u6kqz5"
+------+-------+
| name | bonus |
+------+-------+
| Brad | null  |
| John | null  |
| Dan  | 500   |
+------+-------+
```

### Explanation

* Brad has no bonus → include.
* John has no bonus → include.
* Dan has a bonus of `500` → include because `500 < 1000`.
* Thomas has a bonus of `2000` → exclude.

---

# Pandas Solution

```python id="v6p2qa"
import pandas as pd

def employee_bonus(employee: pd.DataFrame, bonus: pd.DataFrame) -> pd.DataFrame:
    result = pd.merge(
        employee,
        bonus,
        on='empId',
        how='left'
    )

    result = result[
        result['bonus'].isna() | (result['bonus'] < 1000)
    ]

    return result[['name', 'bonus']]
```

---

# Explanation

We need **all employees**, including those who have no corresponding row in the `Bonus` DataFrame.

Therefore, we use a **left merge**:

```python id="b6k0tv"
result = pd.merge(
    employee,
    bonus,
    on='empId',
    how='left'
)
```

This keeps every employee and attaches their bonus when one exists.

For employees without a bonus, the `bonus` column becomes `NaN`.

After the merge:

| name   | bonus |
| ------ | ----: |
| Brad   |   NaN |
| John   |   NaN |
| Dan    |   500 |
| Thomas |  2000 |

---

## Step 1: Filter the Required Employees

```python id="s5c8xn"
result = result[
    result['bonus'].isna() | (result['bonus'] < 1000)
]
```

There are two conditions.

### No Bonus

```python id="n7q3pv"
result['bonus'].isna()
```

`isna()` identifies employees whose bonus is missing.

These are employees who did not get a bonus.

### Bonus Less Than 1000

```python id="w8r2cj"
result['bonus'] < 1000
```

This identifies employees whose bonus is below `1000`.

### Combine the Conditions

```python id="z4m6kh"
result['bonus'].isna() | (result['bonus'] < 1000)
```

`|` means **OR** in Pandas.

So an employee is included if:

```text
No bonus
     OR
Bonus < 1000
```

---

## Step 2: Select the Required Columns

```python id="h3v9qs"
return result[['name', 'bonus']]
```

The problem only asks for the employee's `name` and `bonus`.

---

# Important Pandas Concepts

### Left Merge + `isna()`

This problem uses the same common pattern as finding customers with no orders:

```python id="q7p3wd"
pd.merge(
    employee,
    bonus,
    on='empId',
    how='left'
)
```

A left merge preserves every employee. Employees without a matching bonus receive `NaN`, which can then be identified using:

```python id="r2n8vc"
result['bonus'].isna()
```

### Boolean OR: `|`

Pandas uses `|` for element-wise OR:

```python id="j5x4mz"
condition1 | condition2
```

Parentheses are required around individual comparisons:

```python id="c8v1ks"
result['bonus'].isna() | (result['bonus'] < 1000)
```

---

# SQL Equivalent

```sql id="x6t3pn"
SELECT
    e.name,
    b.bonus
FROM Employee e
LEFT JOIN Bonus b
    ON e.empId = b.empId
WHERE b.bonus < 1000
   OR b.bonus IS NULL;
```

---

# Pandas vs SQL

| SQL                    | Pandas                      |
| ---------------------- | --------------------------- |
| `LEFT JOIN`            | `pd.merge(..., how='left')` |
| `ON e.empId = b.empId` | `on='empId'`                |
| `b.bonus < 1000`       | `result['bonus'] < 1000`    |
| `b.bonus IS NULL`      | `result['bonus'].isna()`    |
| `OR`                   | `\|`                        |
| `SELECT name, bonus`   | `[['name', 'bonus']]`       |

---

# Common Mistakes

### 1. Using an Inner Merge

```python id="s2k6vp"
how='inner'
```

would remove employees without a bonus before we can identify them.

We need:

```python id="a7f3hx"
how='left'
```

to preserve all employees.

### 2. Checking Only `bonus < 1000`

```python id="m9w4kc"
result[result['bonus'] < 1000]
```

would exclude employees with no bonus because `NaN < 1000` is not `True`.

We must explicitly include missing bonuses:

```python id="x4q8nd"
result['bonus'].isna() | (result['bonus'] < 1000)
```

### 3. Using Python `or` Instead of `|`

Don't write:

```python id="v6t1rx"
result['bonus'].isna() or (result['bonus'] < 1000)
```

Pandas requires `|` for element-wise OR.

---

# Key Takeaway

The core pattern is:

```text id="p7c2mw"
Left merge employees with bonuses
        ↓
Employees without bonuses → NaN
        ↓
Keep NaN OR bonus < 1000
        ↓
Return name + bonus
```

> **When a condition includes both missing values and a numeric comparison, use `isna()` for the missing case and combine it with the comparison using `|`.**
