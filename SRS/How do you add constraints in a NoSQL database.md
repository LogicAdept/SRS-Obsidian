<!--
reps: 0
priority: 0
-->
#Databases/NoSQL #SRS

# How do you add constraints in a NoSQL database

> [!abstract] Short answer
> **You use the store's native mechanisms: MongoDB validators with $jsonSchema or query-expression rules on collections; Redis enforces structure through its typed commands and application checks; wide-column stores validate types and rely on the partition/clustering design; everything beyond that — cross-document invariants — moves into application code or single-document design.** Uniqueness, where offered, is the one true cross-write constraint you get.

## Per-store mechanisms, named

**MongoDB** is the richest case: a collection can carry a `validator` with `$jsonSchema` (required fields, typed fields, ranges, pattern) or plain query-expression rules (`{price: {$gte: 0}}`). The `validationLevel` chooses whether rules apply to all documents or only inserts/updates (`strict`/`moderate`), and `validationAction` decides reject versus warn-only — reject is the default for failing operations, warn logs the violation and writes anyway. Crucially, **multi-document foreign-key-style references are NOT validated by the store**: an order may carry a userId that exists in no collection; the reference integrity is application-enforced, which is the classic trade documented in MongoDB's data-modeling guidance (embed or reference, and the application maintains consistency). **Uniqueness** is real: a unique index is the store-enforced constraint that two documents cannot share a value — the NoSQL replacement for a relational natural key. **Redis** constrains by *type discipline*: commands are type-specific (LPUSH only on lists, HSET only on hashes), so "a list is a list" is enforced by the engine; value-level rules (email format, ranges) are application code, optionally wrapped in Lua for atomicity. **Cassandra** validates column types and clustering order, and its lightweight transactions (Paxos-based LWT) give compare-and-set semantics for the rare cross-node invariant.

```javascript
db.createCollection("orders", {
  validator: {
    $jsonSchema: {
      required: ["userId", "status", "total"],
      properties: {
        status: { enum: ["NEW", "PAID", "CANCELLED"] },
        total:  { bsonType: "number", minimum: 0 }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
})
```

**Listing 1.** MongoDB schema validation: required fields, an enum, a range — enforced on writes, with reject-on-violation as the action.

```d2
direction: right
doc: "Document shape\nvalidator + $jsonSchema\nreject or warn per write" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
uniq: "Uniqueness\nunique index per collection" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
ref: "Cross-references\napplication code (or embed)\nno engine-side FK check" {
  width: 300
  height: 100
  style.fill: "#ffebee"
}
doc -> ref
uniq -> ref
```

**Fig. 1.** The constraint budget in a document store: shape and uniqueness are engine-enforced; referential integrity is deliberately the application's job.

> [!warning] "Schemaless" never meant "constraint-free by magic" — someone owns every invariant
> The trap is assuming flexible schema means validation is unnecessary: it means validation is *your* subsystem now. Every invariant a relational CHECK or FK would have enforced must be named — value ranges, enum states, required fields, references — and assigned to a validator, a unique index, or explicit application checks, ideally all in one place (a data-access layer) so three services cannot drift. The flip side is design: invariants that are hard to enforce across documents are often a signal to *embed* the related data into one atomic document, which MongoDB's modeling guidance treats as the first choice.

The relational contrast: [[How do you add constraints to a database]]; the store families behind the examples: [[What categories of NoSQL databases exist]]; transactions that bound multi-document work: [[How do you use multi-document transactions in Spring Data MongoDB]].

> [!tip] Interview answer
> In NoSQL you use each store's native constraint surface: MongoDB validators with $jsonSchema plus unique indexes, with validationLevel and validationAction tuning strictness; Redis enforces types through command discipline; Cassandra validates types and offers LWT compare-and-set. What you do not get is engine-checked cross-document references — those move to application code or to embedding related data in one document, and every invariant must be consciously owned somewhere.
