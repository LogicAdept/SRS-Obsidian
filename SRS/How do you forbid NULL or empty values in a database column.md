<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

> [!abstract] Short answer
> Two constraints layered: `NOT NULL` forbids the missing value; a `CHECK` forbids the empty *content* — `CHECK (col <> '')` for strings, `CHECK (length(trim(col)) > 0)` when whitespace-only must also fail. Either alone is half a guarantee: NOT NULL still allows `''`, and an empty-check alone still allows NULL ([[What integrity constraints exist in SQL]]).

The verified demo walks the whole grid: NULL rejected by NOT NULL (`NOT NULL constraint failed`), `''` and `'  '` rejected by the CHECK (`CHECK constraint failed: length(trim(nick)) > 0`), and the honest value inserted. Why the layering matters is the conflation bug every production schema eventually meets: empty string and NULL are *different* answers ("nickname deliberately blank" versus "nickname unknown") and ORMs, HTML forms and CSV loaders happily produce `''` where the model means NULL — with only NOT NULL on the column, the empty string sneaks through and quietly splits your grouping keys, your UNIQUE pool and your report denominators ([[What does NULL mean in SQL]]). The alternative design stance is equally defensible and worth naming: normalize on the boundary — translate empty inputs to NULL in the application/loading layer — and keep only NOT NULL in the schema; the CHECK is the defense that works when you cannot trust every writer. PostgreSQL accepts the same CHECK predicates; SQL Server's `CHECK (col <> '')` equivalent treats NULL as UNKNOWN and passes it — which is precisely why NOT NULL must carry that half ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE users2 (id INTEGER PRIMARY KEY,
  nick TEXT NOT NULL CHECK (length(trim(nick)) > 0));

INSERT INTO users2 VALUES (1, 'al');
-- (ok)
INSERT INTO users2 VALUES (2, NULL);
-- ERROR: NOT NULL constraint failed: users2.nick
INSERT INTO users2 VALUES (2, '');
-- ERROR: CHECK constraint failed: length(trim(nick)) > 0
INSERT INTO users2 VALUES (2, '   ');
-- ERROR: CHECK constraint failed: length(trim(nick)) > 0
```

**Listing 1.** Verified on SQLite 3.53.1. Three rejected writes with the *right* error each time — missing value caught by NOT NULL, empty and whitespace-only caught by the trimmed-length CHECK.

```d2
direction: right
v1: "NULL
missing value" {width: 160; height: 70}
v2: "'' / '  '
empty content" {width: 170; height: 70}
v3: "real value" {width: 130; height: 70}
nn: "NOT NULL
rejects NULL" {width: 150; height: 70}
ck: "CHECK
rejects empty/blank" {width: 180; height: 70}
ok: "accepted" {width: 110; height: 60}
v1 -> nn
v2 -> ck
v3 -> ok
nn -> ok
ck -> ok
```

**Fig. 1.** Two different failure modes pass through two different gates: absence is NOT NULL's jurisdiction, emptiness is the CHECK's.

> [!warning] CHECK sees NULL as UNKNOWN and lets it pass — by design
> `CHECK (col <> '')` on a nullable column does not reject NULL, because NULL compared to anything is UNKNOWN and CHECK requires only "not false". The pair (NOT NULL + CHECK) is therefore not redundant but complementary; dropping either half reopens its hole ([[What is the difference between PRIMARY KEY and UNIQUE]]).

> [!tip] Interview answer
> I layer both: NOT NULL for absence, and a CHECK for emptiness — CHECK (col <> '') at minimum, CHECK (length(trim(col)) > 0) when whitespace-only should fail too. Either alone is bypassable: NOT NULL still admits empty strings, and CHECK alone passes NULL because NULL evaluates to UNKNOWN, which satisfies a CHECK. I also mention the alternative policy of normalizing empty inputs to NULL in the application layer — the constraints are what stands when a loader bypasses that layer.
