<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# What is the difference between SQL char and varchar types?

> [!abstract] Short answer
> **CHAR(n)** is fixed-length: values are space-padded to n on storage (PostgreSQL `bpchar`) and the padding is ignored in most comparisons. **VARCHAR(n)** is variable-length with an optional maximum; the industry default for text. SQLite implements both as the same TEXT storage class — no padding, no truncation — making the distinction purely a *declared* behavior elsewhere ([[What does NULL mean in SQL]]).

The verified demo shows SQLite's reality: both `CHAR(5)` and `VARCHAR(5)` columns store `'ab'` as a 2-character TEXT (`typeof` = text, `length` = 2), and the trailing space survives in comparisons — `'ab ' = 'ab'` is false, unlike padded CHAR semantics on PostgreSQL or SQL Server where `'ab' = 'ab   '` (CHAR comparison ignores trailing blanks). PostgreSQL's documentation defines the real CHAR behavior: values right-padded to the declared length, trailing spaces semantically invisible in comparisons but present in storage (`char_length` counts them until cast) — which is exactly why VARCHAR dominates modern schemas: padding wastes bytes and the blank-insensitive comparisons surprise. The length attribute differs too: PostgreSQL *enforces* varchar(n) (insert longer fails; `varchar` without n is unconstrained), SQL Server similarly, and the varchar limit is per *characters* in modern engines, not bytes — the bytes question is UTF-8 storage length, which is where interviewers steer next ([[For which SQL numeric types are addition and subtraction invalid]]). SQLite's type affinity completes the picture: CHAR and VARCHAR both map to TEXT affinity, the (n) is ignored, and enforcement is an application job ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE ch (c CHAR(5), v VARCHAR(5));
INSERT INTO ch VALUES ('ab', 'ab');
SELECT c, length(c), typeof(c), v, length(v), typeof(v) FROM ch;
-- ab|2|text|ab|2|text
SELECT c = 'ab', c = 'ab ' FROM ch;
-- 1|0
-- (SQLite: no padding, no blank-blind comparison -- a space is a real character.
--  PostgreSQL CHAR(5) would pad 'ab' to 'ab   ' and compare equal to 'ab'.)
```

**Listing 1.** Verified on SQLite 3.53.1. Both declared types behave identically as TEXT, and `'ab '` differs from `'ab'` — the opposite of padded-CHAR comparison semantics documented for PostgreSQL and SQL Server.

```d2
direction: right
c1: "CHAR(5)
'ab' -> 'ab   '
padded, blank-blind compare" {width: 240; height: 90}
c2: "VARCHAR(5)
'ab' -> 'ab'
variable, length-checked" {width: 220; height: 90}
c3: "SQLite
columns -> TEXT affinity
(n) ignored" {width: 210; height: 90}
c1 -> c3
c2 -> c3
```

**Fig. 1.** The declared types diverge where storage is typed — padding versus variable length — and converge in SQLite, where both collapse to one TEXT storage class.

> [!warning] CHAR's blank-blind comparisons leak into joins and keys
> `WHERE char_col = 'ab'` matching 'ab   ' is convenient until two "different" values join, group together, or compare unequal only after casts (`trim` needed). Choose CHAR only for genuinely fixed-width codes (ISO country codes) and store those without padding surprises ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> CHAR is fixed-length and space-padded — PostgreSQL pads and ignores trailing blanks in comparisons — while VARCHAR is variable with an enforced maximum in PG and SQL Server; the declared limit counts characters, not UTF-8 bytes. My demo shows SQLite flattening both to TEXT affinity with no padding, where 'ab ' genuinely differs from 'ab'. Default choice is VARCHAR; CHAR only for true fixed-width codes, knowing its blank-blind comparisons can surprise joins and keys.
