<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How would you explain VIEW vs MATERIALIZED VIEW?

> [!abstract] Short answer
> **View**: stored query, zero storage, always current, pays the query cost on every read. **Materialized view**: stored *result*, pays at refresh time, reads are fast but see a snapshot. Choose by freshness requirement and read/write ratio: live correctness -> view; expensive aggregate read many times -> matview with a refresh policy ([[What is a SQL view and what is it used for]], [[How would you explain MATERIALIZED VIEW]]).

The contrast is two costs moved around, and the verified demo pins the live half: after an INSERT into the base table, the plain view's COUNT(*) includes the new row immediately — a matview would still report the snapshot count until refreshed. The full decision table: correctness-critical numbers (balances, inventory) tolerate no staleness — plain view (or query directly); dashboards over huge tables tolerate minutes of staleness — matview; PostgreSQL-only syntax is fine there, while SQLite/MySQL need summary-table emulation with triggers or jobs. The subtleties that separate candidates: a matview's refresh is a *full* recompute (PostgreSQL core has no incremental refresh), so refresh cost scales with the defining query, not with changed rows; `REFRESH ... CONCURRENTLY` needs a unique index and buys non-blocking reads; a plain view's cost can still be *low* if its predicates are index-covered — the view/matview choice is not automatically slow/fast, it is recompute-per-read versus recompute-per-refresh ([[How do you optimize COUNT star on a large table]]). Security also differs: both hide columns, a matview can even denormalize *less* sensitive copies while the base table keeps strict grants ([[What integrity constraints exist in SQL]]).

```sql
CREATE TABLE items (id INTEGER PRIMARY KEY, title TEXT, price NUMERIC);
INSERT INTO items VALUES (1,'a',10),(2,'b',20);
CREATE VIEW cheap AS SELECT title, price FROM items WHERE price < 15;
INSERT INTO items VALUES (3,'c',12);

SELECT COUNT(*) FROM cheap;
-- 2
-- (plain view: live, sees the new row.
--  A matview would answer 1 from its stored snapshot
--  until REFRESH MATERIALIZED VIEW runs.)
SELECT * FROM cheap;
-- a|10
-- c|12
```

**Listing 1.** Verified on SQLite 3.53.1 (live half). The count includes the just-inserted row and the listing shows it — the exact moment where view and materialized view semantics diverge.

```d2
direction: right
q: "read request" {width: 130; height: 60}
v: "view
recompute now
always current" {width: 170; height: 80}
m: "matview
read stored snapshot
refresh on schedule" {width: 200; height: 90}
c: "correctness first" {width: 150; height: 60}
d: "speed first,
staleness budgeted" {width: 160; height: 60}
q -> v -> c
q -> m -> d
```

**Fig. 1.** One read request, two service models: recompute-and-be-right, or fetch-and-be-fast — the freshness requirement picks the branch.

> [!warning] A matview is a promise about staleness — write it down
> "Reports may lag up to N minutes" is a product decision, not an implementation detail; when the underlying data churns faster than refreshes, dashboards disagree with operational queries and the mismatch gets reported as a bug. Budget staleness explicitly, monitor refresh duration drift, and alarm when refresh stops fitting its window ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> View versus materialized view is recompute-per-read versus recompute-per-refresh: a view stores only the query and is always current — my demo shows it picking up an insert instantly — while a matview stores the result and serves reads from it until REFRESH, optionally CONCURRENTLY with a unique index. I choose by freshness: correctness-critical reads get views or raw queries; expensive, read-heavy aggregates get matviews with a written staleness budget; on engines without them, summary tables maintained by triggers or jobs emulate the trade.
