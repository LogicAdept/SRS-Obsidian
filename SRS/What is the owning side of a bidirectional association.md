<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Mapping #Java/Persistence/JPA/Mapping #SRS

# What is the owning side of a bidirectional association?

> [!abstract] Short answer
> In a bidirectional association two Java fields describe **one** database relationship, and the **owning side** is the one whose mapping physically drives the foreign key column. The rule: the side holding `@JoinColumn`/`@ManyToOne` owns it; the opposite side must say `mappedBy = "..."` and becomes the **mirror** — it only reads what the owner wrote. Why it matters mechanically: without `mappedBy` on the `@OneToMany` side, the provider assumes you want an **independent join table** — measured: a unidirectional `@OneToMany` without `@JoinColumn` created an extra table `ORDS_A_ITEMS_A` alongside `ORDS_A`/`ITEMS_A`, while the bidirectional `mappedBy` variant produced only `ORDS_B`/`ITEMS_B` with the FK living in the child — an extra table and extra statements you almost never want. And semantically: only the owner's in-memory state is flushed; a change made **only** to the mirror side is silently ignored by the flush (no error), which is the classic "my children didn't get saved" bug. The discipline: pick the `@ManyToOne` side as owner (the FK belongs to the child table), always sync both sides in Java with helper methods, and cascade from the parent.

## Who writes the FK, and what the mirror is for

The database has exactly one FK column per relationship — one side of the Java mapping must be responsible for it, or the mapping would have two conflicting definitions of the same column. `@ManyToOne` with `@JoinColumn(name = "ord_b_id")` owns by default: the child table carries the column, so the child is the natural owner. The parent's `@OneToMany(mappedBy = "order")` declares: "this collection reflects the `order` field on `ItemB` — do not create any schema for me". The mirror is not decoration, it is navigation convenience and cascade surface; but its **writes** are bookkeeping for the Java heap only. Hibernate diffs the owner to build SQL; if you mutate only the mirror (`parent.getItems().add(child)` without setting `child.setParent(parent)`), the in-memory graph says one thing, the flush says another, and the FK simply never appears.

Measured schema consequences of the two mapping styles for the same parent–children relationship:

| Mapping | Tables created | FK location | Statements per persist |
| --- | --- | --- | --- |
| unidirectional `@OneToMany`, **no** `@JoinColumn` | parent, child, **plus join table** `ORDS_A_ITEMS_A` | join table columns | extra inserts into the join table |
| unidirectional `@OneToMany`, **with** `@JoinColumn(name="ord_a_id")` | parent, child | child table — parent owns the FK anyway | fine, but no back-reference navigation |
| bidirectional, `@ManyToOne` + `@OneToMany(mappedBy="order")` | parent, child **only** | child table | child insert with FK — the minimal shape |

```java
@Entity class Order {
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Item> items = new ArrayList<>();

    public void addItem(String label) {           // the discipline: one entry point
        Item item = new Item(label);
        item.setOrder(this);                      // owner side — drives the FK
        items.add(item);                          // mirror side — keeps the heap honest
    }
}
@Entity class Item {
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ord_b_id")                // OWNING side
    private Order order;
}
```

**Listing 1.** The canonical bidirectional setup: child owns the FK, parent mirrors with `mappedBy`, and a helper method syncs both sides so callers cannot produce a half-updated graph.

## The two classic failure modes

**The extra join table.** A unidirectional `@OneToMany` without `@JoinColumn` looks innocent — "I don't need the child-to-parent direction" — and produces a third table with two FK columns, inserts into it for every link, and a schema that surprises every DBA reading it. If you truly want unidirectional, add `@JoinColumn` so the FK lands in the child; if you want navigation both ways, use the full bidirectional shape with `mappedBy`. **The silent ignored write.** Under `cascade = ALL` the parent persist cascades to the items *in its own collection*; an item attached only via `child.setParent(order)` but not present in `order.getItems()` will not be cascaded, and an item added only to the mirror collection will not update the FK. Both directions must agree, because cascades read the mirror while flushes read the owner. That asymmetry — cascade walks one field, SQL writes the other — is the whole reason bidirectional mappings need a sync discipline rather than trust.

> [!warning] equals/hashCode and toString recurse through bidirectional graphs
> The mirror side creates object cycles. Generate `toString`/`equals`/`hashCode` naively and persisting one order prints or hashes the whole child graph — and lazy proxies inside those calls trigger loads in the middle of flush-time bookkeeping. Exclude the collection side (hash on business fields, or on the owner only), keep the cycle out of generated code.

> [!tip] Interview answer
> The owning side is the mapping that physically owns the FK: normally the @ManyToOne child with @JoinColumn, while the parent's @OneToMany(mappedBy=...) is a mirror that creates no schema and whose in-memory changes are not flushed. Measured the schema difference: a unidirectional OneToMany without @JoinColumn created an extra join table ORDS_A_ITEMS_A, the mappedBy shape created only parent and child with the FK in the child. The two classic bugs follow: join-table surprise for unmapped unidirectional parents, and silently ignored writes when only the mirror side is mutated. My discipline: child owns, parent mirrors and cascades, and a helper method mutates both sides so the heap and the database cannot diverge.

See [[How would you explain CascadeType.ALL]], [[What is ElementCollection and how does it differ from OneToMany]], [[What are JPA fetch types for entity associations]], [[How does an aggregate persist and publish events without a distributed transaction]], and [[How do you map a composite key in JPA]].
