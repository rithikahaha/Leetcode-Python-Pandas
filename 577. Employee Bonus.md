# 577. Employee Bonus
LeetCode: https://leetcode.com/problems/employee-bonus/ · Easy

## Problem
Return `name, bonus` for every employee whose bonus is under 1000, including employees with no bonus at all.

**Employee**
| Column | Type | Notes |
|---|---|---|
| empId | int | unique |
| name | varchar | |
| supervisor | int | |
| salary | int | |

**Bonus**
| Column | Type | Notes |
|---|---|---|
| empId | int | foreign key to Employee.empId |
| bonus | int | |

**Example**
```
Employee: (3, Brad, null, 4000), (1, John, 3, 1000), (2, Dan, 3, 2000), (4, Thomas, 3, 4000)
Bonus:    (2, 500), (4, 2000)

Output:
name | bonus
Brad | null
John | null
Dan  | 500
```
Brad and John have no row in `Bonus`, so they qualify by having no bonus. Dan's bonus (500) is under 1000, so he qualifies too. Thomas's bonus (2000) is neither missing nor under 1000, so he's excluded.

## Solution
```python
import pandas as pd

def employee_bonus(employee: pd.DataFrame, bonus: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(employee, bonus, on='empId', how='left')
    result = merged[merged['bonus'].isna() | (merged['bonus'] < 1000)]
    return result[['name', 'bonus']]
```

Tracing the example above:

1. `pd.merge(employee, bonus, on='empId', how='left')` keeps every employee. Brad and John have no matching row in `Bonus`, so their `bonus` column comes back `NaN`. Dan gets 500, Thomas gets 2000.
2. `merged['bonus'].isna() | (merged['bonus'] < 1000)` has to check both conditions with an OR, and `isna()` is doing real work here: `NaN < 1000` evaluates to `False` in Pandas, not `True`, so a bare `bonus < 1000` filter would silently drop Brad and John instead of including them.
3. Applying that filter: Brad and John pass via `isna()`, Dan passes via `500 < 1000`, and Thomas fails both checks (2000 isn't missing and isn't under 1000), so he's dropped.
4. Pandas needs `|` for this, not Python's `or`, since the comparison is element-wise across a whole column rather than a single boolean value.

SQL equivalent:
```sql
SELECT e.name, b.bonus
FROM Employee e
LEFT JOIN Bonus b ON e.empId = b.empId
WHERE b.bonus < 1000 OR b.bonus IS NULL;
```
