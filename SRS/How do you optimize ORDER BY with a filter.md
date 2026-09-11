<!--
reps: 0
priority: 0
-->
#Databases/Indexes #Databases/SQL #SRS

# How do you optimize ORDER BY with a filter

> [!abstract] Short answer
> Build the composite index in the order the query consumes columns: equality predicates first, then the ORDER BY columns. Equality constraints turn each prefix value into a contiguous run ordered by the next columns, so the sort disappears. A partial index handles the common single-status case, and mixed sort directions must be declared in the index.

## The ordering algebra that removes the sort

If the query is `WHERE status = 'open' ORDER BY created_at DESC`, the index `(created_at)` alone cannot help, but a composite `(status, created_at)` makes all rows for `status = 'open'` adjacent and sorted by `created_at` inside that run: the engine seeks the run and reads it in order. PostgreSQL's ORDER BY docs describe exactly this: an index on (x, y) satisfies ORDER BY x, y scanned forward or x DESC, y DESC scanned backward, but ORDER BY x ASC, y DESC has no scan direction that produces it — you declare the index as (x ASC, y DESC) or (x DESC, y ASC). ASC/DESC options plus NULLS FIRST/NULLS LAST exist precisely for mixed-direction sorts on composite keys.

```sql
-- queue pattern: hot subset + newest first
CREATE INDEX idx_tasks_open
    ON tasks (created_at DESC)
    WHERE status = 'open';

-- generic composite: equality then sort
CREATE INDEX idx_orders_cust_created
    ON orders (customer_id, created_at DESC);
```

**Listing 1.** The partial index skips closed tasks entirely, so the hot subset stays small; the composite serves per-customer history.

## When it stops working

A range predicate on an earlier column disables deeper seeking: `WHERE customer_id > 10 ORDER BY created_at` cannot use (customer_id, created_at) for the sort, because within the range the second column is not globally ordered; the planner will scan and sort or pick another strategy. Predicates that are not equality on all leading columns are the boundary — MySQL's ORDER BY optimization docs and PostgreSQL's both describe the same shape. With LIMIT the economics sharpen: an index-matching order lets the engine stop after N rows, while a mismatched one pays a full sort first, the interaction detailed in [[How does LIMIT interact with ORDER BY and indexes]]. Verify the plan shows no Sort node, following [[How do you read EXPLAIN ANALYZE in PostgreSQL]].

> [!warning] "I added an index with the ORDER BY column" is not the fix
> A single-column index on the sort column only helps when the whole scan is ordered by it. With a filter present, what matters is the run of rows selected by the equality prefix. And a range predicate before the sort column breaks the property — the index silently stops ordering, which is the same trap family as the prefix rule in [[What is the leftmost prefix rule for composite indexes]].

> [!tip] Interview answer
> Order the composite index as the query consumes it: equality columns first, ORDER BY columns after, declaring ASC/DESC and NULLS placement when mixed. A partial index is the sharper tool when the filter is a stable hot status. If the plan still shows a Sort, check for a range predicate ahead of the sort column — it breaks the contiguity the sort removal depends on.
