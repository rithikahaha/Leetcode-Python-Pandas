# 577. Employee Bonus
LeetCode: https://leetcode.com/problems/employee-bonus/ · Easy

## Problem
`Employee(empId, name, supervisor, salary)`, `Bonus(empId, bonus)`. Return `name, bonus` for employees whose bonus is under 1000 or missing entirely.

## Solution
```python
import pandas as pd

def employee_bonus(employee: pd.DataFrame, bonus: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(employee, bonus, on='empId', how='left')
    result = merged[merged['bonus'].isna() | (merged['bonus'] < 1000)]
    return result[['name', 'bonus']]
```

Left merge keeps employees with no `Bonus` row, giving them NaN. The filter has to explicitly OR in `isna()` because `NaN < 1000` evaluates to `False`, not `True`, so a plain `bonus < 1000` check would silently drop everyone with no bonus at all. Pandas needs `|` for element-wise OR here, not Python's `or`.

SQL equivalent:
```sql
SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b ON e.empId = b.empId
WHERE b.bonus < 1000 OR b.bonus IS NULL;
```
