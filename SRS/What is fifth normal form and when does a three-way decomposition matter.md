<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #SRS

# What is fifth normal form and when does a three-way decomposition matter

> [!abstract] Short answer
> **5NF (project-join normal form) means every join dependency of a table is implied by its keys — the table cannot be split into smaller projections that join back with spurious or lost rows.** It matters only for genuinely three-way relationships, where three pairwise facts jointly assert the triple; then the table decomposes into three projections and reassembles exactly.

## Three pairwise facts that imply the triple

The working case: suppliers, parts, projects, with three independent many-to-many facts — supplier supplies part (sp), part is allocated to project (pj), supplier is contracted on project (sj). The business rule of the relationship: a triple (supplier, part, project) is asserted exactly when **all three** binary facts exist together. Under that rule a single triple table is redundant three ways — every projection of it (sp, pj, sj) repeats facts — and 5NF says: store the three binary tables and let the triple be their three-way join. Formally: a join dependency ⋈{R1, R2, R3} holds on R, and when the only such dependencies are the ones keys imply, R is in 5NF.

```sql
CREATE TABLE sp (supplier TEXT, part TEXT, PRIMARY KEY (supplier, part));
CREATE TABLE pj (part TEXT, project TEXT, PRIMARY KEY (part, project));
CREATE TABLE sj (supplier TEXT, project TEXT, PRIMARY KEY (supplier, project));
-- triple (s,p,j) asserted iff (s,p) in sp AND (p,j) in pj AND (s,j) in sj
```

**Listing 1.** The three projections. Verified on SQLite 3.53.1 with 3 rows each: the three-way join returns exactly the 4 triples the combined facts assert.

## Why two of the three are not enough

Joining only sp and pj produced **5** rows — one more than the 4 true triples. The extra row (S2, P1, J2) is **spurious**: S1 supplies P1 and P1 sits on J2, but S2 has no contract on J2, so only the third projection can veto it. Dropping any one of the three tables either fabricates rows (spurious tuples) or loses them; the decomposition is lossless precisely when **all three** projections are joined. That is the interview-grade content of 5NF: with 4NF it was two lists and one split; here the join dependency has three components, and pairwise joins are provably insufficient.

```d2
direction: right
sp: "sp\n(supplier, part)" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
pj: "pj\n(part, project)" {
  width: 170
  height: 80
  style.fill: "#e3f2fd"
}
sj: "sj\n(supplier, project)" {
  width: 180
  height: 80
  style.fill: "#e3f2fd"
}
pair: "sp JOIN pj\n5 rows\n1 spurious" {
  width: 160
  height: 90
  style.fill: "#ffebee"
}
all: "3-way join\n4 rows\nexact" {
  width: 140
  height: 80
  style.fill: "#e8f5e9"
}
sp -> pj -> pair
pair -> sj -> all
```

**Fig. 1.** Pairwise join of a three-component join dependency is not lossless; the third projection filters the spurious tuple out. Verified on SQLite 3.53.1: 5 rows pairwise, 4 after the third join — matching the asserted facts exactly.

> [!warning] The split is valid only while the implication rule holds
> If even one triple has independent meaning — the supplier ships this part to this project **only** as a package, and the pairwise facts do not exist for it — then the three binary tables cannot store or reconstruct that fact: the decomposition is lossy, and the original table was already the irreducible design. Blind "split everything into two-column tables" is the popular misreading; the split is licensed by the join dependency, not by row width. And check the flip side: if the pairwise facts are *not* maintained independently (sp is always derived from triples), the three-table design forces meaningless inserts to make a triple visible.

Practical frequency is low: most real schemas reach 3NF/BCNF and stop, and 4NF/5NF cases announce themselves as wide bridge tables between three entities with independently maintained pairs. They surface in er-modeling debates and in warehouse staging, where facts about three dimensions are loaded from separate sources and the join must be exact. When the sources do not guarantee the implication rule, keep the triple table and enforce the pairs as constraints instead.

The two-set version of the same idea: [[What is fourth normal form and what are multivalued dependencies]]; why determinants, not just sets, push you past 3NF: [[What is Boyce-Codd normal form and how does it differ from 3NF]]; the join mechanics reassembling projections: [[How would you explain JOIN]]; when deliberate redundancy is the better trade: [[What is database denormalization for]].

> [!tip] Interview answer
> 5NF is about join dependencies: when three pairwise facts — supplier-part, part-project, supplier-project — jointly imply the triple, the triple table decomposes into those three projections and joins back with zero spurious rows. The measured point: joining just two of the three gave 5 rows where only 4 triples were true; the third projection removed the fabricated one. The split is licensed only while the implication rule holds — a package-only triple makes it lossy. In practice you rarely go past BCNF; 5NF appears with three-entity bridge tables fed from independent sources.
