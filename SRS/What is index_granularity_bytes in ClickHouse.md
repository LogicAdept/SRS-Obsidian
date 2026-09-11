<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #Databases/Indexes #SRS

# What is index_granularity_bytes in ClickHouse?

> [!abstract] Short answer
> `index_granularity_bytes` turns on adaptive index granularity: instead of a fixed 8192 rows per granule, ClickHouse closes a granule once it reaches roughly this many bytes — 10485760 (10 MiB) by default, with a floor of `min_index_granularity_bytes` = 1024. Setting it to 0 disables adaptivity and makes granules exactly `index_granularity` rows.

## What adaptivity buys you

With adaptive granularity, small-insert parts get small granules — the same granule unit the [[What is a sparse primary index in ClickHouse]] indexes one mark of ([[What is a granule in ClickHouse]]) — a part holding 300 rows has one granule either way, but a part of very wide rows (big `String`/`JSON` payloads) produces far fewer, byte-sized granules than a strict 8192-row slicing would. Queries then skip data in proportion to bytes rather than rows, and background merges produce well-sized granules from mixed input parts. The classic use case is high-cardinality string data where 8192 rows can be hundreds of megabytes; the counter-case — tiny granules, more marks, more per-granule overhead — is why the minimum is bounded and why the docs still default `index_granularity = 8192` as the row cap.

```sql
SELECT
    name,
    engine_full
FROM system.tables
WHERE name IN ('t_fixed', 't_adaptive');
-- t_fixed:    ... SETTINGS index_granularity = 8192
-- t_adaptive: ... index_granularity = 8192 index_granularity_bytes = 10485760
```

**Listing 1.** Both settings coexist: adaptive mode closes a granule at whichever limit — rows or bytes — is hit first; `engine_full` shows the effective configuration.

```d2
rows: "Incoming sorted rows" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
bytes: "bytes >= index_granularity_bytes?\n(10 MiB default)" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
rows8192: "rows >= index_granularity?\n(8192 default)" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
close: "Close granule\nemit mark" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
rows -> bytes
bytes -> close: yes
bytes -> rows8192: no
rows8192 -> close: yes
```

**Fig. 1.** Adaptive granularity closes a granule on whichever threshold — bytes or rows — the sorted stream reaches first.

> [!warning] Do not shrink it "for faster lookups"
> Dropping `index_granularity_bytes` to a few kilobytes multiplies the number of marks: the index grows, per-granule bookkeeping inflates, and merges do more work — often the opposite of the intended speedup. Point-lookup weakness comes from the sparse design ([[When should you not use ClickHouse]]), not from granule size, and it is better fixed with projections or a row store.

> [!tip] Interview answer
> It is the adaptive-granularity control: a granule closes at ~10 MiB of data by default instead of exactly 8192 rows, with 0 disabling adaptivity. This lets granule size follow real data size — useful for wide rows — at the cost of more marks. It works together with `index_granularity`, which remains the row cap.
