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

Say the salaries are `[100, 200, 200, 300]`.

1. `drop_duplicates()` removes repeats first: `[100, 200, 300]`. Skip this and a tied top salary (two people at 200, say) would crowd out the real second place — you'd end up comparing 200 against itself instead of against 100.
2. `sort_values(ascending=False)` puts them highest to lowest: `[300, 200, 100]`.
3. `.iloc[1]` grabs the value at index 1, the second one in that sorted list, which is `200`, the second-highest distinct salary.
4. `len(salaries) > 1` guards that lookup. If there's only one distinct salary (or the table's empty), there is no second-highest, so `second` becomes `None` instead of crashing on `iloc[1]`.
5. LeetCode wants a one-row table with a column named `SecondHighestSalary`, not a bare number, so the last line wraps `second` in a list and builds a DataFrame from it: `pd.DataFrame({'SecondHighestSalary': [second]})`.

SQL equivalent:
```sql
SELECT MAX(salary) AS SecondHighestSalary
FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```
