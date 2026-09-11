<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DDL #SRS

# What is the difference between a trigger and a rule in PostgreSQL

> [!abstract] Short answer
> **A trigger is a function that runs when a row event occurs** (`INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`) — it can modify `NEW`/`OLD`, run queries, raise exceptions, and is the standard mechanism for row-level logic. **A rule is a query-rewrite mechanism** that transforms one SQL statement into another before it reaches the executor — historically used to make views updatable, now mostly replaced by `INSTEAD OF` triggers on views. Use triggers for row-level behavior; use views (which compile to rules internally) for query composition; avoid hand-written rules on tables.

## The two mechanisms

A **trigger** is a function attached to a table or view. PostgreSQL fires it **per row** or **per statement** when the event matches. The function can:

- modify `NEW` before `INSERT`/`UPDATE` (`BEFORE` trigger);
- read `NEW`/`OLD` and run side-effect queries (`AFTER` trigger);
- redirect writes on a view to a base table (`INSTEAD OF` trigger on a view);
- raise an exception to veto the operation.

A **rule** is a query-rewrite entry. PostgreSQL rewrites the incoming parse tree before the planner sees it. The classic forms:

- `ON SELECT DO INSTEAD SELECT ...` — this is what `CREATE VIEW` compiles to internally (`_RETURN` rule).
- `ON INSERT DO INSTEAD ...` — historically how updatable views were built before `INSTEAD OF` triggers (PostgreSQL 9.1+).
- `ON INSERT DO ALSO ...` — append a second statement (e.g. an audit insert) without replacing the original.

```d2
direction: right
sql: "INSERT INTO view ..." {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
rule: "parse tree\nrewrite" {
  width: 200
  height: 60
  style.fill: "#fff3e0"
}
exec1: "executor runs\nrewritten INSERT into base table" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
sql2: "INSERT INTO table ..." {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
trigger: "BEFORE INSERT\ntrigger fires\nNEW.name_upper := upper(NEW.name)" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
exec2: "executor runs\nthe (modified) row" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
sql -> rule -> exec1
sql2 -> trigger -> exec2
```

**Fig. 1.** A rule rewrites the SQL parse tree before execution (left path — the classic view pattern). A trigger fires during execution, after the row is identified and before it is written (right path — the row-level logic pattern). Both can be made to do similar things, but the abstraction they expose is different.

## Verified on PostgreSQL 17.11

The empiric shows the three patterns side by side: a `BEFORE INSERT` trigger that sets a derived column; a rule that makes a view insertable; and an `INSTEAD` rule on a real table (the anti-pattern the spec warns against — kept here to show what it does).

```python
import psycopg

DSN = "host=/tmp user=postgres dbname=postgres"

with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("DROP VIEW IF EXISTS people_view")
    adm.execute("DROP TABLE IF EXISTS people")
    adm.execute("DROP TABLE IF EXISTS rule_demo")
    adm.execute("CREATE TABLE people (id int PRIMARY KEY, name text, name_upper text)")
    adm.execute("CREATE VIEW people_view AS SELECT id, name FROM people")
    adm.execute("""
        CREATE OR REPLACE FUNCTION people_set_upper() RETURNS trigger AS $$
        BEGIN
            NEW.name_upper := upper(NEW.name);
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """)
    adm.execute("""
        CREATE TRIGGER people_before_insert
            BEFORE INSERT OR UPDATE OF name ON people
            FOR EACH ROW
            EXECUTE FUNCTION people_set_upper()
    """)
    adm.execute("""
        CREATE RULE people_view_insert AS
            ON INSERT TO people_view DO INSTEAD
            INSERT INTO people (id, name) VALUES (NEW.id, NEW.name)
    """)

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("INSERT INTO people (id, name) VALUES (1, 'alice')")
    cur.execute("INSERT INTO people (id, name) VALUES (2, 'bob')")
    cur.execute("SELECT id, name, name_upper FROM people ORDER BY id")
    for r in cur.fetchall():
        print(f"  id={r[0]}  name={r[1]}  name_upper={r[2]}")

    cur.execute("INSERT INTO people_view (id, name) VALUES (3, 'carol')")
    cur.execute("SELECT id, name, name_upper FROM people WHERE id = 3")
    r = cur.fetchone()
    print(f"INSERT via view (rule rewrite): id={r[0]}  name={r[1]}  name_upper={r[2]}  (trigger still fires)")
    conn.commit()

# A rule on a real table (not a view): rewrite UPDATE into an INSERT.
# This is the "RULE-based magic" the spec warns against — kept as an anti-pattern demo.
with psycopg.connect(DSN, autocommit=True) as adm:
    adm.execute("CREATE TABLE rule_demo (id int, v int)")
    adm.execute("INSERT INTO rule_demo VALUES (1, 10)")
    adm.execute("""
        CREATE OR REPLACE RULE rule_demo_no_update AS
            ON UPDATE TO rule_demo DO INSTEAD
            INSERT INTO rule_demo VALUES (NEW.id, NEW.v)
    """)

with psycopg.connect(DSN) as conn:
    cur = conn.cursor()
    cur.execute("UPDATE rule_demo SET v = 99 WHERE id = 1")
    cur.execute("SELECT * FROM rule_demo ORDER BY id")
    for r in cur.fetchall():
        print(f"  id={r[0]}  v={r[1]}")
    conn.commit()
```

**Listing 1.** Source code run against PostgreSQL 17.11 (output in the next listing).

```text
  id=1  name=alice  name_upper=ALICE
  id=2  name=bob  name_upper=BOB
INSERT via view (rule rewrite): id=3  name=carol  name_upper=CAROL  (trigger still fires)
  id=1  v=10
  id=1  v=99
```
**Listing 2.** Verified on PostgreSQL 17.11. The `BEFORE INSERT` trigger on `people` sets `name_upper` for direct inserts. The `ON INSERT DO INSTEAD` rule on `people_view` rewrites the view insert into a base-table insert — and the trigger still fires on that rewritten insert, because the rewrite happens before execution. The `ON UPDATE DO INSTEAD` rule on `rule_demo` rewrites `UPDATE` into `INSERT`, so the original row survives and a new row appears — surprising behavior that is the reason hand-written rules on tables are discouraged.

## Why rules lost to triggers

The PostgreSQL manual (`rules.html`) is unusually direct: rules are a powerful but confusing mechanism, and most things you might do with a rule on a table are better done with a trigger. The reasons:

- **Rules fire once per statement, not per row.** A rule on `UPDATE` sees the rewritten query, not the individual rows. A `BEFORE UPDATE FOR EACH ROW` trigger sees each row.
- **Rule semantics interact with the planner in non-obvious ways.** A rule that adds an `ALSO` clause runs the original and the extra statement; a rule that uses `INSTEAD` replaces the original. Which one applies depends on the rule list ordering and the condition, and the resulting query plan can be hard to predict.
- **`INSTEAD OF` triggers on views subsume the historical use case.** Before PostgreSQL 9.1, rules were the only way to make a view updatable. Since 9.1, `INSTEAD OF` triggers do the same job with clearer semantics and per-row visibility.
- **Rules cannot easily raise exceptions or veto.** A trigger function can `RAISE EXCEPTION` to abort the statement; a rule can only rewrite it.

The one place rules remain canonical is `CREATE VIEW` itself — internally, `CREATE VIEW` creates a rule named `_RETURN` that rewrites `SELECT FROM view` into the view's defining query. Application code rarely writes this by hand.

> [!warning] A rule on a table is not "a cheaper trigger"
> Interviewers ask this as a trap. Rules and triggers are not interchangeable. A rule rewrites the SQL statement before execution; a trigger fires during execution, after the row is identified. A rule sees the parse tree, not the row values; a trigger sees `NEW`/`OLD`. A rule cannot raise an exception mid-statement; a trigger can. If the question is "do X for each row that matches Y", the answer is a trigger, full stop. If the question is "make this view updatable" or "rewrite this query shape", the answer is a view (or, rarely, a hand-written rule). See [[How would you explain CREATE TABLE syntax in SQL]] and [[How would you explain DDL DML and DCL in SQL]].

> [!warning] Triggers fire on the rewritten statement
> If a rule rewrites `INSERT INTO view` into `INSERT INTO table`, any `BEFORE INSERT` trigger on `table` fires — the trigger does not know (or care) that the original statement targeted a view. This is usually what you want, but it means a rule can cause a trigger to fire in ways the original SQL does not suggest. The reverse is also true: a trigger that itself issues `INSERT`/`UPDATE` on another table can fire that table's triggers, recursively (up to `session_replication_role` and the configured recursion limit). Recursive trigger bugs are real and notoriously hard to trace.

> [!tip] Interview answer
> A trigger is a function that runs on row or statement events and can modify `NEW`, run side-effect queries, or raise an exception. A rule is a query-rewrite mechanism that transforms the SQL parse tree before execution — `CREATE VIEW` compiles to a rule internally, and historical updatable-view code used `ON INSERT DO INSTEAD` rules. Since PostgreSQL 9.1, `INSTEAD OF` triggers on views subsume that use case with clearer per-row semantics. Use triggers for row-level behavior; use views (which compile to rules) for query composition; avoid hand-written rules on tables. Rules fire per statement and see the parse tree; triggers fire per row and see `NEW`/`OLD`. Related: [[How would you explain CREATE TABLE syntax in SQL]] and [[How do generated columns work in PostgreSQL]].
