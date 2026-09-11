<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #SRS

# How would you explain second normal form in relational normalization

> [!abstract] Short answer
> **2NF forbids a non-key column that depends on only part of a composite key — a partial dependency.** It can only be violated when the key is composite: if every non-key fact is a fact about the *whole* key, the table is in 2NF.

## The classic partial dependency, from Kent's guide

Kent's inventory table is the canonical example: key (PART, WAREHOUSE), with QUANTITY — a fact about the whole pair — but also WAREHOUSE-ADDRESS, a fact about WAREHOUSE alone. The address is repeated on every row for any part stored there; changing it touches many rows and can disagree between them; and a warehouse holding no parts has no row to keep its address at all. Those are exactly the update, insertion, and deletion anomalies 2NF exists to kill.

```sql
-- violates 2NF: WAREHOUSE-ADDRESS depends on WAREHOUSE only
CREATE TABLE inventory_bad (
  part             int,
  warehouse        int,
  quantity         int,
  warehouse_address text,          -- fact about warehouse, not the pair
  PRIMARY KEY (part, warehouse)
);

-- 2NF: split by what each fact is about
CREATE TABLE inventory (
  part      int,
  warehouse int,
  quantity  int,
  PRIMARY KEY (part, warehouse)
);
CREATE TABLE warehouses (
  id       int PRIMARY KEY,
  address  text
);
```

**Listing 1.** The repair: decompose so each non-key column depends on the entire key of its table — quantity on (part, warehouse), address on warehouse id.

```d2
direction: down
inv: "inventory (part, warehouse)\nquantity: whole key" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
wh: "warehouses (id)\naddress: key only" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
inv -> wh: "warehouse = id"
```

**Fig. 1.** After decomposition every fact sits under the full key it depends on, joined back through a foreign key when needed.

Note the scope: with a single-column primary key there is nothing to be "part" of the key, so 2NF is automatic — interviewers use that as a quick probe. Surrogate-key designs can also *hide* a latent 2NF problem: slapping `id int` on a table does not make the data dependencies disappear; the composite business key (part, warehouse) still governs the facts, and the decomposition rule still applies to how you split tables.

> [!warning] 2NF is about dependencies, not about "columns I see twice"
> The same address appearing in two tables is normal — one of them stores it, the other references it. The violation is a non-key column whose value is determined by a *subset of the key* within one relation. Over-eager "dedup everywhere" designs that split until every table is two columns lose joins and transactions for nothing; stop when every non-key column depends on the whole key — then move to 3NF, whose transitive-dependency case is the other classic: [[How would you explain third normal form in relational databases]].

Position in the ladder: [[What is normalization]]; the dependency that motivates keys overall: [[How would you explain candidate keys in relational databases]].

> [!tip] Interview answer
> Second normal form forbids partial dependencies: a non-key column determined by only part of a composite key. The example is warehouse address hanging off the (part, warehouse) key of inventory — repeated per row, inconsistent on update, and unstoreable for an empty warehouse. The cure is decomposition: quantity under the whole key, address under warehouse. With a single-column key 2NF cannot be violated.
