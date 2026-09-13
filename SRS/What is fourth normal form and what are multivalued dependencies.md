<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #SRS

# What is fourth normal form and what are multivalued dependencies

> [!abstract] Short answer
> **4NF is BCNF plus: no multivalued dependency except those the key implies.** A multivalued dependency (MVD) means one key value fixes a whole *set* of values of another attribute. Two **independent** such sets forced into one table multiply into an M×N row cross product — that table is not in 4NF, and the fix is one table per set.

## The mechanism of the cross-product blowup

A course table holds which tutors certify it and which skills it requires — and the two lists vary independently: tutors are hired without touching the syllabus, skills are added without touching staffing. In one table course(course, tutor, skill) each tutor row is repeated for every skill and each skill for every tutor; the table encodes the **cross product** of the two lists. Formally that is two MVDs, course →→ tutor and course →→ skill, holding at once with no dependency between them — the definition of a 4NF violation (non-trivial MVDs whose determinant is not the key; BCNF-level FD problems are assumed already gone).

```sql
-- not in 4NF: two independent sets in one table
CREATE TABLE course_req_bad (course TEXT, tutor TEXT, skill TEXT);
-- 4NF: one table per independent set
CREATE TABLE course_tutor (course TEXT, tutor TEXT,
  PRIMARY KEY (course, tutor));
CREATE TABLE course_skill (course TEXT, skill TEXT,
  PRIMARY KEY (course, skill));
```

**Listing 1.** The shape of the violation and the repair. Verified on SQLite 3.53.1 with 3 tutors and 2 skills: the bad table holds 6 rows — the pair (SQL, T1) alone is stored 2 times.

```d2
direction: down
bad: "course(course, tutor, skill)\nM x N rows\neach pair of facts repeated" {
  width: 300
  height: 100
  style.fill: "#ffebee"
}
t: "course_tutor\ncourse ->-> tutor\nN rows" {
  width: 200
  height: 90
  style.fill: "#e3f2fd"
}
s: "course_skill\ncourse ->-> skill\nM rows" {
  width: 200
  height: 90
  style.fill: "#e8f5e9"
}
bad -> t
bad -> s
```

**Fig. 1.** The split trades one M×N table for two 1-dimension tables; their join restores the cross product on demand, losslessly.

## The measured cost of the single table

With 3 tutors and 2 skills: adding **one** skill inserted 3 rows into the bad table (one per existing tutor); removing **one** tutor deleted 3 rows (one per existing skill). Every write pays the multiplier, and each copy is free to drift. In the 4NF split the same add is 1 row in course_skill and the same removal 1 row in course_tutor; 3 + 2 = 5 rows store the same 5 facts the bad table encoded in 6. Joining the two split tables back on course returns exactly the original 6 combinations — lossless, which is what makes the split safe.

> [!warning] Splitting is correct only because the lists are independent
> If tutor and skill were **correlated** — T1 may certify joins but not query plans — the join of the two split tables would fabricate combinations nobody asserted (T1 with query plans). Independence is the test: does every combination of the two lists make sense? If not, the association between the lists is a real fact that needs its own columns or table, and the 4NF decomposition would silently destroy it. This is also why 4NF sits above BCNF: an MVD produces no conflicting scalar values, so FD checks alone will never reveal it.

In practice the disease hides in wide bridge tables with three or more foreign-key columns: order×channel×region, user×role×scope, product×tag×locale. Any time two of the dimensions are genuinely independent per key value, the row count and the anomaly risk are the same M×N product.

Where the previous rung stops: [[What is Boyce-Codd normal form and how does it differ from 3NF]]; the three-way generalization: [[What is fifth normal form and when does a three-way decomposition matter]]; what the unsplit version breeds: [[What can violating database normalization lead to]]; how joins recombine the split facts: [[How would you explain JOIN]].

> [!tip] Interview answer
> 4NF targets multivalued dependencies: when one key determines an independent set of values of two different attributes, one wide table stores the cross product — 3 tutors × 2 skills became 6 rows, and adding a single skill meant inserting 3. The fix is a table per set — 5 rows total — whose join rebuilds the original exactly. The gate is independence: if the lists are correlated, splitting fabricates facts. That is why 4NF is beyond BCNF — no FD check will ever catch it.
