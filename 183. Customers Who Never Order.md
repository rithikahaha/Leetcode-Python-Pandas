# 183. Customers Who Never Order
LeetCode: https://leetcode.com/problems/customers-who-never-order/ · Easy

## Problem
Return the names of customers who never placed an order.

**Customers**
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| name | varchar | |

**Orders**
| Column | Type | Notes |
|---|---|---|
| id | int | primary key |
| customerId | int | foreign key to Customers.id |

**Example**
```
Customers: (1, Joe), (2, Henry), (3, Sam), (4, Max)
Orders:    (1, customerId=3), (2, customerId=1)

Output: Customers = Henry, Max
```
Joe and Sam each placed an order, so they're excluded. Henry and Max have no matching row in `Orders`, so they're the answer.

## Solution
```python
import pandas as pd

def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(customers, orders, left_on='id', right_on='customerId', how='left')
    result = merged[merged['customerId'].isna()]
    return result[['name']].rename(columns={'name': 'Customers'})
```

Tracing the example above:

1. `pd.merge(..., left_on='id', right_on='customerId', how='left')` keeps every customer regardless of whether they placed an order. Joe (`id=1`) matches order `customerId=1`; Sam (`id=3`) matches `customerId=3`. Henry and Max have no matching order row at all.
2. Because it's a **left** join, Henry and Max aren't dropped for lacking a match. Instead, the `customerId` column on their rows just becomes `NaN`. An inner join would have removed them before you got a chance to check for that.
3. `merged['customerId'].isna()` picks out exactly those NaN rows, i.e. Henry and Max.
4. `rename(columns={'name': 'Customers'})` matches the required output column name.

SQL equivalent:
```sql
SELECT c.name AS Customers
FROM Customers c
LEFT JOIN Orders o ON c.id = o.customerId
WHERE o.customerId IS NULL;
```
