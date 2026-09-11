<!--
reps: 0
priority: 0
-->
#Databases/RelationalAlgebra #SRS

# How would you explain the relational data model and Codd rules basics

> [!abstract] Short answer
> **The relational model (Codd, 1970) represents data as relations — unordered sets of tuples over declared domains — accessed through relational algebra and keyed by values, not pointers.** Codd's 13 rules (0–12) grade how faithfully a DBMS implements the idea: full data independence, guaranteed access, systematic NULLs, an active online catalog, and at least one non-procedural language.

## The model's three components

**Structure:** a database is a set of time-varying relations; each relation is a set of n-tuples over domains (types). Position means nothing — domains are identified by name (Codd introduced role-qualified names for repeated domains, e.g. `sub.part` vs `super.part` in a component relation). **Integrity:** tuples are identified by candidate keys — Codd's primary-key notion: a nonredundant domain combination that uniquely identifies each tuple; relations cross-reference through foreign keys, "the possibility that S and R are identical is not excluded" (self-reference). **Manipulation:** relational algebra — selection, projection, join and the set operations — with retrievals defined as expressions over relations, so results of queries are themselves relations. That algebra is what SQL's SELECT projects from.

The rules (1974 article, numbered 0–12 after Rule 0 was added) operationalize "how relational is your system": Rule 1 — all data stored as table values; Rule 2 — guaranteed logical access by table name + key value + column name (no pointers); Rule 3 — NULLs distinct from zero and empty string; Rule 4 — the catalog itself is relational; Rule 5 — one comprehensive language (this is the rule SQL satisfied, and it is why SQL won); Rules 6–8 — view updating, high-level insert/update/delete (set-at-a-time), physical and logical data independence; Rules 9–12 demand integrity independence, distribution independence, and non-subversion (low-level bypass must not defeat integrity). No commercial system satisfies all of them — they are a measuring stick, not a checklist any product passes.

```d2
direction: right
struct: "Structure\nrelations = sets of tuples\nover named domains" {
  width: 280
  height: 100
  style.fill: "#e3f2fd"
}
integ: "Integrity\ncandidate keys · foreign keys\n(tuple identity by values)" {
  width: 290
  height: 100
  style.fill: "#fff3e0"
}
manip: "Manipulation\nrelational algebra\nqueries are expressions" {
  width: 270
  height: 100
  style.fill: "#e8f5e9"
}
struct -> integ -> manip
```

**Fig. 1.** The model's three pillars: set-based structure, value-based identity, and closed-world manipulation — queries over relations return relations.

> [!warning] "Relational" is a data model claim, not a product label
> Codd's rules were written partly against pre-relational systems that *stored tables* but exposed pointers and per-record navigation — satisfying the storage look while breaking data independence. The same confusion persists today: a system with "tables" but no constraint engine, no value-based access, or mandatory navigational access is not relational in Codd's sense. And the model is deliberately logical — nothing in it prescribes B-trees or pages; that separation is exactly what Rule 8 (physical independence) protects.

Where the model's key machinery gets daily use: [[What is a primary key and how do you choose one]], [[What is a foreign key]]; the normalization program it spawned: [[What is normalization]].

> [!tip] Interview answer
> Codd's relational model stores data as time-varying relations — unordered tuples over named domains — identified by candidate keys and cross-referenced by foreign keys, and manipulated through a closed algebra whose results are relations again. The rules grade implementations: value-based guaranteed access, systematic NULLs, a relational catalog, one comprehensive non-procedural language, and physical/logical data independence. SQL systems approximate it; the rules are the measuring stick.
