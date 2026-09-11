<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# What is LowCardinality in ClickHouse?

> [!abstract] Short answer
> `LowCardinality` is a data-type wrapper that switches a column to dictionary encoding: values are stored as integer codes into a per-part dictionary. It is effective when a column has few distinct values — up to roughly 10,000 is efficient per the docs — and can hurt when a column has more than 100,000 distinct values, where plain types perform better.

## Mechanics

Internally the column becomes a numeric code array plus a dictionary; operations compare and join codes instead of strings, which both shrinks storage and accelerates `GROUP BY`, `DISTINCT`, and equality filters. It composes with string, numeric, date, and UUID types — `LowCardinality(String)` for things like country, status, or event_name is the canonical case. Dictionary-encoded columns compress better too, since repeated codes are trivially compressible — see [[How does ClickHouse compress data]] for the codec layer that stacks on top.

```sql
CREATE TABLE events
(
    ts         DateTime,
    region     LowCardinality(String),   -- ~50 distinct values: ideal
    user_id    UInt64                    -- millions of values: no LowCardinality
)
ENGINE = MergeTree ORDER BY (region, ts);

SELECT region, count() FROM events GROUP BY region;  -- codes, not strings
```

**Listing 1.** Dictionary encoding pays on the grouping column; the high-cardinality identifier stays plain.

## Where the guidance comes from

The threshold is about dictionary churn: every new distinct value adds an entry, and a dictionary growing alongside the data erodes the fixed-width code advantage while increasing memory per part. The docs frame it as a rule of thumb — efficient below ~10K distinct values, potentially worse than ordinary types above 100K. Note the interplay with the sort key: a low-cardinality column is often a good *early* key column ([[How do you choose ORDER BY in ClickHouse]]), and the same cardinality reasoning appears in index-column debates — compare [[Does it make sense to index low-cardinality columns]] for the B-tree-side discussion in row stores.

> [!warning] LowCardinality(String) is not free storage for enums that grow
> Wrapping a column that quietly accumulates values (URL paths, error messages, user agents) degrades toward the 100K cliff, and older parts keep their own dictionaries — "temporary explosion" is the documented failure mode. Measure distinct counts first (`uniq()`, `uniqExact()`) rather than assuming a column stays small forever.

> [!tip] Interview answer
> LowCardinality swaps a column for dictionary-coded integer references — a big win for equality filters, GROUP BY, and storage when the column truly has under ~10K distinct values, and a measurable loss above ~100K. It is the standard wrapper for categorical strings in ClickHouse, but it requires actually knowing the cardinality profile of your data.
