<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> `SELECT` is the DML statement that **retrieves a result set** from the database. Its core flow is: pick columns (`SELECT list`), pick the source (`FROM`, with joins), filter rows (`WHERE`), group and aggregate (`GROUP BY`, `HAVING`), sort (`ORDER BY`), and cut a page (`LIMIT`/`OFFSET` or `FETCH FIRST`). The result of a `SELECT` is itself a table-like set — which is why queries nest and compose.

The full pipeline the engine applies is longer than the five clauses most people name: `FROM`/joins → `WHERE` → `GROUP BY` → `HAVING` → `SELECT` (expressions and aliases) → `DISTINCT` → `ORDER BY` → `LIMIT/TOP` ([[What is the logical order of SQL SELECT execution]]). Knowing that order explains most surprises: column aliases from the `SELECT` list are not visible to `WHERE`, but are visible to `ORDER BY`; aggregate filters go in `HAVING`, row filters in `WHERE` ([[What is the difference between SQL WHERE and HAVING clauses]]).

Beyond column picking, `SELECT` shapes *shape itself*: `*` means all columns (fine in interactive debugging, costly in production because it drags every column over the wire and defeats covering indexes — [[Why is SELECT star a performance problem]]), expressions compute derived values, aliases name outputs, and `DISTINCT` collapses duplicates. Join types in `FROM` decide row multiplication — an inner join keeps matches, outer joins keep unmatched sides too, and a bad join condition can multiply rows ([[Why can a JOIN multiply your row count]]).

```sql
CREATE TABLE t (name TEXT, score INTEGER);
INSERT INTO t VALUES ('Ada',90),('Bo',75),('Cy',90),('Di',60);

SELECT name, score          -- projection: which columns
FROM t                      -- source
WHERE score >= 75           -- row filter
ORDER BY score DESC, name   -- sort (DESC first key, name as tiebreak)
LIMIT 3;                    -- page
-- Ada|90
-- Cy|90
-- Bo|75
```

**Listing 1.** Verified on SQLite 3.53.1. The same statement in the ANSI style ends `FETCH FIRST 3 ROWS ONLY` instead of `LIMIT 3`; T-SQL writes `SELECT TOP 3 ...`. Clause roles are identical across dialects.

```d2
direction: right
from: "FROM + joins\nrow source" {width: 180; height: 80}
where: "WHERE\nfilter rows" {width: 150; height: 80}
group: "GROUP BY + HAVING\naggregate" {width: 200; height: 80}
select: "SELECT\nproject, alias" {width: 170; height: 80}
order: "ORDER BY\nsort" {width: 140; height: 80}
limit: "LIMIT\npage" {width: 130; height: 80}
from -> where -> group -> select -> order -> limit
```

**Fig. 1.** Clause order in the source text matches the engine's logical pipeline — that is why an alias defined in `SELECT` reaches `ORDER BY` but not `WHERE`.

> [!warning] `ORDER BY` without a unique tiebreak column is not deterministic
> Rows that compare equal on the sort keys may come back in any order (and in any order on each execution). Paginating with `LIMIT/OFFSET` over such a query can repeat or skip rows between pages; add a unique key as the final sort column ([[How does LIMIT interact with ORDER BY and indexes]]).

> [!tip] Interview answer
> SELECT retrieves a result set: FROM with joins builds the row source, WHERE filters rows, GROUP BY and HAVING aggregate and filter groups, the SELECT list projects and names output, then DISTINCT, ORDER BY, and LIMIT finish. Because the result is a table-like set, queries compose and nest. The classic follow-up is clause order: aliases exist after the SELECT step, so WHERE cannot see them while ORDER BY can.
