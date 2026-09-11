<!--
reps: 0
priority: 0
-->
#Databases/Relational/PostgreSQL #Databases/SQL/DataTypes #SRS

# What is the difference between CHAR, VARCHAR and TEXT in PostgreSQL?

> [!abstract] Short answer
> Performance is identical; the differences are semantics. `char(n)` is blank-padded to exactly n characters and trailing spaces compare as insignificant; `varchar(n)` is variable length with a hard maximum; `text` is unlimited with no length check. PostgreSQL treats varchar without a length as text, and internally varchar is essentially a domain over text — there is no storage or speed penalty for text.

## The three semantics

| Type | Storage | Length behavior |
|---|---|---|
| char(n) | padded to n | trailing spaces insignificant in comparisons |
| varchar(n) | actual + header | error on overflow |
| text | actual + header | unlimited (up to ~1 GB with TOAST) |

`char(n)` pads values with spaces on store; comparisons and many operations ignore the padding, which is a rich source of subtle bugs. Omitting the length (`char`) means char(1). Omitting it on varchar makes it behave exactly like text. See [[What is TOAST in PostgreSQL]] for how long values are stored out of line.

```sql
SELECT 'ab'::char(4) = 'ab      '::char(8);   -- true: padding ignored
SELECT 'ab '::varchar(4) = 'ab'::varchar(4); -- false: trailing space matters
CREATE TABLE emails (addr text);             -- idiomatic PostgreSQL
```

**Listing 1.** The padding trap in two lines plus the idiomatic choice.

```d2
pad: "char(n)\nblank-padded, comparisons\nignore trailing spaces" {width: 320; height: 90}
var: "varchar(n)\nexact value, max-length\ncheck on input" {width: 300; height: 90}
txt: "text\nexact value, no limit\nnative string type" {width: 300; height: 90}
```

**Fig. 1.** Same engine underneath — the choice is a contract about padding and limits, not about speed.

## Which to use

PostgreSQL documentation and community practice: `text` by default, and enforce real constraints with CHECK or domains when needed:

```sql
CREATE TABLE users (name text CHECK (char_length(name) <= 100));
```

**Listing 2.** A length limit as a constraint can be altered without a table rewrite; changing a `varchar(n)` limit is an ALTER TYPE. Functionally `varchar` acts like a domain over text ([[What are IMMUTABLE STABLE and VOLATILE functions in PostgreSQL]] is unrelated here — but the char-padding interactions with pattern matching are real: LIKE keeps trailing spaces significant even on char columns).

> [!warning] char(n) does not make anything faster
> The classic myth from other engines — fixed-length rows are faster — is false in PostgreSQL: all three types go through the same varlena storage, and char(n) adds padding work plus comparison quirks. The only honest uses of char(n) are interop with systems expecting it or single-character codes; even then text with a CHECK is cleaner.

> [!tip] Interview answer
> In PostgreSQL the three have identical performance and storage mechanics: char(n) is blank-padded with trailing-space-insensitive comparison, varchar(n) is variable with a max-length check, text is unlimited. Idiomatic PostgreSQL is text plus CHECK constraints or domains — and never char(n) for speed, the padding only buys bugs.
