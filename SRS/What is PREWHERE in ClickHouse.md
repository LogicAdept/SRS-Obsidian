<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/SQL #SRS

# What is PREWHERE in ClickHouse?

> [!abstract] Short answer
> PREWHERE is a two-stage filter: first read only the columns needed for the filter condition and evaluate it, then read the remaining requested columns only for surviving rows. It cuts I/O when the filter is more selective than the other columns — and it is automatic by default: `optimize_move_to_prewhere` (on since 23.2 in multi-step form) moves eligible WHERE conditions to PREWHERE for you.

## Mechanics

Without it, granules selected by the [[What is a sparse primary index in ClickHouse]] are read for *all* query columns before filtering. With PREWHERE, the filter columns are read and evaluated first; row masks of surviving rows gate the reads of the payload columns. ClickHouse orders multiple PREWHERE conditions by ascending uncompressed column size, cheapest filter first, so a small flag column filters before a big string is ever decompressed. Writing `PREWHERE` explicitly is supported to control which conditions run at this stage, and [[How do you verify a ClickHouse index is used]] remains the way to check the optimizer's choices — worth it when the optimizer's cost guess is wrong for your data; it is incompatible with queries whose filters cannot be evaluated column-wise in that order.

```sql
-- explicit form: filter on the small column before reading the payload
SELECT url, title
FROM hits
PREWHERE severity = 'ERROR'
WHERE timestamp >= now() - 3600;
```

**Listing 1.** A manual PREWHERE: `severity` (a low-cardinality flag) prunes rows before the wide `url`/`title` strings are read.

```d2
key: "Primary index\ngranule selection" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
fcol: "Read filter columns only\n(severity)" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
mask: "Row mask\nmatching rows" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
payload: "Read remaining columns\nonly for surviving rows" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
key -> fcol
fcol -> mask
mask -> payload
```

**Fig. 1.** The PREWHERE pipeline: filter columns are read and evaluated before payload columns enter memory.

> [!warning] PREWHERE is not free — and not a replacement for the sort key
> It pays when the filter reads far fewer rows than the payload columns; on wide-fanout predicates (nearly everything matches) it adds an extra column pass for nothing. And it complements, not replaces, key-column pruning ([[How do you choose ORDER BY in ClickHouse]]): PREWHERE still reads the filter column's granules, just not the other columns'. Measure with `optimize_move_to_prewhere` on and off, as the guide demonstrates, instead of sprinkling PREWHERE everywhere.

> [!tip] Interview answer
> PREWHERE splits filtering from projection: filter columns are read and evaluated first, then remaining columns are read only for matching rows — saving decompression of payloads that get discarded. ClickHouse does it automatically for eligible WHERE conditions and orders filters by column size; manual PREWHERE is for overriding its cost model when you know better.
