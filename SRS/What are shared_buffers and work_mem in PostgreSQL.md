<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #SRS

# What are shared_buffers and work_mem in PostgreSQL?

> [!abstract] Short answer
> shared_buffers is the server-wide cache of data pages shared by all backends (default 128 MB — deliberately small; production typically sets it to about a quarter of RAM). work_mem is per-operation private memory for sorts and hash tables — a single query can allocate it several times, so it is not "memory per query" (default 4 MB). They solve different problems: page cache versus per-operation working space.

## shared_buffers

The shared buffer pool caches heap and index pages; all backends read and write through it, guarded by its own locking. The default 128 MB exists so the binary runs everywhere — the documentation and common practice move it to roughly 25 percent of system RAM, leaving the rest for the OS page cache (which PostgreSQL relies on heavily — double caching is normal, not waste) ([[What is the PostgreSQL WAL]] — dirty buffer flushing is driven by checkpoints and the background writer).

```d2
disk: "Heap / index files" {width: 240; height: 60}
sb: "shared_buffers\nglobal page cache, all backends" {width: 340; height: 80}
osc: "OS page cache\nsecond layer, file-backed" {width: 300; height: 80}
wm: "work_mem\nper sort/hash operation,\nprivate to one backend" {width: 340; height: 90}
disk -> sb -> osc
wm: private
```

**Fig. 1.** Two cache layers plus private work memory; they multiply, not substitute.

## work_mem

Each sort node, hash build, and several other plan nodes may allocate up to work_mem before spilling to temporary files — and a query plan can contain several such nodes, each in every backend running it. The formula to fear: concurrent queries times nodes per query times work_mem. Spills show as temp read/written in EXPLAIN (ANALYZE, BUFFERS) ([[How do you read EXPLAIN ANALYZE in PostgreSQL]]).

```sql
-- 100 connections x a 3-sort query at 64 MB work_mem
-- = up to ~19 GB transient, before other memory
SET work_mem = '64MB';   -- scope it: session, role, or function - not global
```

**Listing 1.** The realistic sizing discipline: raise work_mem for the roles or statements that need it (ALTER ROLE ... SET work_mem), keep the global default modest.

## The pairing in answers

- shared_buffers too small: every read hits the OS cache or disk; hit ratios in pg_stat_database drop ([[How do you monitor database health and load]]).
- work_mem too small: sorts and hashes spill to temp files — the slow-but-correct failure.
- work_mem too large: OOM under concurrency ([[What is the difference between a process and a connection in PostgreSQL]] — per-backend memory multiplies).
- Related but separate: maintenance_work_mem (index builds, vacuum) and the planner's effective_cache_size hint ([[How does the PostgreSQL query planner choose a plan]]).

> [!warning] work_mem is not per query — and shared_buffers is not "use all the RAM"
> The two classic sizing errors in one card: setting work_mem to 1 GB because "the server has 32 GB" (multiplied by concurrent nodes and backends, it is an OOM generator), and setting shared_buffers to 90 percent of RAM (starves the OS cache PostgreSQL also uses). Sizing is a product of concurrency, not a percentage of memory.

> [!tip] Interview answer
> shared_buffers is the global shared page cache — default 128 MB, production around a quarter of RAM with the OS cache doing the rest. work_mem is private memory per sort or hash operation — default 4 MB — and one query can use it many times, so the real budget is concurrency times nodes times work_mem. Underprovisioning shows as cache misses and temp-file spills; overprovisioning shows as OOM.
