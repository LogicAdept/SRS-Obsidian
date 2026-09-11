<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# How do you search Map or Nested fields in ClickHouse?

> [!abstract] Short answer
> Map columns store keys and values as separate subcolumns: `mapKeys(m)`/`m.keys` and `mapValues(m)`/`m.values` are queryable arrays, a single-key read `m['key']` is rewritten to a typed key subcolumn, and predicates can use `mapContains`, `has(mapKeys(m), ...)`, or `arrayExists`. Nested structures are parallel `Array(T)` columns read with `ARRAY JOIN` or array functions — and both can carry skipping indexes on their subcolumn expressions.

## Searching a Map

Because each key materializes as its own subcolumn (`m.key_<serialized_key>`), filtering on a known key reads only that column — this is the fast path. For unknown keys, you scan `mapKeys(m)` or use `mapContains(m, 'key')`; text predicates over values can be accelerated with `tokenbf_v1`-style indexes created on `mapValues(m)` or on specific key expressions, since indexes require an expression, not a whole map. For key-set-heavy workloads the modern alternative is the `JSON` type, which stores frequent paths as dynamic subcolumns with direct single-path reads — the Map-vs-JSON comparison in the docs turns on whether keys are known in advance ([[How do you index JSONB in PostgreSQL]] is the row-store analogue of the same decision).

```sql
SELECT count()
FROM events
WHERE props['browser'] = 'Chrome';          -- reads the props.browser subcolumn

SELECT count()
FROM events
WHERE mapContains(props, 'trace_id');       -- key presence, any key

ALTER TABLE events ADD INDEX bv_ix props['browser']
    TYPE set(100) GRANULARITY 1;            -- index one key's subcolumn
```

**Listing 1.** Known-key reads are subcolumn reads; key presence and rare keys fall back to the keys/values arrays.

## Searching Nested

A `Nested(k String, v UInt64)` is stored as `Array(String) k` and `Array(UInt64) v` — per-row parallel arrays. Search means `ARRAY JOIN` to unnest rows ([[What is ARRAY JOIN in ClickHouse]]), then filter, or predicate directly with `has(arr, x)` / `arrayExists(x -> x > 10, arr)` without unnesting. Column names containing dots and dot-prefixed columns are interpreted as flattened Nested when `flatten_nested = 1` (the default), which the docs flag as a source of surprising insert validation — prefer underscores unless you intend Nested semantics.

> [!warning] The whole map is not skipped as one unit
> Skip indexes attach to expressions — a specific key subcolumn or `mapKeys(m)` — not to "the map" in general; searching an arbitrary absent key reads the keys array for every surviving granule. And querying an unknown key cannot use the typed-subcolumn fast path at all. If most searches target keys you cannot enumerate, that is the documented signal to switch to the JSON type or restructure into a real child table.

> [!tip] Interview answer
> Maps are stored as keys and values arrays with per-key subcolumns, so known-key filters read one subcolumn, mapContains and mapKeys handle key search, and you can put a set or Bloom index on a specific key expression. Nested is parallel arrays — search with ARRAY JOIN or array functions. For open-ended key sets, the JSON type with dynamic paths is the better fit.
