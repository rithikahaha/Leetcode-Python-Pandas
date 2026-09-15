# 176. Second Highest Salary
LeetCode: https://leetcode.com/problems/second-highest-salary/ · Medium

## Problem
Return the second highest **distinct** salary from `Employee(id, salary)`. If it doesn't exist, return null.

## Solution
```python
import pandas as pd

def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    salaries = employee['salary'].drop_duplicates().sort_values(ascending=False)
    second = salaries.iloc[1] if len(salaries) > 1 else None
    return pd.DataFrame({'SecondHighestSalary': [second]})
```

Drop duplicates before sorting, otherwise a repeated top salary (say two people tied for the max) would push the real second-highest out of position. Sorting descending puts the highest salary at `iloc[0]`, so the second-highest sits at `iloc[1]`. Guard that access with `len(salaries) > 1`, since indexing into an empty or single-row Series throws. The output also has to be a one-row, one-column DataFrame rather than a bare scalar, hence the `pd.DataFrame({...: [second]})` wrapper.

SQL equivalent:
```sql
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```
