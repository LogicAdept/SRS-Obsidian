<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/SQL #SRS

# What is ARRAY JOIN in ClickHouse?

> [!abstract] Short answer
> ARRAY JOIN explodes an array column: each element of the array becomes its own row, with other columns copied. It is ClickHouse's built-in `unnest` — PostgreSQL's `CROSS JOIN UNNEST` and `LATERAL` patterns are done with ARRAY JOIN — and `LEFT ARRAY JOIN` additionally keeps rows whose arrays are empty, filling the element with defaults.

## Mechanics

Only one array can be joined per ARRAY JOIN clause (it may be a `Nested` structure, which is parallel arrays joined consistently). With plain `ARRAY JOIN arr`, rows with empty arrays disappear from the result; `LEFT ARRAY JOIN` keeps them with the default element value (0, empty string, or NULL). The `arrayJoin()` function achieves the same per-expression but the clause form is broader — for example joining multiple arrays of equal length positionally via a Nested structure. Note the versioned fact: since 26.5 `unnest(arr)` exists as a function-call alias of `arrayJoin`, but the table-function `UNNEST` form is not supported — ARRAY JOIN is the idiom.

```sql
-- one row per tag
SELECT id, tag
FROM events
ARRAY JOIN tags AS tag;

-- keep events with no tags at all
SELECT id, tag
FROM events
LEFT ARRAY JOIN tags AS tag;
```

**Listing 1.** Exploding a tags array, with and without preserving empty arrays.

## When it appears in real schemas

`Nested` structures — `Nested(k String, v UInt64)` stored as parallel arrays — are queried by ARRAY JOIN to align `k` and `v` per element ([[How do you search Map or Nested fields in ClickHouse]]); log/event payloads with repeated fields (tags, labels, items) unnest at query time so aggregations work per element; and funnel-style analysis unnests event arrays before windowing. Because unnesting multiplies rows, the cost lands after granule pruning — arrays are read as columns and expanded in memory, so a `count()` over the raw table stays cheap while the exploded query pays proportional to total elements.

> [!warning] ARRAY JOIN changes row counts before aggregation — mind your filters
> Predicates on the *element* must run after the join (or in the WHERE of the same query), while predicates on the *row* must not accidentally apply per element; the classic bug is filtering an exploded row set with a row-level condition and silently duplicating or dropping matches. And an `arrayJoin` on a column of enormous arrays (thousands of elements) can blow up intermediate row counts — cap arrays or pre-aggregate with `-Array` combinators ([[What are aggregate function combinators in ClickHouse]]) when possible.

> [!tip] Interview answer
> ARRAY JOIN unnests arrays into rows — one row per element, other columns duplicated; LEFT ARRAY JOIN preserves empty-array rows with defaults, and Nested structures join positionally. It's ClickHouse's answer to UNNEST/LATERAL, executed in memory after granule pruning, with the caveat that it multiplies row counts before your aggregations.
