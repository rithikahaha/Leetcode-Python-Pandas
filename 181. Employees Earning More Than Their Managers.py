# 181. Employees Earning More Than Their Managers
LeetCode: https://leetcode.com/problems/employees-earning-more-than-their-managers/ · Easy

## Problem
`Employee(id, name, salary, managerId)`. Return the names of employees who earn more than their manager.

## Solution
```python
import pandas as pd

def find_employees(employee: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(
        employee, employee,
        left_on='managerId', right_on='id',
        suffixes=('_employee', '_manager')
    )
    result = merged[merged['salary_employee'] > merged['salary_manager']]
    return result[['name_employee']].rename(columns={'name_employee': 'Employee'})
```

Since a manager is just another row in the same table, this is a self-merge: match each employee's `managerId` to the manager's `id`, and use `suffixes` to keep the overlapping `name`/`salary` columns apart. The merge is an inner join by default, which conveniently drops employees with no manager (`managerId` is null, e.g. Sam and Max) before you'd even need to filter for them. From there it's a straight salary comparison and a rename to match the expected `Employee` output column.

Watch the join direction: `left_on='managerId', right_on='id'`, not `on='id'`, which would just match each employee to itself.

SQL equivalent:
```sql
SELECT e.name AS Employee
FROM Employee e
JOIN Employee m ON e.managerId = m.id
WHERE e.salary > m.salary;
```
