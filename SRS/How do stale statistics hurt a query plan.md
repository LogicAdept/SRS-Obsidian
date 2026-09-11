<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> The planner is only as good as its **statistics**: row counts, distinct-value counts, and value distributions per column. When they are stale (after bulk loads, mass deletes, or skewed updates), the planner estimates wrong row counts, picks the wrong join order or access path, and queries degrade from milliseconds to seconds with *no query change at all*. PostgreSQL: `ANALYZE` (manual or autovacuum) refreshes them; SQLite: `ANALYZE` populates `sqlite_stat1` ([[How do you systematically diagnose a slow SQL query]]).

The cost-based planner is an estimation machine: PostgreSQL's documentation describes the planner consulting `pg_class` sizes and per-column statistics (including most-common-values histograms) to estimate selectivity, and those estimates decide join order, join algorithm, and index versus scan. A stale histogram that says "amount > 100 matches 5 rows" when it now matches 5 million flips nested-loop plans into catastrophes. The demo verifies what statistics *are* on SQLite: after `ANALYZE`, `sqlite_stat1` holds `table | index | rows avg-rows-per-key` — literally the inputs the planner reads; SQLite's query-planner documentation states these are exactly what lets it choose join orders and indexes. Diagnosing staleness: compare EXPLAIN-estimated rows to actual rows (EXPLAIN ANALYZE) — divergence by an order of magnitude is the signature ([[What do cost rows and loops mean in EXPLAIN]]). Fixes: refresh statistics (PostgreSQL `ANALYZE tablename`, autovacuum's analyzer; SQLite `ANALYZE`), raise sampling detail (`default_statistics_target`), or pin a good plan (`pg_hint_plan`-style extensions, planner method settings) as a last resort ([[What is a query plan in a relational database]]).

```sql
CREATE TABLE skew (id INTEGER PRIMARY KEY, v INTEGER, payload TEXT);
INSERT INTO skew (v, payload) SELECT 1, '0123456789abcdef0123456789abcdef'
FROM (SELECT 1 UNION ALL SELECT 1) a, (SELECT 1 UNION ALL SELECT 1) b,
 (SELECT 1 UNION ALL SELECT 1) c, (SELECT 1 UNION ALL SELECT 1) d,
 (SELECT 1 UNION ALL SELECT 1) e, (SELECT 1 UNION ALL SELECT 1) f,
 (SELECT 1 UNION ALL SELECT 1) g, (SELECT 1 UNION ALL SELECT 1) h,
 (SELECT 1 UNION ALL SELECT 1) i, (SELECT 1 UNION ALL SELECT 1) j,
 (SELECT 1 UNION ALL SELECT 1) k, (SELECT 1 UNION ALL SELECT 1) l,
 (SELECT 1 UNION ALL SELECT 1) m, (SELECT 1 UNION ALL SELECT 1) n;
INSERT INTO skew VALUES (99999, 2, 'rare');
CREATE INDEX idx_v ON skew(v);
ANALYZE;
SELECT tbl, idx, stat FROM sqlite_stat1 WHERE tbl = 'skew';
-- skew|idx_v|16385 8193
-- (16385 index rows, average 8193 rows per distinct v)
```

**Listing 1.** Verified on SQLite 3.53.1. `ANALYZE` wrote the fact the planner needs: the table has 16385 rows and v averages 8193 rows per value — so a lookup on the rare value is cheap, on the common value is a half-table read, and the planner now knows which is which.

```d2
direction: right
d1: "data changes
bulk load / skew shift" {width: 200; height: 70}
s1: "statistics stale
estimates wrong" {width: 180; height: 70}
p1: "planner chooses
wrong plan shape" {width: 190; height: 70}
q1: "queries degrade
same SQL, slower" {width: 180; height: 70}
d1 -> s1 -> p1 -> q1
```

**Fig. 1.** Staleness propagates silently: data changes first, estimates second, plans third, latency last — by which point nothing in the SQL looks guilty.

> [!warning] The plan degrades without any query change — alarms blame the wrong thing
> Because the SQL text is unchanged, staleness masquerades as "the database got slow" and triggers wasted investigation of application code. The first responder question after a bulk load or mass update is "when did statistics last refresh" — PostgreSQL's pg_stat_user_tables.last_analyze answers it directly ([[How do you identify slow or non-performant SQL queries]]).

> [!tip] Interview answer
> Statistics are the planner's model of the data — row counts, distinct values, histograms — and staleness means estimates are wrong, so join orders and access paths get chosen against reality: same SQL, sudden seconds. I diagnose by comparing estimated rows in EXPLAIN with actual rows in EXPLAIN ANALYZE; divergence by orders of magnitude points at stats. The fix is ANALYZE — manual after bulk loads, autovacuum or scheduled jobs otherwise — and SQLite shows the same idea through sqlite_stat1 that ANALYZE populates.
