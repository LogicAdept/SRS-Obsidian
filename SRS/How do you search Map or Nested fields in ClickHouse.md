<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# How do you search Map or Nested fields in ClickHouse

> [!abstract] Short answer
> For Map columns, query by key or value with mapKeys/mapValues and index those expressions with bloom-based or text skip indexes — the docs explicitly support applying bloom filters to maps via mapKeys or mapValues. For Nested columns, either address the arrays directly (array functions, ARRAY JOIN) or explode with ARRAY JOIN and filter; skip indexes on arrays test every element.

## Map: read the key, index the projection

ClickHouse Map columns support element access via the map['key'] subscript syntax and via dedicated functions (mapKeys, mapValues, mapContains). Equality on a known key, `map['user_id'] = 42`, is a normal predicate and can be served by the primary key if the expression is part of the ORDER BY (a common denormalization), or by skip indexes on the extracted expression. The skip-index documentation states the important capability directly: bloom filter indexes can be applied to maps by converting keys or values with mapKeys or mapValues, since every value of the array is tested. The token bloom and text index also accept Map, with the same caveat that only granule-level exclusion is provided, per [[What data skipping indexes exist in ClickHouse]].

```sql
CREATE TABLE events
(
    ts       DateTime,
    attrs    Map(String, String),
    INDEX idx_attr_keys (mapKeys(attrs)) TYPE bloom_filter(0.025) GRANULARITY 4,
    INDEX idx_attr_vals (mapValues(attrs)) TYPE bloom_filter(0.025) GRANULARITY 4
) ENGINE = MergeTree ORDER BY ts;

SELECT count() FROM events WHERE attrs['service'] = 'billing';
```

**Listing 1.** Bloom skip indexes over mapKeys/mapValues let granules without the key or value be skipped.

## Nested: array predicates and explosion

Nested columns are arrays of parallel columns (nested.Key1, nested.Value1), so search is either element-wise predicates — has(array, value), arrayExists, indexOf — or a lateral explosion with ARRAY JOIN that turns each element into a row before filtering. Bloom skip indexes apply to arrays element-wise, so an INDEX on the nested array column lets granules lacking the value be skipped before the array functions run, per the same skip-index mechanics. For deep JSON-shaped data the parallel PostgreSQL toolset is GIN over jsonb, described in [[How do you search JSON fields efficiently in SQL]], and the granule-exclusion verification is identical to other skip structures — EXPLAIN indexes = 1, per [[How do you verify a ClickHouse index is used]]. The text-flavored variant (token search inside map or nested strings) rides the same machinery as [[What is hasToken in ClickHouse]].

> [!warning] "Skip index on the map column" is not a thing by itself
> Skip indexes are defined on expressions, and a raw Map/Array expression needs the right index type and a functional form that the index supports: minmax will never apply to array or map expressions (the docs say so explicitly), bloom indexes require the mapKeys/mapValues projection, and text/token structures have their own expectations. Declaring an index on the raw column and assuming it fires is exactly the failure that [[Why might a ClickHouse skip index not help]] dissects — verify granule counts, not DDL.

> [!tip] Interview answer
> For maps I filter with the subscript syntax and index the projections: bloom_filter over mapKeys or mapValues, or text indexes for token lookups — the docs call out exactly this application. For Nested I use array predicates or ARRAY JOIN to explode, and bloom indexes test elements so granules without the value are skipped. The rule to remember: skip indexes on structured types work on well-chosen expressions, and minmax never applies to arrays or maps.
