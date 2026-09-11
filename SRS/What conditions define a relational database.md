<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What conditions define a relational database?

> [!abstract] Short answer
> A relational database is a database that **conforms to the relational model**: data lives in *relations* (tables) — unordered sets of *tuples* (rows), each with the same set of named *attributes* (columns) drawn from declared domains (types) — and the model provides three things: well-defined **structures**, clearly defined **operations** that manipulate them, and **integrity rules** that constrain what the data may say. SQL is the standard language on top of that model, not the model itself.

The definition comes from E. F. Codd's 1970 paper *"A Relational Model of Data for Large Shared Data Banks"*, which built the model on set theory; Oracle's official concepts guide summarizes the same three aspects (structures, operations, integrity rules) and states directly: a relational database is one that stores data in relations (tables). Working with the set-theoretic core explains SQL's flavor — a query result is itself a set, joins are set operations, and a table has **no built-in row order** ([[What is the logical order of SQL SELECT execution]]).

What follows from the definition, condition by condition:

- **Tables (relations), rows (tuples), columns (attributes).** Every row of a table has the same column set; a column holds values from one declared type (its domain).
- **No duplicate rows.** A relation is a *set* of tuples, which is why a table needs a primary key to address rows uniquely, and why `UNION`/`DISTINCT` eliminate duplicates ([[What is the difference between SQL UNION and UNION ALL]], [[What is the difference between PRIMARY KEY and UNIQUE]]).
- **No meaningful row order.** Without `ORDER BY` the engine returns rows in whatever order is fastest.
- **Operations over sets.** Selection (rows), projection (columns), and joins combine relations; results are again relations.
- **Integrity rules.** Keys (entity integrity: no part of a primary key is `NULL`), foreign keys (referential integrity), and domain constraints ([[What integrity constraints exist in SQL]]).

```sql
-- The relational core: relations over domains, addressed by keys, combined by set operations.
CREATE TABLE dept (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE emp  (id INTEGER PRIMARY KEY, name TEXT NOT NULL,
                   dept_id INTEGER REFERENCES dept(id));   -- referential integrity
INSERT INTO dept VALUES (1,'Core'),(2,'Web');
INSERT INTO emp VALUES (10,'Ada',1),(11,'Bo',2),(12,'Cy',1);

SELECT d.name AS department, e.name AS employee   -- projection
FROM emp e JOIN dept d ON d.id = e.dept_id        -- set operation (join)
ORDER BY department, employee;
-- Core|Ada
-- Core|Cy
-- Web|Bo
```

**Listing 1.** Verified on SQLite 3.53.1: two relations with declared domains and keys, a foreign key for referential integrity, and a join whose result is again a relation (rows/columns), which the query then projects and orders.

```d2
direction: right
model: "Relational model\nCodd, 1970" {width: 190; height: 90}
structures: "Structures\nrelations: rows x columns" {width: 210; height: 90}
ops: "Operations\nselect, project, join" {width: 200; height: 90}
rules: "Integrity rules\nkeys, foreign keys, domains" {width: 220; height: 90}
model -> structures
model -> ops
model -> rules
```

**Fig. 1.** Three aspects of the model in one picture: what the data looks like, what you can do to it, and what may never be violated.

> [!warning] "SQL database" and "relational database" are not synonyms
> A SQL engine may expose non-relational extras (JSON columns, arrays, text search), and a product can be "relational" in marketing while allowing duplicate unkeyed rows in practice (MySQL with older engines). The definition bites at review time: if a table has no key, duplicate rows are storable and the set semantics silently break — that is a model violation, not a quirk.

> [!tip] Interview answer
> A relational database is one that conforms to Codd's relational model: data is stored in relations — sets of tuples with fixed attributes over declared domains — with no duplicate rows and no inherent order. The model gives you structures, set-based operations like select/project/join, and integrity rules such as keys and foreign keys. SQL is the standard language over that model, and features like primary keys, `DISTINCT`, and `ORDER BY` only make sense once you take the set semantics seriously.
