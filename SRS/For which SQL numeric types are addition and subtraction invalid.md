<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# For which SQL numeric types are addition and subtraction invalid?

> [!abstract] Short answer
> The numeric-ish type where `+` and `-` are invalid is **BIT** — in both major spellings. T-SQL's `bit` (its boolean) is documented as excluded from the `+`/`-` operators ("Operand data type bit is invalid for add operator"); PostgreSQL's `bit` is a *bit string* type with no arithmetic operators at all (`B'101' + B'010'` errors). SQLite has no BIT type — flags are INTEGER 0/1 and arithmetic is valid, which makes the contrast the demo ([[What are the main SQL aggregate functions]]).

Why the exclusion exists clarifies the answer. T-SQL's `bit` is a logical type (TRUE/FALSE/NULL storage in one bit per row pack) — arithmetic on truth values is meaningless by design, so the documented operator table for `+` lists numeric categories *except* bit; the canonical workaround is explicit conversion (`CAST(bit_col AS int)`). PostgreSQL's `bit VARYING`/`bit(n)` is a bit-string (binary digits as data), and its operator catalog offers concatenation (`B'101' || B'010'`) and bitwise functions, not numeric addition — the documented error for `+` is "operator does not exist: bit + bit", with the hint that no cast path exists. The verified demo demonstrates the *other* half: SQLite booleans are plain INTEGERs, `is_admin + 1` computes 2 and 1 — legal arithmetic over a boolean-ish column, with the trailing implication that SQLite flags support both `is_admin + 1` arithmetic and `is_admin = 1` logic, while T-SQL forces the CAST and PostgreSQL forces bit-string operations. The practical reading: "boolean as number" is a type-system decision each engine makes, and hot paths that do arithmetic on flags need to know which regime they are in ([[What harmful SQL patterns or pitfalls do you know]]).

```sql
CREATE TABLE flags (id INTEGER PRIMARY KEY, is_admin INTEGER);
INSERT INTO flags VALUES (1, 1), (2, 0);
SELECT id, is_admin + 1 AS plus FROM flags ORDER BY id;
-- 1|2
-- 2|1
-- (SQLite: no BIT type; booleans are INTEGER 0/1, so arithmetic is valid.
--  T-SQL: bit + int -> ERROR "Operand data type bit is invalid for add operator"
--  PostgreSQL: B'101' + B'010' -> ERROR "operator does not exist: bit + bit")
```

**Listing 1.** Verified on SQLite 3.53.1 for the runnable half: flag arithmetic succeeds where a real BIT type exists elsewhere. The two error behaviors are the documented operator rules of T-SQL and PostgreSQL, quoted by their messages.

```d2
direction: right
b1: "T-SQL bit
logical type
no + / - (cast to int first)" {width: 230; height: 90}
b2: "PG bit
bit string
no + (concat || instead)" {width: 210; height: 90}
b3: "SQLite
no bit: INTEGER 0/1
arithmetic valid" {width: 200; height: 90}
q: "can you add two flags?" {width: 200; height: 70}
b1 -> q
b2 -> q
b3 -> q
```

**Fig. 1.** Three engines, three answers to one innocent expression: forbidden by the operator table, forbidden by the type system, or simply valid because no BIT type exists.

> [!warning] The error message names the escape hatch — and the design smell
> CAST to int before arithmetic works, but arithmetic over boolean flags in a query usually means the *model* wants an integer counter or a real status enum instead of a bit carrying numeric meaning. Fixing the type beats fixing the expression ([[What harmful SQL patterns or pitfalls do you know]]).

> [!tip] Interview answer
> It is the BIT type: T-SQL's bit is excluded from addition and subtraction by its documented operator table — the error is literally "operand data type bit is invalid for add operator" — and PostgreSQL's bit is a bit string with no arithmetic operators at all. SQLite has no BIT, so booleans are INTEGER 0/1 and arithmetic just works, which my demo shows. The deeper point: boolean-as-number is a type-system choice per engine, and needing arithmetic on flags usually means the column wants to be an integer counter in the first place.
