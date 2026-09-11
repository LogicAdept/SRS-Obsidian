<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `MERGE` ("upsert") applies a batch of changes to a target table in one statement: rows from the source that **match** the target on a key get `UPDATE`, unmatched source rows get `INSERT`, optionally unmatched target rows get `DELETE` — SQL:2003 syntax, standard in PostgreSQL (15+), Oracle and SQL Server. Engines without MERGE spell the same contract with `INSERT ... ON CONFLICT DO UPDATE` (SQLite, PostgreSQL 9.5+) or `ON DUPLICATE KEY UPDATE` (MySQL) ([[What integrity constraints exist in SQL]]).

The verified demo shows the SQLite/PostgreSQL ON CONFLICT dialect executing the upsert half of the contract: the second insert of an existing SKU *updates* (`qty = qty + 3` makes 8) instead of failing or duplicating — one atomic statement, no read-modify-write race. The full MERGE form matters for sync jobs: `MERGE INTO target USING (SELECT ...) src ON target.key = src.key WHEN MATCHED THEN UPDATE ... WHEN NOT MATCHED THEN INSERT ...` — batch reconciliation in one statement (PostgreSQL's MERGE reference documents the full clause set, including conditional WHEN clauses and DELETE). The race-condition story is the senior part: the naive "SELECT, then INSERT or UPDATE" from application code is a lost-update machine under concurrency — two transactions both see "absent", both insert, one crashes on the PK. MERGE/ON CONFLICT make the *engine* the arbiter: the insert attempt itself detects the conflict and switches to update atomically ([[Can the same primary key value appear in two rows of one table]]). Portability matrix worth quoting: MERGE — PostgreSQL 15+, Oracle, SQL Server, DB2; ON CONFLICT — SQLite, PostgreSQL 9.5+; MySQL — ON DUPLICATE KEY UPDATE. The classic MERGE footgun (SQL Server folklore): source rows matching the same target row twice error out — dedupe the source first.

```sql
CREATE TABLE stock (sku TEXT PRIMARY KEY, qty INTEGER);
INSERT INTO stock VALUES ('a', 5);
INSERT INTO stock VALUES ('a', 3)
  ON CONFLICT(sku) DO UPDATE SET qty = qty + 3;
-- (ok: the conflicting row UPDATED, not rejected)
SELECT * FROM stock;
-- a|8
-- (the standard's MERGE shape, PostgreSQL syntax:
--  MERGE INTO stock s USING (VALUES ('a', 3)) v(sku, qty)
--  ON s.sku = v.sku
--  WHEN MATCHED THEN UPDATE SET qty = s.qty + v.qty
--  WHEN NOT MATCHED THEN INSERT VALUES (v.sku, v.qty);)
```

**Listing 1.** Verified on SQLite 3.53.1 for the ON CONFLICT form — quantity 5 plus 3 becomes 8 atomically; the MERGE block shows the SQL-standard spelling of the same contract (PostgreSQL syntax, per its reference).

```d2
direction: right
src: "source rows
(batch / feed)" {width: 150; height: 70}
m: "MERGE on key
match?" {width: 140; height: 80}
u: "WHEN MATCHED
UPDATE" {width: 150; height: 70}
i: "WHEN NOT MATCHED
INSERT" {width: 160; height: 70}
src -> m
m -> u
m -> i
```

**Fig. 1.** MERGE is a keyed reconciliation: each source row takes exactly one branch — update if its key exists, insert if it does not — atomically, without an application round-trip.

> [!warning] Race conditions live in the application spelling, not in the words "upsert"
> Check-then-write logic (SELECT absent -> INSERT) breaks under concurrency no matter how careful the code; only the engine-side atomic forms — MERGE, ON CONFLICT, INSERT IGNORE variants — remove the window. And MERGE needs a *unique* join key: two source rows hitting one target row is an error, so deduplicate the source first ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> MERGE is the standard one-statement upsert: source rows matched on a key update the target, unmatched ones insert, optionally deleting unmatched target rows — PostgreSQL 15, Oracle and SQL Server spell it MERGE; SQLite and older PostgreSQL use INSERT ON CONFLICT DO UPDATE, MySQL has ON DUPLICATE KEY UPDATE. My demo shows ON CONFLICT updating quantity 5 to 8 atomically. The reason it exists is the race: check-then-insert from application code loses updates under concurrency; the engine-side form makes the conflict resolution atomic — with the caveat that the merge key must be unique and the source deduplicated.
