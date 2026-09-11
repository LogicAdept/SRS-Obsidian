<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #SRS

# What is normalization

> [!abstract] Short answer
> **Normalization is the step-by-step decomposition of tables so that every non-key fact lives in exactly one place, judged against the normal forms — 1NF, 2NF, 3NF, and beyond.** Its purpose is minimal redundancy and freedom from update anomalies; it is not a performance goal, and denormalization for read speed is a separate, deliberate step ([[What is database denormalization for]]).

## The process and the ladder

Normalization works by decomposition: given a table that mixes facts about different entities, split it so each relation holds facts about one entity keyed by one key, and connect the pieces with foreign keys. The normal forms grade the result. **1NF** — atomic values, no repeating groups; **2NF** — no non-key fact depending on only part of a composite key; **3NF** — no non-key fact depending on another non-key field. The usual mnemonic for 2NF/3NF is that every field must provide a fact about "the key, the whole key, and nothing but the key". Further forms (BCNF, 4NF, 5NF) tighten edge cases of determinant dependencies and multi-valued facts; OLTP schemas are normally engineered to 3NF, which removes the anomalies that matter in day-to-day writes.

```d2
direction: right
raw: "One wide table\norders + customer address\n+ product warehouse" {
  width: 240
  height: 100
  style.fill: "#ffebee"
}
n1: "1NF\natomic cells" {
  width: 150
  height: 80
  style.fill: "#fff3e0"
}
n2: "2NF\nno partial dependency" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
n3: "3NF\nno transitive dependency" {
  width: 220
  height: 80
  style.fill: "#e8f5e9"
}
raw -> n1 -> n2 -> n3
```

**Fig. 1.** Normalization as a sequence of decompositions, each killing one class of dependency: repeating groups, partial dependencies, transitive dependencies.

Each rung has a concrete symptom it removes, which is the practical way to reason: if the same address is stored on every order row, updates must hit many rows and can disagree (anomaly); after decomposition the address lives once in the customers table and orders reference it. The classic worked examples are in [[How would you explain first normal form in relational databases]], [[How would you explain second normal form in relational normalization]], and [[How would you explain third normal form in relational databases]].

The idea descends from Codd's relational model (1970), where normalization of non-simple domains was introduced, and the 2NF/3NF definitions come from Codd's early-1970s papers; Kent's 1983 guide remains the standard intuitive formulation. The model the whole ladder rests on is drilled in [[How would you explain the relational data model and Codd rules basics]].

> [!warning] Normalization has no unit of measure and no "fully normalized" badge
> Forms are judged per-relation against functional dependencies you can actually state; a schema is "in 3NF" relative to the dependencies you identified, and real schemas stop there for pragmatism. Believing normalization "removes all duplication" is also wrong — it removes redundancy of *facts*, while key values are deliberately repeated in referencing tables; and some duplication (snapshots, audit copies) is intentional design, not a violation.

The price of skipping it: [[What can violating database normalization lead to]]; the deliberate reverse step: [[What is database denormalization for]].

> [!tip] Interview answer
> Normalization is decomposition of tables so each non-key fact is stored once, checked against the normal forms: 1NF atomic values, 2NF no partial dependency on a composite key, 3NF no transitive dependency through another non-key field. It minimizes redundancy and update anomalies — its cost is more joins, which is why OLAP and read-heavy paths deliberately denormalize afterwards.
