<!--
reps: 0
priority: 0
-->
#Databases/OLAP/ClickHouse #SRS

# How do you materialize a skip index on existing ClickHouse data

> [!abstract] Short answer
> ALTER TABLE ... ADD INDEX only defines the index and applies it to parts written afterwards. To build it over already existing data, run ALTER TABLE ... MATERIALIZE INDEX name [IN PARTITION ...], which recomputes the index on old parts as a mutation. Without materialization, queries over historical data see no skipping at all.

## The two statements and what each touches

The skip-index guide demonstrates the sequence on its 100-million-row table: add the index with ALTER TABLE ... ADD INDEX vix my_value TYPE set(100) GRANULARITY 2, then note that skip indexes are normally applied only to newly inserted data, and run ALTER TABLE skip_table MATERIALIZE INDEX vix to index existing parts. After materialization the demo query drops from processing 100 million rows to about 33 thousand — four granules. The mutation form optionally takes IN PARTITION to scope the rebuild. The same flow applies to the text index and other skip structures, and the docs note the materialization runs like any mutation: background, resource-consuming, and trackable in system.mutations.

```sql
ALTER TABLE logs ADD INDEX msg_text message TYPE text(tokenizer splitByNonAlpha) GRANULARITY 4;
ALTER TABLE logs MATERIALIZE INDEX msg_text;                 -- rebuild on existing parts
ALTER TABLE logs MATERIALIZE INDEX msg_text IN PARTITION '202608';  -- scoped variant
```

**Listing 1.** Define, then materialize; scope by partition when a full-table mutation is too heavy.

## Cost model and operational practice

Materialization rewrites per-part index files, so plan disk, I/O, and merge pressure accordingly — the guide's own framing is that you should plan for the disk and CPU cost of building the index, and the mutation executes per part like UPDATE/DELETE mutations do. The verification loop after materialization matters as much as the command: before it, EXPLAIN shows no skip on old parts (the classic false negative, part of [[Why might a ClickHouse skip index not help]]); after it, EXPLAIN indexes = 1 should show the Skip index eliminating granules, per [[How do you verify a ClickHouse index is used]]. If the materialized index still skips nothing, the problem is correlation or predicate shape, not the command — the fix paths run through [[How do you choose ORDER BY in ClickHouse]] or the index-type menu in [[What data skipping indexes exist in ClickHouse]].

> [!warning] "ADD INDEX is enough" is the trap the docs call out verbatim
> The guide states plainly that just adding the index won't affect the earlier query until materialization runs. The reverse trap is firing MATERIALIZE INDEX on a huge table during peak load without scoping by partition — it is a mutation, competing with merges and ingest. Also, dropping and re-adding an index definition does not rebuild anything by itself; materialization is always an explicit step.

> [!tip] Interview answer
> ADD INDEX defines the structure and covers only future parts; MATERIALIZE INDEX builds it over existing data as a mutation, optionally scoped with IN PARTITION. Until materialization runs, historical queries get zero benefit — the guide's example goes from 100 million rows processed to 33 thousand after it. I schedule the mutation off-peak, then confirm granule elimination with EXPLAIN indexes = 1.
