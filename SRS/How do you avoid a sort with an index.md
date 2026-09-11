<!--
reps: 0
priority: 0
-->
#Databases/Indexes #Databases/SQL #SRS

# How do you avoid a sort with an index

> [!abstract] Short answer
> Let an index supply the order instead of the Sort node: scan a B-tree whose key matches the ORDER BY, in forward or backward direction. For single-column sorts the direction is free; for mixed ASC/DESC on several columns the index must declare matching sort orders; bitmap scans and hash-based plans throw the order away.

## Which index shapes preserve order

A B-tree on the sort columns stores keys in order, so the planner can hand rows to the client in order as it walks the leaves — PostgreSQL's ORDER BY docs note an index can be scanned forward or backward and that direction covers either direction of a single-column sort. Composite ordering needs the same left-to-right shape as the ORDER BY, and mixed directions must be written into the DDL: (x ASC, y DESC) is satisfiable no other way. The same logic answers MIN/MAX instantly and feeds [[What is keyset pagination]], where the next-page predicate rides the index order. If the WHERE clause also matches the prefix, the engine can stop early — the LIMIT case in [[How does LIMIT interact with ORDER BY and indexes]].

```sql
CREATE INDEX idx_feed ON posts (author_id, created_at DESC);
SELECT id, title FROM posts
WHERE author_id = 42
ORDER BY created_at DESC
LIMIT 20;
-- Plan: Index Scan using idx_feed, no Sort node
```

**Listing 1.** Equality on the leading column plus declared DESC on the sort column means rows come out ordered straight from the leaves.

## How sorts sneak back in

Bitmap heap scans visit pages in physical order and therefore require a separate sort, as PostgreSQL's combining-multiple-indexes page explicitly warns. Functions or expressions on the sort column change the ordering unless the index is on the same expression, the functional case in [[Why does a function on a column prevent index use]]. Locale-dependent text order can need a text_pattern_ops-style opclass, and a collation mismatch silently invalidates the ordering guarantee, which is one of the planner traps behind [[How does implicit type conversion hide an index]]. The cheapest audit is the plan: any Sort node above an Index Scan means the index did not deliver the order.

> [!warning] Backward scan covers reversal, not mixed directions
> The common mistake is assuming any index serves any ORDER BY because "you can scan it backwards". Reversal flips every column's direction at once: (x, y) backward gives x DESC, y DESC, never x ASC, y DESC. Top-N with mixed directions without a matching index degrades to sort the whole filtered set first, which for large tables is the difference between milliseconds and seconds.

> [!tip] Interview answer
> To avoid a sort, make the index key match the ORDER BY: same columns, same order, declaring ASC/DESC when they differ, and relying on forward or backward scan for single-column reversal. The plan must show an index scan with no Sort node. Bitmap plans and expressions on the sort column lose the order, so they reintroduce it.
