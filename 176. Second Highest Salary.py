# 176. Second Highest Salary

**LeetCode:** [176. Second Highest Salary](https://leetcode.com/problems/second-highest-salary/)
**Difficulty:** Medium
**Language:** Python (Pandas)

---

## Problem

### Table: `Employee`

```text
+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| salary      | int  |
+-------------+------+
```

* `id` is the primary key (column with unique values) for this table.
* Each row contains information about an employee and their salary.

Write a solution to find the **second highest distinct salary** from the `Employee` table.

If there is no second highest salary, return `null` (`None` in Pandas).

---

## Example 1

### Input

```text
Employee table:
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
| 2  | 200    |
| 3  | 300    |
+----+--------+
```

### Output

```text
+---------------------+
| SecondHighestSalary |
+---------------------+
| 200                 |
+---------------------+
```

### Explanation

The distinct salaries in descending order are:

```text
300 → 200 → 100
```

Therefore, the second highest salary is `200`.

---

## Example 2

### Input

```text
Employee table:
+----+--------+
| id | salary |
+----+--------+
| 1  | 100    |
+----+--------+
```

### Output

```text
+---------------------+
| SecondHighestSalary |
+---------------------+
| null                |
+---------------------+
```

### Explanation

There is only one distinct salary, so a second highest salary does not exist.

---

# Pandas Solution

```python id="k8m4qx"
import pandas as pd

def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    salaries = employee['salary'].drop_duplicates().sort_values(
        ascending=False
    )

    second_highest = salaries.iloc[1] if len(salaries) > 1 else None

    return pd.DataFrame({
        'SecondHighestSalary': [second_highest]
    })
```

---

# Explanation

We need the **second highest distinct salary**.

The important part is handling duplicate salaries and the case where a second salary does not exist.

## Step 1: Remove Duplicate Salaries

```python id="n5t2cr"
salaries = employee['salary'].drop_duplicates()
```

The problem asks for a **distinct** salary, so duplicate salary values must be removed.

For example:

```text
100
200
200
300
```

becomes:

```text
100
200
300
```

---

## Step 2: Sort in Descending Order

```python id="y6p3vz"
salaries.sort_values(ascending=False)
```

This puts the highest salary first:

```text
300
200
100
```

---

## Step 3: Get the Second Value

```python id="c9r7mk"
second_highest = salaries.iloc[1] if len(salaries) > 1 else None
```

Pandas uses **zero-based indexing**, so:

```text
iloc[0] → highest salary
iloc[1] → second highest salary
```

We first check:

```python id="q2x6nd"
len(salaries) > 1
```

because accessing `iloc[1]` when there is only one salary would cause an error.

If there is no second distinct salary, we return:

```python id="m7v3kc"
None
```

which corresponds to `NULL` in the LeetCode output.

---

## Step 4: Create the Required Output

```python id="r4n8wp"
return pd.DataFrame({
    'SecondHighestSalary': [second_highest]
})
```

The result must contain exactly one column named:

```text
SecondHighestSalary
```

and exactly one row.

---

# Important Pandas Concepts

### `drop_duplicates()`

```python id="x5q2mh"
employee['salary'].drop_duplicates()
```

removes repeated salary values so that we work with **distinct salaries**.

### `sort_values()`

```python id="f7m3kp"
.sort_values(ascending=False)
```

sorts salaries from highest to lowest.

### `iloc`

```python id="d8v4nz"
salaries.iloc[1]
```

selects the second element because Pandas uses zero-based indexing.

### Conditional Expression

```python id="j3k6px"
value if condition else None
```

allows us to safely return `None` when fewer than two distinct salaries exist.

---

# SQL Equivalent

```sql id="p6w8rx"
SELECT
    MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (
    SELECT MAX(salary)
    FROM Employee
);
```

This works by first finding the highest salary, then finding the maximum salary that is **less than** it.

If there is no lower salary, `MAX()` returns `NULL`.

---

# Pandas vs SQL

| SQL                      | Pandas                        |
| ------------------------ | ----------------------------- |
| `MAX(salary)`            | `.max()` / sorted values      |
| `WHERE salary < highest` | Remove highest via ordering   |
| Distinct second salary   | `drop_duplicates()` + sorting |
| `NULL`                   | `None`                        |
| Return one value         | Create a one-row DataFrame    |

---

# Common Mistakes

### 1. Not Removing Duplicates

If salaries are:

```text
300
300
200
```

simply taking the second row would give `300`, but the **second highest distinct** salary is `200`.

Use:

```python id="z5x8pc"
drop_duplicates()
```

first.

### 2. Using `iloc[1]` Without Checking

```python id="k4p9tm"
salaries.iloc[1]
```

will raise an error if there is only one distinct salary.

Always handle the case:

```python id="w6n3qd"
len(salaries) > 1
```

### 3. Returning the Scalar Directly

LeetCode expects a DataFrame with the required column, not just the salary value.

Use:

```python id="v2c7mk"
pd.DataFrame({
    'SecondHighestSalary': [second_highest]
})
```

---

# Key Takeaway

The core pattern is:

```text
Remove duplicate salaries
        ↓
Sort from highest to lowest
        ↓
Take the second value
        ↓
If fewer than 2 values exist → None
        ↓
Return as a one-row DataFrame
```

> **For the second highest distinct value, remove duplicates first, then use descending order and zero-based indexing.**
