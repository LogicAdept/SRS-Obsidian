<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# How does ClickHouse accelerate LIKE and substring search?

> [!abstract] Short answer
> Three layers, cheapest first: tokenized predicates (`hasToken`, `equals`, `IN`) served by a `text` index; whole-word `LIKE '%word%'` patterns served by `tokenbf_v1`; and true substring search via `ngrambf_v1` — the only classic option for needles without token boundaries. Beyond skipping, scalar substring functions use SIMD, and column-level codecs keep string data compact.

## The decision path

Start by asking whether the needle has token structure. If yes — error ids, class names, event keywords — index the column with a [[What is a text index in ClickHouse]] and query with `hasToken`/`hasAllTokens`, which gives exact pruning. If the pattern must match inside words (`'%tion of the%'`), tokens cannot help; an n-gram Bloom filter splits both column and needle into overlapping n-grams so `LIKE` and `startsWith` predicates prune blocks — with false positives and bigger filters as the price ([[What is ngrambf_v1 versus tokenbf_v1]]). Leading-wildcard `LIKE` on a plain indexed column prunes nothing — the same limitation as B-tree leading wildcards in row stores ([[Why does LIKE with a leading wildcard not use a B-tree index]]).

```sql
-- token search: exact index pruning
SELECT count() FROM logs WHERE hasToken(msg, 'timeout');
-- substring search: n-gram Bloom filter pruning
ALTER TABLE logs ADD INDEX ngr msg TYPE ngrambf_v1(3, 1024, 3, 0) GRANULARITY 1;
SELECT count() FROM logs WHERE msg LIKE '%segmentation fault%';
```

**Listing 1.** Token predicate on a text index versus substring predicate on an n-gram index.

## Below the index layer

Even without an index, ClickHouse's substring and matching functions (`like`, `position`, `match`) are SIMD-vectorized over granule-sized batches, so raw scans are fast in absolute terms; and for repeated analysis of the same text, materialized lowercase copies or projections reduce read volume. For large-scale log search the whole toolkit composes with the data model — see [[How do you search logs in ClickHouse]] — and with the version caveats of the text index ([[What is hasToken in ClickHouse]] documents the custom-tokenizer edge).

> [!warning] n-gram parameters are a false-positive dial, not a switch
> Small `n` (2-3) matches short needles but explodes the Bloom filter over long columns; large `n` keeps filters small but misses needles shorter than `n` — a search for `'err'` cannot be pruned by an n=5 index. Sizing `n`, filter bytes, and hash functions against real data is a measurement exercise, and the docs now steer new full-text workloads to the text index instead of tuning these knobs.

> [!tip] Interview answer
> ClickHouse accelerates text search by predicate shape: token predicates get exact pruning from the inverted text index; word-level LIKE patterns get token Bloom filters; genuine substrings need n-gram Bloom filters or scan with SIMD. The key interview point is that leading-wildcard LIKE is not index-free magic here either — you pick the structure that matches the needle.
