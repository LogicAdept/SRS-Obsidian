<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #SRS

# How would you explain third normal form in relational databases

> [!abstract] Short answer
> **3NF forbids transitive dependencies: a non-key column must not depend on another non-key column — every non-key fact must depend on the key alone.** The repair is to promote the intermediate entity into its own table.

## The classic transitive chain

Kent's example: EMPLOYEE is the key; DEPARTMENT is a fact about the employee; LOCATION is a fact about the **department**, not the employee. Through DEPARTMENT, LOCATION depends on EMPLOYEE transitively — so the location repeats on every employee row of that department, updates can disagree row by row, and a department with no employees has nowhere to keep its location. Formally: if key → A and A → B (A non-key), then B depends on the key transitively, and the table is not in 3NF.

```sql
-- violates 3NF: LOCATION -> depends on DEPARTMENT (non-key)
CREATE TABLE employees_bad (
  id         int PRIMARY KEY,
  name       text,
  department text,
  location   text               -- fact about the department
);

-- 3NF: the department carries its own location
CREATE TABLE employees (
  id         int PRIMARY KEY,
  name       text,
  department text
);
CREATE TABLE departments (
  name     text PRIMARY KEY,
  location text
);
```

**Listing 1.** The decomposition follows the dependency: location moves to the table whose key it truly depends on.

```d2
direction: down
emp: "employees (id)\nname · department" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
dep: "departments (name)\nlocation" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
emp -> dep: "department = name"
```

**Fig. 1.** After the split, every non-key fact depends on the key directly: name and department on employee id, location on department name.

2NF and 3NF together compress into the working rule: every field provides a fact about "the key, the whole key, and nothing but the key" — 2NF removes facts about part of the key, 3NF removes facts about another non-key field. Because transitive dependencies do not require a composite key, 3NF is the form you violate most often in practice: status_label copied next to status_code, city stored next to zip, category_name next to category_id.

> [!warning] 3NF is not free — and not always the finish line
> Every decomposition adds a join to the read path; for read-heavy analytical workloads that cost is why denormalization exists as a deliberate step. And 3NF still allows determinants that are not candidate keys (that is BCNF's job, where every determinant must be a key) — the distinction matters with overlapping composite keys, and BCNF is the usual "we went beyond 3NF" follow-up an interviewer probes. Know both names, and be able to say why the employee/departments split also fixes deletion of the last employee losing the department location.

Where the ladder started: [[What is normalization]]; the preceding rung: [[How would you explain second normal form in relational normalization]]; the deliberate reverse: [[What is database denormalization for]].

> [!tip] Interview answer
> Third normal form kills transitive dependencies: no non-key column may depend on another non-key column. The employee → department → location chain is the canonical case — location repeats per employee, can disagree, and vanishes with the last employee. Promote the intermediate entity to its own table. It is the rung most often broken in real schemas (status_label next to status_code), and beyond it sits BCNF requiring every determinant to be a key.
