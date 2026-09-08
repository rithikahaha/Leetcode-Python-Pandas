# 181. Employees Earning More Than Their Managers

**LeetCode:** [181. Employees Earning More Than Their Managers](https://leetcode.com/problems/employees-earning-more-than-their-managers/)
**Difficulty:** Easy
**Language:** Python (Pandas)

---

## Problem

### Table: `Employee`

```text
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| salary      | int     |
| managerId   | int     |
+-------------+---------+
```

* `id` is the primary key (column with unique values) for this table.
* Each row indicates the ID of an employee, their name, salary, and the ID of their manager.

Write a solution to find the employees who **earn more than their managers**.

Return the result table in **any order**.

---

## Example 1

### Input

```text
Employee table:
+----+-------+--------+-----------+
| id | name  | salary | managerId |
+----+-------+--------+-----------+
| 1  | Joe   | 70000  | 3         |
| 2  | Henry | 80000  | 4         |
| 3  | Sam   | 60000  | Null      |
| 4  | Max   | 90000  | Null      |
+----+-------+--------+-----------+
```

### Output

```text
+----------+
| Employee |
+----------+
| Joe      |
+----------+
```

### Explanation

* Joe earns `70000`, while his manager Sam earns `60000` → **Joe qualifies**.
* Henry earns `80000`, while his manager Max earns `90000` → Henry does not qualify.
* Sam and Max have no managers, so they cannot be compared.

Therefore, the answer is:

```text
Joe
```

---

# Pandas Solution

```python
import pandas as pd

def find_employees(employee: pd.DataFrame) -> pd.DataFrame:
    result = pd.merge(
        employee,
        employee,
        left_on='managerId',
        right_on='id',
        suffixes=('_employee', '_manager')
    )

    result = result[
        result['salary_employee'] > result['salary_manager']
    ]

    return result[['name_employee']].rename(
        columns={'name_employee': 'Employee'}
    )
```

---

# Explanation

Since the **manager is also an employee**, both the employee and manager information exists in the same DataFrame.

Therefore, we perform a **self merge**:

```python
result = pd.merge(
    employee,
    employee,
    left_on='managerId',
    right_on='id',
    suffixes=('_employee', '_manager')
)
```

The important relationship is:

```text
employee.managerId = manager.id
```

* `left_on='managerId'` uses the employee's manager ID.
* `right_on='id'` matches it with the manager's employee ID.
* `suffixes` distinguish overlapping columns such as `name` and `salary`.

This puts the employee and manager information on the same row, allowing their salaries to be compared.

---

## Step 1: Filter Employees Earning More

```python
result = result[
    result['salary_employee'] > result['salary_manager']
]
```

This keeps only rows where:

```text
employee salary > manager salary
```

For the example:

| Employee | Employee Salary | Manager | Manager Salary | Result |
| -------- | --------------: | ------- | -------------: | ------ |
| Joe      |           70000 | Sam     |          60000 | ✅      |
| Henry    |           80000 | Max     |          90000 | ❌      |

Only Joe remains.

---

## Step 2: Select and Rename the Required Column

The problem requires the output column to be named `Employee`.

```python
return result[['name_employee']].rename(
    columns={'name_employee': 'Employee'}
)
```

* `[['name_employee']]` selects the employee's name.
* `.rename()` changes the column name to `Employee`.

Final result:

```text
+----------+
| Employee |
+----------+
| Joe      |
+----------+
```

---

# Why Does the Self Merge Exclude Employees Without Managers?

`pd.merge()` uses an **inner merge by default**.

Therefore, only employees whose `managerId` matches an `id` in the DataFrame are included.

For example:

```text
Sam → managerId = NULL
Max → managerId = NULL
```

There is no manager row to match for Sam or Max, so they are automatically excluded.

This is exactly what we want because employees without managers cannot satisfy the condition.

---

# Important Pandas Concepts

### 1. Self Merge

A **self merge** joins a DataFrame with itself when rows are related to other rows in the same DataFrame.

Here:

```python
pd.merge(
    employee,
    employee,
    left_on='managerId',
    right_on='id',
    suffixes=('_employee', '_manager')
)
```

creates the employee-manager relationship:

```text
employee.managerId → manager.id
```

This allows values from the two related rows to be compared.

### 2. Boolean Filtering

```python
result['salary_employee'] > result['salary_manager']
```

creates a Boolean condition that keeps only employees whose salary is greater than their manager's salary.

### 3. Selecting and Renaming

```python
result[['name_employee']].rename(
    columns={'name_employee': 'Employee'}
)
```

selects the required column and renames it to match the expected output.

---

# Common Mistake

Do **not** match the two copies using `id` to `id`:

```python
pd.merge(employee, employee, on='id')
```

That would match each employee with the row having the same ID rather than finding their manager.

The correct relationship is:

```text
employee.managerId = manager.id
```

so we use:

```python
left_on='managerId'
right_on='id'
```

---

# SQL Equivalent

The same logic in SQL is:

```sql
SELECT
    e.name AS Employee
FROM Employee e
JOIN Employee m
    ON e.managerId = m.id
WHERE e.salary > m.salary;
```

| SQL                     | Pandas                               |
| ----------------------- | ------------------------------------ |
| `JOIN Employee m`       | `pd.merge(employee, employee)`       |
| `ON e.managerId = m.id` | `left_on='managerId', right_on='id'` |
| `e.salary > m.salary`   | Boolean filtering                    |
| `e.name AS Employee`    | Select + rename                      |

---

# Key Takeaway

The core pattern is:

```text
Self merge
    ↓
Match employee.managerId with manager.id
    ↓
Compare employee salary with manager salary
    ↓
Keep employees earning more
    ↓
Return employee names
```

> **Self merge is useful when rows in the same DataFrame have relationships with other rows in that same DataFrame.**
