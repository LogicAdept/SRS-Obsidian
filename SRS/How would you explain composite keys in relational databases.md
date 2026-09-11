<!--
reps: 0
priority: 0
-->
#Databases/Keys #Databases/Indexes #SRS

# How would you explain composite keys in relational databases

> [!abstract] Short answer
> A composite key is a key made of two or more columns whose combination must be unique. As a constraint it enforces that no two rows repeat the same tuple of values; as the basis of an index it defines a lexicographic sort order, which is why column order controls what predicates the resulting index can serve.

## Constraint versus index

As a constraint, a composite key says the tuple (a, b) identifies a row: PostgreSQL's PRIMARY KEY (a, b) creates a unique B-tree index over both columns and NOT NULL on each; MySQL's InnoDB makes the composite primary key the clustered index; SQL Server makes it clustered by default. Uniqueness applies to the combination, not the parts: two rows may share `a` or share `b`, just not both. This is the standard modeling answer for junction tables in many-to-many relationships (student_id, course_id) and for natural keys like (tenant_id, external_id) in multi-tenant systems, and it is the reason the PK choice interacts with clustering as in [[How many clustered indexes can a table have and what is a clustered index physically]].

```sql
CREATE TABLE enrollment (
    student_id  BIGINT NOT NULL REFERENCES students(id),
    course_id   BIGINT NOT NULL REFERENCES courses(id),
    enrolled_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (student_id, course_id)
);
```

**Listing 1.** The pair is unique; duplicates of either column alone are fine and expected.

## The order question people forget

The moment the composite key becomes an index, order matters: (student_id, course_id) serves lookups by student and by student+course, but not by course alone — the leftmost prefix property in [[What is the leftmost prefix rule for composite indexes]]. InnoDB multiplies the effect because the composite PK is the clustered index and every secondary index entry duplicates all PK columns, so long composite keys bloat every secondary structure, per InnoDB's own guidance to keep primary keys short. Design habit: put the higher-selectivity or most-queried equality column first unless a specific ORDER BY needs the run order, in which case the sort column follows the equality columns as in [[How do you optimize ORDER BY with a filter]].

> [!warning] Composite key vs composite index confusion
> A composite key is a uniqueness/identity concept; a composite index is an access-path concept. A table can have a single-column primary key plus a separate composite unique index, and a composite key does not automatically make every member column individually unique. Answering this question with "it's two indexes" or "all columns are unique" fails the follow-up instantly.

> [!tip] Interview answer
> A composite key uses two or more columns together as the identifier: uniqueness holds for the combination, not the parts. As a constraint it is enforced by a unique index over the tuple, and as an index it sorts lexicographically, so column order decides which leading prefixes are seekable. In InnoDB the composite PK is also the clustered index and gets duplicated into every secondary index, so keep it short.
