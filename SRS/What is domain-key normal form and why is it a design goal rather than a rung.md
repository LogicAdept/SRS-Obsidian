<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #SRS

# What is domain-key normal form and why is it a design goal rather than a rung

> [!abstract] Short answer
> **DKNF asks that every constraint a schema needs be a logical consequence of two kinds of rules alone: domain constraints (what values a column may take) and key constraints (which attribute sets are unique and referenced).** It is the strictest named form and the ceiling of the ladder — but a design direction rather than a rung: no engine certifies it, and generic business rules always leave a residue that domains and keys cannot express.

## Domains, keys, and the constraint classes left over

A domain constraint speaks about one attribute's legal values: type, `NOT NULL`, `CHECK`, enum, range. A key constraint speaks about uniqueness and reference: `PRIMARY KEY`, `UNIQUE`, foreign keys. Everything else a business states falls into three leftover classes. First, single-row conditions spanning several columns (`valid_from < valid_to`) — expressible as a `CHECK`, and by the generous reading still domain-shaped. Second, conditional uniqueness — "at most one active subscription per customer": a plain `UNIQUE (customer, status)` is too coarse (it would also forbid two cancelled rows), but a partial unique index reshapes the rule into genuine key-constraint territory. Third, cross-row and aggregate rules — "shares sum to 100", "department salary total stays under budget" — fundamentally outside both kinds: no key expresses them and no row-level `CHECK` can see other rows.

```sql
CREATE TABLE subscriptions (id INTEGER PRIMARY KEY, customer INT, status TEXT NOT NULL);
CREATE UNIQUE INDEX one_active
  ON subscriptions (customer) WHERE status = 'active';

INSERT INTO subscriptions VALUES (1, 7, 'active');
INSERT INTO subscriptions VALUES (2, 7, 'active');   -- rejected
INSERT INTO subscriptions VALUES (3, 7, 'cancelled');
INSERT INTO subscriptions VALUES (4, 7, 'cancelled'); -- fine
```

**Listing 1.** Conditional uniqueness as a key constraint: a partial unique index. Verified on SQLite 3.53.1: the second active row for customer 7 was rejected with `UNIQUE constraint failed: subscriptions.customer`, while the two cancelled rows coexisted.

```sql
CREATE TABLE shares (id INTEGER PRIMARY KEY, pct INT CHECK (pct > 0));
INSERT INTO shares VALUES (1, 60);
INSERT INTO shares VALUES (2, 50);                    -- sum 110, CHECK happy

CREATE TRIGGER sum_guard AFTER INSERT ON shares
WHEN (SELECT SUM(pct) FROM shares) > 100
BEGIN SELECT RAISE(ROLLBACK, 'shares exceed 100'); END;
INSERT INTO shares VALUES (3, 50);                    -- rejected by trigger
```

**Listing 2.** The aggregate class: row-level `CHECK` cannot see other rows (measured: 60 + 50 = 110 accepted), so the cross-row rule needs a trigger — verified on SQLite 3.53.1: the third insert rolled back with `shares exceed 100` and the sum stayed 110.

## Why it sits above the ladder — and above the engines

Each rung from 1NF to 6NF removes one redundancy class and is phrased in dependencies; DKNF is not one more decomposition step but a statement about the whole constraint set: a redundancy-free schema whose every remaining rule lives in a domain or a key — a fully self-enforcing design. The practical approximation is unglamorous and effective: typed columns and `CHECK`/enum as domains, primary and foreign keys plus partial (in PostgreSQL, exclusion) indexes as keys, and an honest list of what remains — the trigger-shaped residue of Listing 2 is exactly the boundary where "the database checks it for me" ends and application-transaction or scheduled-reconciliation logic begins, the same boundary that motivates [[What is database denormalization for]] with a refresh story. In interview terms, DKNF is where the ladder terminates: name it as the design ideal, show you know which rules modern engines can absorb and which they cannot.

> [!warning] Two popular misreadings
> "DKNF means sprinkling more CHECKs" — no: a single-row CHECK is only the generous first class; the measured fact of Listing 2 is that aggregate rules cannot be CHECKs at all, and pretending otherwise leaves them silently unenforced. "DKNF is always the better design" — also no: it constrains where rules live, not how the system performs; pushing every invariant into triggers moves application logic into the database, with its own latency, debugging, and migration costs. The honest target is maximal domains-and-keys coverage with an explicit, owned residue — not zero residue by any means necessary.

The rung below: [[What is sixth normal form and where does per-attribute decomposition pay off]]; the machinery the forms are stated in: [[What is a functional dependency in relational databases]]; what happens without the discipline: [[What can violating database normalization lead to]]; uniqueness mechanics behind the key half: [[What is the difference between PRIMARY KEY and UNIQUE]].

> [!tip] Interview answer
> DKNF: every constraint follows from domain constraints and key constraints alone. The ladder 1NF→6NF removes redundancy class by class; DKNF is the ceiling — a self-enforcing schema, not an engine feature (nothing certifies it). Working classification of constraints: single-row CHECKs ≈ domains; conditional uniqueness → partial/exclusion indexes = keys (measured: the second active subscription rejected, cancelled ones coexisting); aggregate rules are the residue — CHECKs cannot see other rows (60 + 50 = 110 accepted), triggers or application transactions must own them. Name it as the design direction: maximize domains-and-keys coverage, keep the trigger-shaped residue explicit and owned.
