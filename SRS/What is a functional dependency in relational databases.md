<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #Databases/Keys #SRS

# What is a functional dependency in relational databases

> [!abstract] Short answer
> **A functional dependency X → Y is a promise that the values in Y are determined by the values in X: any two rows that agree on X must agree on Y.** It is the vocabulary every normal form after 1NF is stated in — and the engine enforces an FD only when the determinant becomes a key; until then an FD is just a pattern your data happened to show so far.

## The definition, and where FDs actually live

X is the *determinant*, Y the *dependent*: `email → name` says the email decides the name, `zip → city` says the zip decides the city. The dependency *holds* in a relation when no pair of rows contradicts it. The trap is the gap between "holds in the current rows" and "is enforced by the schema": a flat table gives you no way to declare an FD at all. The only mechanism a relational engine has for making a determinant decisive is a key — PRIMARY KEY or UNIQUE. Normalization, at its core, is the move that converts trusted FDs into keys: decompose so that each determinant becomes the key of its own table. A trivial dependency `Y ⊆ X` (for example `zip, city → city`) never constrains anything — it is true by definition, which is why normal-form conditions always say *non-trivial*.

```sql
CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT, name TEXT);
INSERT INTO users VALUES (1, 'a@x.io', 'Ann'), (2, 'b@x.io', 'Bob');
-- FD email -> name holds in the data so far. The engine accepts:
INSERT INTO users VALUES (3, 'a@x.io', 'Ann Fake');   -- two names for one email

CREATE TABLE emails (email TEXT PRIMARY KEY, name TEXT NOT NULL);
INSERT INTO emails VALUES ('a@x.io', 'Ann Fake');     -- same insert, decomposed table
```

**Listing 1.** The same violation, before and after the FD becomes a key. Verified on SQLite 3.53.1: the flat table kept both `('a@x.io', 'Ann')` and `('a@x.io', 'Ann Fake')`; the decomposed table rejected the insert with `UNIQUE constraint failed: emails.email`.

## Closure: how keys fall out of an FD list

Given a set of FDs, the closure X⁺ is everything derivable from X using three inference rules — reflexivity (a set implies its subsets), augmentation (adding attributes to both sides preserves the dependency), and transitivity (`X→Y, Y→Z` gives `X→Z`; commonly grouped as Armstrong's axioms). A candidate key is then an X whose closure covers all attributes, minimal so that no proper subset does. Worked example: with `student_id → name`, `course_id → title`, `(student_id, course_id) → grade`, the closure of `(student_id, course_id)` reaches every attribute, while `student_id` alone closes at `{student_id, name}` — so the composite is the candidate key, and that is precisely why *partial* dependency on "part of a key" is a meaningful phrase in 2NF. This is the working skill behind the forms: from an FD list you derive keys and normal forms mechanically instead of eyeballing columns and hoping.

## Every form after 1NF is a statement about FDs

2NF forbids a non-key attribute depending on a *proper subset* of a candidate key; 3NF forbids transitive chains where a non-key attribute determines another non-key attribute — formally, every non-trivial FD must have a superkey determinant or a prime dependent; BCNF keeps only the superkey clause, no exceptions; 4NF and 5NF generalize the same machinery from functional to multivalued and join dependencies, where an FD is the special case that at most one Y-value matches each X. The full ladder: [[How would you explain second normal form in relational normalization]], [[How would you explain third normal form in relational databases]], [[What is Boyce-Codd normal form and how does it differ from 3NF]], [[What is fourth normal form and what are multivalued dependencies]].

> [!warning] A pattern in today's rows is not a dependency
> An FD is part of the schema's meaning, not a statistic: `zip → city` that "held since 2019" is one careless INSERT away from breaking, and nothing in a flat table will stop that insert (measured in Listing 1). Queries that silently rely on an FD — joins on the determinant, GROUP BY its dependent — multiply and misjoin rows the day the dependency breaks. Conversely, an FD the business states but the schema cannot enforce is exactly the redundancy source the normal forms exist to remove: state it, then either make the determinant a key or decompose until it is.

Keys behind the FDs: [[How would you explain candidate keys in relational databases]]; what a duplicate determinant does and does not mean for a PK: [[Can the same primary key value appear in two rows of one table]]; the endpoint of the decomposition: [[What is domain-key normal form and why is it a design goal rather than a rung]]; the ladder from the start: [[What is normalization]].

> [!tip] Interview answer
> X → Y means any two rows agreeing on X agree on Y; determinant X, dependent Y, trivial when Y ⊆ X. Every normal form after 1NF is phrased in these terms — 2NF kills partial FDs on key subsets, 3NF kills transitive non-key chains, BCNF requires every determinant to be a superkey. The mechanics: derive candidate keys via attribute closure (reflexivity, augmentation, transitivity), then check each non-trivial FD against the keys. And the practical point: an FD the data happens to satisfy is not enforced until its determinant is a key — measured: a flat table took a second name for the same email without complaint, a decomposed table with that determinant as PRIMARY KEY rejected the identical insert.
