<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> SQL (Structured Query Language) is the standard language for defining, querying, and manipulating data in a relational database. It is **declarative**: you state *what* rows you want, and the database engine decides *how* to produce them. Statements fall into named groups — DDL (schema: `CREATE`, `ALTER`, `DROP`), DML (data: `SELECT`, `INSERT`, `UPDATE`, `DELETE`), DCL (rights: `GRANT`, `REVOKE`), and TCL (transactions: `COMMIT`, `ROLLBACK`, `SAVEPOINT`).

SQL was standardized by ANSI/ISO (the ISO/IEC 9075 family) and every mainstream engine — PostgreSQL, MySQL, Oracle Database, SQL Server, SQLite — implements that core with its own dialect extensions. Oracle's own introduction puts it plainly: SQL is the set of statements with which all programs and users access data in the database; tools may hide it, but underneath every request still runs as SQL.

Two properties define the working style. First, operations are **set-at-a-time**: one `UPDATE ... WHERE` line changes every matching row, with no loop you write yourself. Second, the engine has freedom in execution: the statement is parsed, bound against the catalog, optimized into a query plan, and only then executed — the plan can change as data and statistics change. Your contract is the declared result, not a fixed algorithm ([[What is the logical order of SQL SELECT execution]], [[What is a query plan in a relational database]]).

Declarative does not mean "costless": a poorly shaped query still produces a slow plan, so performance work means giving the optimizer good structures (indexes, statistics, sargable predicates) rather than hand-coding loops ([[What is sargability in SQL]], [[How would you explain common ways to optimize SQL queries]]).

```sql
-- One script, all four statement groups (SQLite):
CREATE TABLE dept (id INTEGER PRIMARY KEY, name TEXT NOT NULL);      -- DDL
CREATE TABLE emp  (id INTEGER PRIMARY KEY, name TEXT NOT NULL,
                   dept_id INTEGER REFERENCES dept(id), salary NUMERIC);
INSERT INTO dept VALUES (1,'Core'),(2,'Web');                        -- DML
INSERT INTO emp VALUES (10,'Ada',1,1200),(11,'Bo',2,900),(12,'Cy',1,1000);
SELECT d.name AS department, COUNT(*) AS people,
       ROUND(AVG(e.salary),1) AS avg_salary                          -- DML: query
FROM dept d JOIN emp e ON e.dept_id = d.id
GROUP BY d.name ORDER BY avg_salary DESC;
-- Core|2|1100.0
-- Web|1|900.0
```

**Listing 1.** Verified on SQLite 3.53.1: DDL creates the schema, DML fills and reads it, and the `SELECT` shows the set-at-a-time style — one aggregate query, no loops. `GRANT`/`REVOKE` (DCL) and `COMMIT`/`ROLLBACK` (TCL) complete the four groups in engines that support them.

```d2
direction: right
sql_text: "SQL text\n declarative" {width: 170; height: 90}
parser: "parse\nbind to catalog" {width: 170; height: 90}
planner: "plan\noptimizer chooses access paths" {width: 210; height: 90}
exec: "execute\nrows returned" {width: 160; height: 90}
sql_text -> parser -> planner -> exec
```

**Fig. 1.** The engine, not the programmer, walks this pipeline — the same statement text can yield different plans as statistics and indexes change.

> [!warning] "Standard SQL" is a moving target, and dialects differ in the edges
> The ISO core is portable, but everyday details are not: row limiting is `LIMIT` in PostgreSQL/SQLite/MySQL, `TOP` in T-SQL, `FETCH FIRST n ROWS ONLY` in the standard and Oracle 12c+; identifier quoting differs (`"x"`, `` `x` ``, `[x]`); date functions diverge wildly. Code that "works in SQL" usually means "works in the engine I tested".

> [!tip] Interview answer
> SQL is the ISO-standardized, declarative language for relational databases: DDL defines the schema, DML reads and changes data, DCL manages rights, TCL manages transactions. You describe the desired result set-at-a-time, and the engine parses, plans, and executes it — so performance comes from good structures and sargable predicates, not manual iteration. Dialects share the core but differ in syntax like `LIMIT` vs `TOP` vs `FETCH FIRST`.
