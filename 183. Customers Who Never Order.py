# 183. Customers Who Never Order
LeetCode: https://leetcode.com/problems/customers-who-never-order/ · Easy

## Problem
`Customers(id, name)`, `Orders(id, customerId)`. Return the names of customers with no row in `Orders`.

## Solution
```python
import pandas as pd

def find_customers(customers: pd.DataFrame, orders: pd.DataFrame) -> pd.DataFrame:
    merged = pd.merge(customers, orders, left_on='id', right_on='customerId', how='left')
    result = merged[merged['customerId'].isna()]
    return result[['name']].rename(columns={'name': 'Customers'})
```

A left merge keeps every customer regardless of whether they have an order; anyone without one ends up with `customerId = NaN` after the merge, so filtering on `isna()` isolates exactly the customers who never ordered. An inner merge would be a mistake here, since it drops the unmatched rows before you get a chance to look for them.

SQL equivalent:
```sql
SELECT c.name AS Customers
FROM Customers c
LEFT JOIN Orders o ON c.id = o.customerId
WHERE o.customerId IS NULL;
```
