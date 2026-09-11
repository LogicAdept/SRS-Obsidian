<!--
reps: 0
priority: 0
-->
#Databases/SQL #SRS

# How many normal forms are commonly taught for relational databases?

> [!abstract] Short answer
> The commonly taught ladder is **1NF, 2NF, 3NF** (Codd), plus **BCNF** as the stricter 3NF refinement; some curricula continue to 4NF (multivalued dependencies) and 5NF/6NF (join dependencies). The interview-standard answer: name the first three precisely, say "and BCNF when a 3NF table still has a composite key overlapping a non-key dependency", and know that practical schemas usually target 3NF/BCNF with deliberate denormalization for read performance ([[What is a SQL view and what is it used for]]).

Each form removes one anomaly class. **1NF**: atomic values, no repeating groups — a `courses TEXT` column holding 'SQL,Java' is the canonical violation; the fix is one row per fact (the enrollment table). **2NF**: 1NF plus no *partial* dependency — in a table keyed `(student, course)`, a `student_name` column depending only on part of the key is the violation; move it out. **3NF**: no *transitive* dependency — `zip -> city` hiding inside an address table keyed by customer id; move it out. **BCNF**: every determinant is a key — the subtle case where a 3NF table still decomposes (two overlapping candidate keys). The verified demo shows the lossless-join property that makes the theory trustworthy: the normalized pair of tables reconstructs the original facts exactly via join (`Ann|SQL,Java` re-aggregated from enrollment rows) — normalization is a lossless decomposition, which is why it can be undone for reports ([[Why can a JOIN multiply your row count]]). The anomalies the forms prevent are the interview payoff: update anomalies (fix the zip in many rows), insert anomalies (cannot add a course without a student), delete anomalies (losing the last enrollment erases the course).

```sql
CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT UNIQUE);
CREATE TABLE courses (id INTEGER PRIMARY KEY, title TEXT UNIQUE);
CREATE TABLE enrollment (student_id INTEGER REFERENCES students(id),
  course_id INTEGER REFERENCES courses(id),
  PRIMARY KEY (student_id, course_id));
INSERT INTO students VALUES (1,'Ann'),(2,'Bob');
INSERT INTO courses VALUES (1,'SQL'),(2,'Java');
INSERT INTO enrollment VALUES (1,1),(1,2),(2,2);

SELECT s.name, group_concat(c.title) FROM enrollment e
JOIN students s ON s.id = e.student_id
JOIN courses c ON c.id = e.course_id
GROUP BY s.name ORDER BY s.name;
-- Ann|SQL,Java
-- Bob|Java
```

**Listing 1.** Verified on SQLite 3.53.1. The 1NF-violating `courses TEXT` list became a link table keyed on `(student_id, course_id)` — a composite PK that is also the 2NF lesson — and the join reconstructs the original lists losslessly.

```d2
direction: right
f1: "1NF
atomic values" {width: 150; height: 80}
f2: "2NF
no partial dependency
on composite keys" {width: 200; height: 90}
f3: "3NF
no transitive
dependencies" {width: 160; height: 90}
f4: "BCNF
every determinant
is a key" {width: 170; height: 90}
f1 -> f2 -> f3 -> f4
```

**Fig. 1.** Each normal form removes one dependency pathology; the ladder is cumulative, and real schemas stop where read-performance demands it.

> [!warning] Normalization is a write-side discipline; reads pay until you design for it
> Fully normalized schemas answer complex reports with multi-join queries — where fan-out, join-order costs and the need for aggregate materializations appear. The senior position: normalize by default, denormalize (materialized views, summary tables, cached counts) with a refresh story, never the reverse out of laziness ([[How would you explain MATERIALIZED VIEW]]).

> [!tip] Interview answer
> Commonly taught: 1NF atomic values, 2NF no partial dependencies on composite keys, 3NF no transitive dependencies, plus BCNF where every determinant is a key — 4NF and 5NF exist for multivalued and join dependencies. The practical line I draw: design to 3NF/BCNF to kill update, insert and delete anomalies, then denormalize deliberately for read paths with materialized aggregates. The key property that makes it safe is lossless decomposition — the normalized tables reconstruct the original facts by join.
