<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is the difference between SQL DATETIME and TIMESTAMP?

> [!abstract] Short answer
> **DATETIME** (SQL Server, MySQL) stores a *naive* wall-clock value — no time zone. **TIMESTAMP** is overloaded: in PostgreSQL, `timestamptz` stores a UTC instant and renders per session zone (the recommended type); in MySQL, TIMESTAMP is UTC-stored zone-converted; in the SQL standard it is an unqualified or zone-qualified point in time. SQLite has neither — TEXT/REAL/INTEGER columns with date functions ([[What is the difference between SQL char and varchar types]]).

The storage-class question under the naming question: PostgreSQL's documented rule — `timestamp` keeps the literal wall-clock digits, `timestamptz` normalizes to UTC on write and converts on read per the session's timezone — is the semantics interviewers want, because "what happens when a user in Tokyo and a job in UTC read the same row" is a timestamptz story and a datetime bug story. SQL Server adds its own folklore: legacy `datetime` (accuracy 3.33 ms, range from 1753) versus `datetime2` (100 ns, from year 1) — the documented migration target is datetime2. The verified demo shows SQLite's model, which is instructive because it is *explicit*: the same instant stored twice — ISO-8601 TEXT and unix epoch INTEGER — with `datetime(ts, 'unixepoch')` reconstructing the string, and lexicographic string comparison serving range filters (`at >= '2024-01-01'`) precisely because ISO format sorts chronologically ([[What does NULL mean in SQL]]). The interview checklist: name one engine pair (PG timestamp vs timestamptz), state "store UTC, convert at the edge", and warn that `NOW()`-style defaults are session-zone-dependent — the classic replica-of-a-different-zone bug ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE ev (id INTEGER PRIMARY KEY, at TEXT, ts NUMERIC);
INSERT INTO ev VALUES (1, '2024-03-05T10:00:00Z', 1709632800);
SELECT at, ts, datetime(ts, 'unixepoch') FROM ev;
-- 2024-03-05T10:00:00Z|1709632800|2024-03-05 10:00:00
-- (same instant, two storage classes: ISO-8601 text and epoch seconds)
SELECT COUNT(*) FROM ev WHERE at >= '2024-01-01';
-- 1
-- (ISO text compares correctly by string order -- SQLite's "datetime" indexing trick)
```

**Listing 1.** Verified on SQLite 3.53.1. Two representations of one instant convert losslessly, and the ISO string's lexicographic order equals chronological order — the property text-timestamp range filters rely on.

```d2
direction: right
w1: "DATETIME
naive wall clock
no zone" {width: 180; height: 90}
w2: "TIMESTAMP (PG timestamptz)
UTC instant
renders per session" {width: 240; height: 90}
w3: "MySQL TIMESTAMP
UTC stored, zone-converted" {width: 230; height: 90}
s: "SQLite
TEXT / REAL / INTEGER + date funcs" {width: 260; height: 90}
```

**Fig. 1.** One concept — a point in time — with four storage contracts: naive digits, UTC instant with session rendering, zone-converting columns, or free-form values with date functions.

> [!warning] Mixing naive and aware timestamps is the silent off-by-timezone bug
> A `timestamp without time zone` column fed by clients in different zones is unparseable history; comparisons between naive and aware values pick an undocumented convention. The policy that survives review: one aware type (timestamptz or epoch), UTC everywhere in storage, zone conversion only at presentation ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> DATETIME is a naive wall-clock value with no zone; TIMESTAMP means different contracts per engine — PostgreSQL's timestamptz stores a UTC instant and renders per session zone (the type I use), MySQL's TIMESTAMP converts through UTC, and SQL Server's legacy datetime versus datetime2 differ in precision and range. SQLite has neither, storing ISO text or epoch numbers with date functions — my demo shows both round-tripping and ISO strings comparing correctly. The rule I follow: aware types, UTC in storage, convert at the edge.
