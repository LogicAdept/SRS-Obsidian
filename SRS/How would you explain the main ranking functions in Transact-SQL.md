<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> The T-SQL (and standard) ranking functions, all evaluated over a window (`OVER (PARTITION BY ... ORDER BY ...)`): **ROW_NUMBER** — unique sequential numbers regardless of ties; **RANK** — ties share a rank, the next rank *skips* (1, 2, 2, 4); **DENSE_RANK** — ties share, no gaps (1, 2, 2, 3); **NTILE(n)** — buckets rows into n near-equal groups; plus **PERCENT_RANK**/**CUME_DIST** for relative position. SQLite and PostgreSQL implement the same set — the syntax is portable; T-SQL's documentation merely popularized the family ([[How would you explain the SQL ORDER BY clause]]).

The verified demo shows all three core ranks on deliberately tied data: in department 1, Greta (5000) leads; Hans and Ivan share 3500 — ROW_NUMBER breaks the tie arbitrarily (2, 3), RANK gives both 2 then skips to 4 for the next distinct value, DENSE_RANK gives 2, 2 with no gap — and department 2's tie (Julia, Kim at 4000) repeats the pattern. That tie behavior *is* the interview: "which rank do you need for top-N per group" — DENSE_RANK when N means "N distinct values" (second-highest *salary*), ROW_NUMBER when N means "N rows" (top-3 rows even if tied), RANK when competition-style numbering matters (1, 2, 2, 4). NTILE(2) over the five salaries splits 3/2 — the first tile holds Greta, Julia, Kim; the documented distribution rule is front-loaded remainders, which is why tiles differ by at most one row. Performance notes worth a sentence: ranking functions require the window ORDER BY (a sort unless an index supplies it), and the PARTITION boundary is what restarts numbering — the same machinery that makes running totals work ([[What are the main SQL aggregate functions]], [[How does LIMIT interact with ORDER BY and indexes]]).

```sql
SELECT name, dept_id, salary,
  ROW_NUMBER() OVER w AS row_num,
  RANK()       OVER w AS rnk,
  DENSE_RANK() OVER w AS drnk
FROM employees
WINDOW w AS (PARTITION BY dept_id ORDER BY salary DESC)
ORDER BY dept_id, rnk, name;
-- Greta|1|5000|1|1|1
-- Hans|1|3500|2|2|2
-- Ivan|1|3500|3|2|2
-- Julia|2|4000|1|1|1
-- Kim|2|4000|2|1|1
SELECT name, NTILE(2) OVER (ORDER BY salary DESC) AS tile
FROM employees ORDER BY tile, name;
-- Greta|1
-- Julia|1
-- Kim|1
-- Hans|2
-- Ivan|2
```

**Listing 1.** Verified on SQLite 3.53.1. The 3500 tie shows the whole family at once — ROW_NUMBER 2/3, RANK 2/2 with the next rank skipping to 4, DENSE_RANK 2/2 gapless — and NTILE splits 5 rows into 3+2 buckets.

```d2
direction: right
r1: "ROW_NUMBER
1 2 3
ties broken arbitrarily" {width: 190; height: 90}
r2: "RANK
1 2 2 4
gaps after ties" {width: 180; height: 90}
r3: "DENSE_RANK
1 2 2 3
ties share, no gaps" {width: 190; height: 90}
r4: "NTILE(n)
near-equal buckets" {width: 180; height: 90}
```

**Fig. 1.** Four numberings of the same ordered rows: position, competition ranks with gaps, packed ranks, and quantile buckets — the ORDER BY supplies order, the function supplies the numbering contract.

> [!warning] ROW_NUMBER's tie-breaking is non-deterministic — paginating on it needs a unique key
> With tied ORDER BY values, which tied row gets row 2 versus row 3 can change between runs and plans; top-N-per-group filters built on bare ROW_NUMBER can return *different rows* next execution. Add the unique id as the final window ORDER BY key when the choice must be stable ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> The ranking family works over a window: ROW_NUMBER numbers rows uniquely with ties broken arbitrarily, RANK shares ranks on ties and skips the next one — 1, 2, 2, 4 — DENSE_RANK shares without gaps, NTILE(n) buckets into near-equal tiles, PERCENT_RANK and CUME_DIST give relative positions. My demo shows a salary tie rendering all three behaviors side by side. I choose by meaning: distinct-value N needs DENSE_RANK, row-count N needs ROW_NUMBER with a unique tiebreaker, and quantile reporting uses NTILE.
