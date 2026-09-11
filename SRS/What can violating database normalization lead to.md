<!--
reps: 0
priority: 0
-->
#Databases/NormalForms #Problems/Persistence #SRS

# What can violating database normalization lead to

> [!abstract] Short answer
> **Redundancy, and through it the three update anomalies: the same fact stored in many rows disagrees on update (update anomaly), facts cannot be stored without unrelated context (insertion anomaly), and deleting a row silently destroys an unrelated fact (deletion anomaly).** Unnormalized schemas also bloat storage and make every writer responsible for consistency that constraints cannot check.

## The three anomalies on one example

Keep Kent's warehouse table: (PART, WAREHOUSE, QUANTITY, WAREHOUSE-ADDRESS). **Update anomaly:** the warehouse moves; every row for every part stored there must be corrected — miss one and the database now states two addresses for one warehouse, and no constraint flags it because the duplicates are ordinary values, not keyed facts. **Insertion anomaly:** a new warehouse is built but stocks no parts — with the key being (part, warehouse) there is no row to record its address without inventing a fake part. **Deletion anomaly:** the last part leaves a warehouse; deleting that row erases the warehouse's address from the database entirely. The same pattern repeats at 3NF with employee/department/location and at 1NF with packed lists.

```d2
direction: right
u: "Update anomaly\nsame fact in N rows\npartial update -> disagreement" {
  width: 280
  height: 100
  style.fill: "#ffebee"
}
i: "Insertion anomaly\nfact needs unrelated key\nto exist at all" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
d: "Deletion anomaly\nlast row deletion\nloses an unrelated fact" {
  width: 260
  height: 100
  style.fill: "#e3f2fd"
}
```

**Fig. 1.** The three faces of redundancy: too much writing to stay consistent, facts that cannot be inserted, and facts that disappear as a side effect.

Beyond anomalies the costs are physical: duplicated values inflate table and index size (and backup windows), caches hold the same fact many times so stale copies outlive their TTLs, and application code grows "fixup" jobs that hunt inconsistencies — a tell that the schema stores one fact in several places.

> [!warning] The diseases are invisible until concurrency and time arrive
> On a laptop with one writer the unnormalized table behaves; the anomalies are *probabilistic* under real load — the second update of the same address can happen months apart, the deletion happens in an admin script nobody reviewed. That is why "we can just be careful" is the classic wrong answer: normalization moves the consistency burden from developer discipline into the schema, where a CHECK or FK enforces it forever. The legitimate counter-move is deliberate, measured denormalization for read speed — chosen with an update path, not drift: [[What is database denormalization for]].

The forms that prevent each disease: [[What is normalization]], [[How would you explain second normal form in relational normalization]], [[How would you explain third normal form in relational databases]].

> [!tip] Interview answer
> Violating normalization stores the same fact in many rows, which yields the three anomalies: updates must touch every copy and can disagree, some facts cannot be inserted without unrelated context, and deleting one row can erase an unrelated fact. Add storage bloat and constraint-blind drift. The cure is decomposition to 3NF for OLTP; denormalization stays acceptable only as a deliberate, maintained read-path choice.
