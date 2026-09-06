<!--
reps: 0
priority: 0
-->
#Java/Persistence/JPA/Fetching #Java/Annotations #SRS

# What are JPA fetch types for entity associations?

> [!abstract] Short answer
> Associations use **`FetchType.EAGER`** or **`FetchType.LAZY`**. **EAGER** is a **requirement**: the provider must load that association when the entity is loaded. **LAZY** is a **hint**: the provider *may* still load it eagerly. Defaults: **`@OneToMany` / `@ManyToMany` → LAZY**; **`@ManyToOne` / `@OneToOne` → EAGER**. The default fetch graph is the **transitive closure** of every EAGER attribute. What JPA is: [[What is the Java Persistence API JPA]]. LAZY vs EAGER as a pair: [[What is the difference between JPA FetchType lazy and eager]].

## Two strategies, four relationship defaults

`jakarta.persistence.FetchType` is the `fetch` element on `@OneToOne`, `@OneToMany`, `@ManyToOne`, `@ManyToMany` (and also `@Basic` / `@ElementCollection`, which are not relationship mappings).

| Mapping | Default `fetch` |
| --- | --- |
| `@ManyToOne`, `@OneToOne` | **EAGER** |
| `@OneToMany`, `@ManyToMany` | **LAZY** |
| `@ElementCollection` | **LAZY** |
| `@Basic` | **EAGER** |

Collections default lazy so `find(Order.class, id)` does not load every line. Single-valued associations default eager, so the same `find` **must** load `order.getCustomer()` if it is `@ManyToOne` with the default. That customer’s own EAGER associations load too — that is the **default fetch graph**, not `CascadeType`. Cascade vs fetch: [[How would you explain CascadeType.ALL]]. One-to-many shape: [[What is an example of a one to many relationship in databases or JPA]].

```d2
direction: down
order: "find(Order)" {
  width: 140
  height: 40
}
cust: "@ManyToOne EAGER\nCustomer" {
  width: 180
  height: 50
  style.fill: "#ffcdd2"
}
addr: "Customer's @ManyToOne EAGER\nAddress" {
  width: 220
  height: 50
  style.fill: "#ffcdd2"
}
lines: "@OneToMany LAZY\nlineItems" {
  width: 180
  height: 50
  style.fill: "#e8f5e9"
}
order -> cust
cust -> addr
order -> lines
```

**Fig. 1.** Default fetch graph follows EAGER edges. LAZY collections stay out unless accessed (and even then LAZY is only a hint).

```java
@Entity
public class Order {
    @Id
    private Long id;

    @ManyToOne // fetch = EAGER by default
    private Customer customer;

    @OneToMany(mappedBy = "order") // fetch = LAZY by default
    private Set<LineItem> lines = new HashSet<>();

    protected Order() {}
}
```

**Listing 1.** Loading an `Order` must fetch `Customer` (and that customer’s EAGER graph). `lines` is not required to load until accessed.

Entity graphs (`jakarta.persistence.fetchgraph` / `loadgraph` on `find` or a query) override or augment these semantics. A fetch graph treats listed attributes as EAGER and unlisted ones as LAZY. The provider may still fetch extra state.

> [!warning] Default EAGER on @ManyToOne / @OneToOne is a join bomb
> Each default-EAGER many-to-one is in the fetch graph of its source. Nested EAGER many-to-ones chain. That is mapping fetch, not cascade persist/remove. Set `fetch = LAZY` on associations you do not always need, or use an entity graph for that `find`.

> [!warning] LAZY is not a guarantee
> The implementation is **permitted** to fetch a LAZY association eagerly. Conversely, after detach, only EAGER state (and already-accessed state) is safely available; navigating an unfetched LAZY association outside the persistence context is not portable. Hibernate’s `LazyInitializationException` is one provider’s reaction, not a JPA type.

> [!tip] Interview answer
> JPA has two fetch types: EAGER, which the provider must load with the entity, and LAZY, which is only a hint. Collections default to LAZY; ManyToOne and OneToOne default to EAGER, so finding an order loads its customer and then that customer’s eager associations. That graph is why people set LAZY on many-to-ones they do not always need.
