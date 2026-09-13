<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Mapping #Java/Persistence/JPA/Mapping #SRS

# What is ElementCollection and how does it differ from OneToMany?

> [!abstract] Short answer
> **`@ElementCollection`** maps a collection of **basic types or `@Embeddable`s** (`List<String> tags`, `List<Address> previousAddresses`) to a separate table **owned entirely by the parent entity**, declared with **`@CollectionTable`**. The difference from **`@OneToMany`** is **identity**: element rows are not entities — no independent lifecycle, no own optimistic-lock version, nothing else may reference them. Changes replace rows wholesale: modifying the collection issues **delete-all-and-reinsert** of the affected rows rather than a targeted diff, and the collection table has **no version column**, so two transactions editing it are not caught by optimistic locking on the collection itself. Use it for small, value-like data that never outlives the parent; use `OneToMany` once the target has its own identity, constraints, or inbound references.

## Same table shape, different ownership

Both annotations produce a child table with a foreign key to the parent, and both default to **`LAZY`** fetching with the same N+1 exposure ([[What is the N plus one problem in Hibernate]] applies unchanged). The semantics diverge at three points:

| | `@ElementCollection` | `@OneToMany` |
| --- | --- | --- |
| Target | basic type / `@Embeddable` | `@Entity` |
| Target identity | none — value semantics | primary key, independent state |
| Optimistic locking on child table | none by default | version on child entity |
| Update style | delete + reinsert affected rows | targeted `UPDATE` of child row |
| Referenced elsewhere | forbidden | expected (inverse side, queries) |
| Lifecycle | fully owned by parent | cascades decide (`CascadeType`, `orphanRemoval`) |

```java
@Entity
class Customer {
    @Id @GeneratedValue Long id;

    @ElementCollection(fetch = FetchType.LAZY)
    @CollectionTable(name = "customer_tags",
                     joinColumns = @JoinColumn(name = "customer_id"))
    @Column(name = "tag")
    Set<String> tags = new HashSet<>();

    @ElementCollection
    @CollectionTable(name = "customer_addresses",
                     joinColumns = @JoinColumn(name = "customer_id"))
    List<Address> addresses = new ArrayList<>();   // Address = @Embeddable
}
```

**Listing 1.** The collection table exists only because the parent says so; no `Address` entity exists anywhere.

## The delete-and-reinsert cost is the headline

Because element rows have no identity, the provider cannot diff "which element changed" — it sees a Java collection before and after. Add one tag to a ten-tag list and the typical flush is **`DELETE FROM customer_tags WHERE customer_id = ?` followed by ten inserts** (or reinsert of the surviving rows), not one insert. Three consequences follow:

- **Small collections only.** The strategy is O(collection size) per mutation, and mutation-frequency × size is the real cost model. A five-element tag list is the sweet spot; a growing event log is a `OneToMany`.
- **Merge on detached graphs amplifies it.** Loading a detached aggregate, touching the collection, and merging it back can rewrite every row, even if only one element changed.
- **No child-side locking.** Two transactions appending different tags both succeed on the child table; only the **parent's version** (if the collection is mapped with optimistic locking through the owning entity, or with explicit lock on the parent) detects the conflict. Where concurrent edits to the collection itself matter, entities are the honest model.

With an **`@OrderColumn`** the collection keeps a positional column — and pays for it: removing a middle element rewrites the order column of every subsequent row. Lists of embeddables without an order column behave as bags.

## When the mapping is right

Value-shaped data — tags, labels, historical names, a fixed set of preferences — that is **meaningless outside its parent** and never referenced by other entities. The schema gains a table, queries on the parent can join it when needed, and the code gains a plain `Set<String>` with no repository for the child type. The moment any of these stops holding — a row needs its own id, another context references it, you need `WHERE` queries with entity semantics or per-row locking — it is an entity, and `@OneToMany` with explicit cascades is the mapping that matches the domain ([[How would you explain CascadeType.ALL]] covers the lifecycle handoff; [[What is an AttributeConverter in JPA]] covers the simpler case where even the table is unnecessary).

> [!warning] Default fetch is LAZY, and the trap is serialization
> Touching an element collection outside the transaction fails the same way entity associations do; exposing an entity with element collections straight to a JSON serializer produces the same lazy-initialization failure or an extra query storm. Map to a DTO in the repository layer and the collection loads once, on purpose.

> [!tip] Interview answer
> `ElementCollection` maps basic or embeddable values into a parent-owned table: no child identity, no child version, delete-and-reinsert on change, so it is for small value data like tags or embedded addresses. `OneToMany` targets entities with their own identity, version, and lifecycle, and is the right call as soon as rows need constraints, references, or targeted updates. The N+1 exposure is identical, so the fetching discipline does not change — what changes is ownership: with a value collection the parent owns every row outright, and I price that as size × mutation frequency.

See [[What are JPA fetch types for entity associations]], [[What is the difference between JPA FetchType lazy and eager]], [[How would you explain CascadeType.ALL]], and [[What is the N plus one problem in Hibernate]].
