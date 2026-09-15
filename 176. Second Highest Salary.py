# 176. Second Highest Salary
LeetCode: https://leetcode.com/problems/second-highest-salary/ · Medium

## Problem
Return the second highest **distinct** salary from `Employee(id, salary)`, or null if it doesn't exist.

## Solution
```python
import pandas as pd

def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    salaries = employee['salary'].drop_duplicates().sort_values(ascending=False)
    second = salaries.iloc[1] if len(salaries) > 1 else None
    return pd.DataFrame({'SecondHighestSalary': [second]})
```

Dedup before sorting so a tied top salary can't crowd out the real second place, then sort descending and take `iloc[1]`. Fall back to `None` when there are fewer than two distinct salaries.

SQL equivalent:
```sql
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```
