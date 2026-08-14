<!--
reps: 0
priority: 0
-->
#Java/HashCodeEquals #Methodologies/DDD #Java/Persistence/JPA #SRS

# In a business context must `equals` consider all entity fields?

> [!abstract] Short answer
> **No.** An entity is identified by its **identity**, not by a snapshot of every attribute. In Jakarta Persistence that identity is the **primary key**: it uniquely identifies the instance in a persistence context. Query-language equality of two entities of the same type is “same primary key,” not “same name, address, and version.” Hashing every mutable column also fights the `Map` rule that keys must not change in an `equals`-relevant way.

## Persistence identity is the key

Every entity has a primary key. That value uniquely identifies the instance to the `EntityManager`. After the instance is persistent, the application must not change the primary key; if it does, behavior is undefined.

The specification **requires** `equals` and `hashCode` on a **composite primary key class**, with value equality consistent with the mapped database types. The same requirement applies to an **embeddable used as a map key**, consistent with the mapped columns. It does **not** require the entity class itself to override `equals` using every persistent field.

In the query language, two entities of the same abstract schema type are equal if and only if they have the same primary key value. That is the persistence notion of “same entity,” not a field-by-field Java `equals`.

```d2
direction: down
e: "Entity instance" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
pk: "Primary key\n(identity)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
attrs: "Name, status, amount\n(mutable attributes)" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}

e -> pk
e -> attrs
```

**Fig. 1.** Changing an attribute does not mint a new entity. Changing the key would (and after persist it is undefined).

## Domain language: entity versus value

In a domain model, **entities** have identity that survives attribute updates (the same customer after a rename). **Value objects** are equal when their attributes are equal (a money amount, a composite key). Put `equals`/`hashCode` on the identity or on the value, respectively — not on “all columns of the table.” [[When should you override equals in Java]] is that semantic fork. [[How would you explain which fields should be included when implementing hashCode in Java]] follows the fields `equals` actually uses.

A generated id starts unset. If entity `hashCode` uses that id, the integer changes at `persist` while the object may already sit in a `HashSet`. That is the mutable-key failure. [[Can you lose objects in a HashMap due to mutable or poorly chosen keys]] is the collection side. Stable business keys, or identity `equals` until you have a key, are design choices; they are not “include every field.”

The entity class must be non-final, so a subclass can exist. Mixing `instanceof` with extra subclass state still breaks symmetry. [[How would you explain symmetry requirements for the equals contract in Java]] still applies.

> [!warning] “Lombok on all fields”
> Including associations, timestamps, and mutable columns makes two loads of the same row unequal after an edit, and makes a `Set<Entity>` unsafe. The spec’s mandatory `equals`/`hashCode` is on the **key type**, aligned with the database, not on the whole entity graph.

> [!tip] Interview answer
> **No. Entities compare by identity — in JPA, the primary key — not by every field. The spec demands `equals`/`hashCode` on composite key classes and embeddable map keys, consistent with the database. Value objects hash their attributes. Hashing all mutable columns breaks both domain identity and hash-table keys.**
