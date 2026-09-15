# 181. Employees Earning More Than Their Managers
LeetCode: https://leetcode.com/problems/employees-earning-more-than-their-managers/ · Easy

## Problem
Return the names of employees who earn more than their manager.

**Employee**
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| name | varchar | |
| salary | int | |
| managerId | int | references Employee.id; null if no manager |

**Example**
```
id | name  | salary | managerId
1  | Joe   | 70000  | 3
2  | Henry | 80000  | 4
3  | Sam   | 60000  | null
4  | Max   | 90000  | null

Output: Employee = Joe
```
Joe (70000) earns more than his manager Sam (60000), so he qualifies. Henry (80000) earns less than his manager Max (90000), so he doesn't. Sam and Max have no manager at all, so there's nothing to compare them against.

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

Tracing the example above:

1. A manager is just another row in the same table, so `employee` is merged with itself: `left_on='managerId', right_on='id'` pairs each employee with the row whose `id` equals that employee's `managerId`. That pairs Joe with Sam (Joe's `managerId` is 3, Sam's `id` is 3) and Henry with Max.
2. `suffixes=('_employee', '_manager')` is what keeps the two copies of `name` and `salary` apart, so you get `salary_employee`/`salary_manager` instead of a collision.
3. `pd.merge` is an inner join by default, so Sam and Max, whose own `managerId` is null, never find a match on the right side and simply disappear from `merged` before any filtering happens.
4. The filter `salary_employee > salary_manager` keeps Joe (70000 > 60000) and drops Henry (80000 is not > 90000).
5. `rename(columns={'name_employee': 'Employee'})` matches the output column name LeetCode expects, leaving just `Employee = Joe`.

SQL equivalent:
```sql
SELECT e.name AS Employee
FROM Employee e
JOIN Employee m ON e.managerId = m.id
WHERE e.salary > m.salary;
```
