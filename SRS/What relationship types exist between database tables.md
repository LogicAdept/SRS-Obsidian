<!--
reps: 0
priority: 0
-->
#Databases/Keys #SRS

# What relationship types exist between database tables

> [!abstract] Short answer
> **Three cardinalities: one-to-one (each row of A matches at most one row of B), one-to-many (one parent row, many child rows), and many-to-many (rows of A relate to arbitrary rows of B).** A relational database realizes all three with foreign keys; M:N additionally requires a junction table carrying a pair of foreign keys.

## How each cardinality is physically expressed

**One-to-one** (university ↔ its rector): the child table carries a UNIQUE foreign key — `rectors(id PRIMARY KEY, university_id UNIQUE REFERENCES universities)`, or the merge option: put the rare fields in the main table. The uniqueness constraint is what enforces "at most one" on the DB side. **One-to-many** (university → faculties): the many side holds a plain (non-unique) foreign key; this is the default shape of application data — orders to lines, users to sessions. **Many-to-many** (professors ↔ faculties): a junction table `faculty_members(professor_id, faculty_id)` with a composite key over both columns; extra columns on the junction (since when, role) are where relationship attributes live, and queries across it join twice.

```sql
-- 1:1  unique FK
CREATE TABLE rectors (
  id            int PRIMARY KEY,
  university_id int UNIQUE REFERENCES universities
);
-- 1:N  plain FK on the many side
CREATE TABLE faculties (
  id            int PRIMARY KEY,
  university_id int REFERENCES universities
);
-- M:N  junction with composite key
CREATE TABLE faculty_members (
  professor_id int REFERENCES professors,
  faculty_id   int REFERENCES faculties,
  PRIMARY KEY (professor_id, faculty_id)
);
```

**Listing 1.** The three cardinalities as DDL: a UNIQUE constraint turns a foreign key into 1:1; the junction table turns two 1:N links into M:N.

```d2
direction: right
u: "universities" {
  width: 170
  height: 70
  style.fill: "#e3f2fd"
}
r: "rectors (unique FK)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
f: "faculties (FK)" {
  width: 190
  height: 70
  style.fill: "#fff3e0"
}
p: "professors" {
  width: 150
  height: 70
  style.fill: "#fff3e0"
}
j: "faculty_members (junction)" {
  width: 250
  height: 70
  style.fill: "#ffebee"
}
u -> r: "1:1"
u -> f: "1:N"
p -> j
f -> j: "M:N"
```

**Fig. 1.** Cardinality is enforced by constraints, not by convention: UNIQUE for one-to-one, plain FK for one-to-many, a composite-keyed junction for many-to-many.

> [!warning] The junction table's composite key is part of the model, not a style choice
> Dropping the composite PK (leaving both FKs unindexed/unconstrained) lets the same professor-faculty pair be inserted twice — data corruption the DBMS will happily store. Related drift: making a "1:1" with a plain FK and trusting the application; and a self-referencing edge case — a table relating to itself (employee → manager) — which is still one-to-many over the same table, per [[How would you explain reflexive relations in relational algebra]].

Key terminology behind the DDL: [[What is a foreign key]], [[What is a primary key and how do you choose one]], and the composite-key drill in [[How would you explain composite keys in relational databases]].

> [!tip] Interview answer
> One-to-one is a foreign key with a UNIQUE constraint (or merged columns); one-to-many is a plain foreign key on the child side; many-to-many is a junction table with a composite key over two foreign keys, carrying relationship attributes like role or date. All cardinality is enforced by constraints in the schema, not by application discipline.
