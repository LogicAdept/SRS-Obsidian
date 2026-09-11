<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> A **materialized view** stores the query's *result* on disk and serves reads from storage; it is refreshed (`REFRESH MATERIALIZED VIEW` in PostgreSQL) rather than live. The trade: reads skip the computation entirely (fast aggregates over big tables), but data is stale between refreshes and the refresh itself is a full recompute (optionally `CONCURRENTLY` to avoid blocking readers). SQLite and MySQL have no materialized views — the pattern is emulated with summary tables plus triggers or scheduled jobs ([[What is a SQL view and what is it used for]]).

The decision is staleness-versus-latency: a dashboard aggregate over 100M rows recomputed on every page view is a COUNT-scan tax per request; materialized, it is one indexed read plus a refresh schedule everyone agrees on. PostgreSQL's documentation frames it exactly this way: `CREATE MATERIALIZED VIEW ... AS query` populates at creation, `REFRESH MATERIALIZED VIEW` recomputes (with data changes visible only after refresh), `WITH NO DATA` defers population, and `REFRESH ... CONCURRENTLY` lets readers continue during refresh at the cost of requiring a unique index on the matview. The verified demo demonstrates the *plain-view half* of the contrast on SQLite — the view always sees new rows — which is precisely the behavior the materialized view gives up until refresh. Emulation stories round out the answer: a summary table maintained by triggers (write-time cost, always fresh) or by a scheduled job (read-time staleness, batched cost) — the same two poles as matview versus view ([[How do you optimize COUNT star on a large table]]). The naming trap to close with: PostgreSQL's `REFRESH` is *not* incremental by default (full recompute; IVM extensions exist but are not core).

```sql
CREATE TABLE items (id INTEGER PRIMARY KEY, title TEXT, price NUMERIC);
INSERT INTO items VALUES (1,'a',10),(2,'b',20);
CREATE VIEW cheap AS SELECT title, price FROM items WHERE price < 15;
INSERT INTO items VALUES (3,'c',12);
SELECT COUNT(*) FROM cheap;
-- 2
-- (a plain view counts the new row instantly.
--  A MATERIALIZED view (PostgreSQL) would answer from its stored snapshot
--  until: REFRESH MATERIALIZED VIEW cheap;)
```

**Listing 1.** Verified on SQLite 3.53.1 for the view half — live semantics; the materialized half is PostgreSQL's documented contract: stored result, explicit refresh, staleness window.

```d2
direction: right
w: "write happens" {width: 140; height: 60}
v: "plain view
next read sees it" {width: 190; height: 70}
m: "matview
stored snapshot until refresh" {width: 240; height: 80}
r: "REFRESH
full recompute (CONCURRENTLY optional)" {width: 250; height: 80}
w -> v
w -> m
m -> r
```

**Fig. 1.** Writes propagate instantly through a plain view; a materialized view stands still on its stored result until an explicit refresh recomputes it.

> [!warning] Refresh is a full query run at refresh time — schedule it like a batch job
> A heavy matview refresh inside business hours competes with production traffic for the same I/O; CONCURRENTLY trades extra work for availability. And a matview whose underlying tables churn faster than it refreshes serves averages of the past — know the staleness budget before promising numbers ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> A materialized view stores the query result on disk and serves reads from storage, refreshed explicitly — PostgreSQL's REFRESH MATERIALIZED VIEW, optionally CONCURRENTLY with a unique index — while a plain view re-runs live. I reach for matviews on expensive aggregates read far more often than the data changes, and I name the costs: staleness between refreshes, full recompute at refresh, and the emulation pattern of summary tables where the engine lacks them, maintained by triggers or jobs.
