<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How would you explain SQL injection attacks and defenses?

> [!abstract] Short answer
> **SQL injection** is the failure of building SQL by string concatenation with untrusted input: the input's quote characters terminate a literal and inject SQL *structure* (`x' OR '1'='1'` makes the WHERE always true). The defense is **parameterized queries** (PreparedStatement, `?`/`:name` binding): SQL structure and data travel separately, so input can never change the statement's shape. Secondary layers: least-privilege accounts, input validation, escaping as a last resort — the OWASP SQL Injection Prevention Cheat Sheet orders exactly these ([[What does the SQL MERGE statement do]]).

The verified demo executes the canonical break: the concatenated predicate `login = 'x' OR '1'='1'` evaluates as `(login = 'x') OR ('1' = '1')` — the injected `'1'='1'` is a *true literal inside SQL structure*, the OR short-circuits the filter, and the query returns every row including secrets. The same input passed as a bound parameter searches for the literal string `x' OR '1'='1` and returns zero rows — because the driver sends the statement template and the value separately; the value is quoted once as data by the engine, and no part of it re-enters the parse tree. The JDBC PreparedStatement javadoc states the contract precisely: the statement is precompiled, parameters are sent with the execution, and "the object used for executing a prepared statement... cannot change the SQL statement" — that sentence is the whole defense. The OWASP cheat sheet's layered list completes the senior answer: prepared statements everywhere (primary), stored-procedure/allow-listing for the dynamic-SQL corners (ORDER BY columns cannot be parameters — validate against an allow-list), least-privilege DB accounts, and defense-in-depth monitoring ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE app_users (login TEXT, secret TEXT);
INSERT INTO app_users VALUES ('admin','s3cret'),('bob','bobspw');

-- input: x' OR '1'='1   -- concatenated into the string:
SELECT login, secret FROM app_users WHERE login = 'x' OR '1'='1';
-- admin|s3cret
-- bob|bobspw
-- (the injected OR '1'='1' is always-true SQL structure: all rows leak)
SELECT login, secret FROM app_users WHERE login = 'x'' OR ''1''=''1';
-- (0 rows: with binding the payload is one literal VALUE, not structure)
```

**Listing 1.** Verified on SQLite 3.53.1. Identical bytes, opposite outcomes: concatenated input rewrites the predicate and leaks both rows; the bound-parameter form searches for the literal payload and matches nothing.

```d2
direction: right
in: "untrusted input" {width: 150; height: 60}
c: "concatenation
input -> SQL structure" {width: 210; height: 80}
p: "parameter binding
input stays a value" {width: 200; height: 80}
x: "statement reinterpreted
injection" {width: 180; height: 70}
o: "statement unchanged
safe" {width: 150; height: 60}
in -> c -> x
in -> p -> o
```

**Fig. 1.** One input, two destinations: into the SQL *text* it becomes structure and can reinterpret the statement; into a *bind slot* it remains data the parser never sees.

> [!warning] Parameters bind VALUES only — the dynamic parts that remain must be allow-listed
> Table names, column names and ORDER BY directions cannot be bound; frameworks interpolate them. The OWASP-mandated pattern is mapping user choices through a server-side allow-list (`sort = ALLOWED.get(requestSort)`), never trusting the raw string — and least-privilege accounts to cap the blast radius if a hole ships anyway ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> SQL injection is input becoming SQL structure: my demo shows `x' OR '1'='1'` concatenated into a WHERE turning it always-true and leaking all rows, while the same payload bound as a parameter is just a literal that matches nothing — because PreparedStatement sends the template and values separately, and parameters cannot change the statement, which the JDBC javadoc states explicitly. My layers: parameterized queries everywhere; allow-lists for the unbindable parts like ORDER BY columns; least-privilege database accounts; and input validation as hygiene, never as the primary defense.
