<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #SRS

# What is Boyce-Codd normal form and how does it differ from 3NF

> [!abstract] Short answer
> **BCNF is 3NF with one rule added: every determinant must be a candidate key.** 3NF tolerates one exception — a column that determines a *prime* attribute (part of some key) without being a key itself; BCNF forbids that too, and the price of the fix can be a dependency you can no longer enforce locally.

## The case 3NF lets through

Take enrollments: R(student, subject, teacher) with two rules — a teacher teaches exactly one subject (teacher → subject), and one teacher per enrollment (student, subject → teacher). The candidate keys are (student, subject) and (student, teacher). Both non-key columns are prime: subject is part of the first key, teacher of the second — so 3NF holds. But teacher is a **determinant that is not a key**: it fixes subject while sitting in the middle of the table. That is exactly the 3NF definition's escape hatch (for every non-trivial dependency X → A, either X is a superkey *or* A is prime) that BCNF closes by dropping the "or A is prime" branch.

The redundancy is real and measurable: the fact "ProfA teaches Math" is stored once per enrolled student — 2 rows here — and re-assigning the subject of one teacher touched 2 rows in the verification run, each free to disagree if one UPDATE misses.

```sql
-- 3NF holds (all non-key columns are prime), BCNF does not:
-- teacher determines subject but is not a candidate key
CREATE TABLE enroll_3nf (
  student TEXT, subject TEXT, teacher TEXT,
  PRIMARY KEY (student, subject)
);
```

**Listing 1.** The 3NF table. Verified on SQLite 3.53.1: the fact "ProfA teaches Math" repeats on every enrollment row of ProfA, and one re-assignment UPDATE touched 2 rows.

```d2
direction: right
r: "R(student, subject, teacher)\nteacher -> subject\nkeys: (student, subject), (student, teacher)" {
  width: 340
  height: 110
  style.fill: "#ffebee"
}
r1: "enrollment(student, teacher)\nPK (student, teacher)" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
r2: "teaches(teacher, subject)\nPK teacher" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
r -> r1
r -> r2
```

**Fig. 1.** The BCNF decomposition: the non-key determinant gets its own table where it finally is the key. The join of the two projections reproduces the original rows exactly — lossless for data.

## What the decomposition costs

Splitting into enrollment(student, teacher) and teaches(teacher, subject) removes the redundancy: subject lives once per teacher, and the join reconstructs the original 3 rows exactly. The measured trap is what happens to the other dependency. In the 3NF table, "one teacher per enrollment" was enforced locally — re-inserting a second teacher for the same (student, subject) was rejected with `UNIQUE constraint failed`. After the split, that dependency spans two tables: nothing in either table can express it. The verification run inserted a second Math teacher for the same student into the split schema — **both inserts were accepted**, and the join now returns 2 rows for one factually single enrollment. Enforcing the original rule needs a trigger, a materialized check, or application logic.

| | stay at 3NF | decompose to BCNF |
|---|---|---|
| Non-key determinant | allowed, redundancy stays | gone — every determinant is a key |
| The crossing dependency | enforced locally by the PK | not expressible as key/FK in either table |
| Write safety | one fact per N rows, can drift | clean, but the other rule is now app-side |
| Typical choice | when the crossing rule matters | when the determinant's redundancy hurts |

> [!warning] BCNF decomposition is lossless for data but can be lossy for constraints
> The popular lie is "BCNF is strictly better, always decompose". The decomposition of a 3NF table may be unable to preserve every dependency — the run above lost (student, subject) → teacher entirely. Which BCNF projection you pick also matters: different split orders can preserve different dependency sets, so "we are in BCNF" is not a certificate that every business rule is still checkable by the schema.

The dependency-preservation idea also explains why 3NF is the usual target: 3NF is the strongest form that **always** admits a dependency-preserving lossless decomposition. Beyond it, you trade local enforceability for zero non-key determinants — a trade to argue, not a default.

Where 3NF stops and this begins: [[How would you explain third normal form in relational databases]]; keys and determinants: [[How would you explain candidate keys in relational databases]]; the cost of skipping the ladder: [[What can violating database normalization lead to]]; the next rung: [[What is fourth normal form and what are multivalued dependencies]].

> [!tip] Interview answer
> BCNF is 3NF plus "every determinant is a candidate key". The gap case: enrollment(student, subject, teacher) where teacher → subject but the keys are (student, subject) and (student, teacher) — 3NF passes because subject is prime, BCNF fails. Decomposing removes the repeated subject fact but can strand a dependency across tables — the one-teacher-per-enrollment PK rule became unenforceable. So: 3NF always keeps a dependency-preserving decomposition; BCNF may not. Choose per constraint, not by reflex.
