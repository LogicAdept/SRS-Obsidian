<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Mapping #Java/Persistence/JPA/Mapping #SRS

# How do you map a composite key in JPA?

> [!abstract] Short answer
> Two mechanisms, one invariant. **`@EmbeddedId`**: define an `@Embeddable` class holding the key columns, put a single field of that type into the entity, and the key is a real value object you can pass around. **`@IdClass`**: keep the key columns as separate fields on the entity, and give the provider a parallel class (`@IdClass(ShipmentPk.class)`) that repeats those fields only for identity — the entity stays flat, the key class is invisible in queries. Both require the key class to implement **`equals`/`hashCode`** (the provider compares keys in maps and cache lookups), a **no-arg constructor**, and to be `Serializable`. Neither can be combined with `@GeneratedValue` — the key is assigned by the application or comes from business data, never from a sequence. The design question underneath: a composite key is correct when the combination **is** the identity (line items keyed by `(order_id, line_no)`, join tables with extra columns); when it merely happens to be unique, prefer a surrogate `@Id` plus a unique constraint — generated ids make FKs cheap and every ORM mechanism (caching, batching, lifecycle) works without exceptions.

## EmbeddedId: the key as a value object

The embeddable approach models the key as a first-class type: `ShipmentPk` with `countryId` and `warehouseId`, marked `@Embeddable`, then `@EmbeddedId private ShipmentPk pk;` on the entity. The type earns its place: repository lookups take the whole key object, JPQL navigates it as a path (`where s.pk.countryId = :c`), and the entity's constructor can enforce invariants on the combination instead of trusting callers to fill two fields consistently. The costs are also real: every entity that wants this key repeats the embeddable (composition, not inheritance), and Spring Data derived queries operate on the nested field (`findByPkCountryId`), which reads awkwardly — a common middle ground is to keep the embeddable but expose key fields via getters on the repository layer.

## IdClass: flat fields, parallel identity

`@IdClass` keeps the columns directly on the entity (`long countryId; long warehouseId;` each annotated `@Id`) and names the key class at the type level. Nothing structural changes in the entity; the class named in `@IdClass` exists so `find()` and internal maps can pass a key around. This fits when the entity already represents a legacy table with natural composite columns and you do not want a wrapper leaking into the domain model. The trade-off mirrors the other side: no type to hang invariants on, duplicate field declarations between entity and key class that must stay in sync, and JPQL refers to the plain field names (`where s.countryId = :c`) — convenient for hand-written queries, weaker for type safety.

| | `@EmbeddedId` | `@IdClass` |
| --- | --- | --- |
| Key shape | real `@Embeddable` type | shadow class, entity fields stay flat |
| JPQL navigation | `e.pk.field` | `e.field` |
| Spring Data lookups | `findByPkField(...)` / whole-key `findById(key)` | `findByCountryIdAndWarehouseId(...)` |
| Reusable key type | yes — shareable across entities | no — declared per entity |
| Invariants on the combination | natural (in the embeddable) | not expressible |
| `equals`/`hashCode` | mandatory in the embeddable | mandatory in the id class |

```java
@Embeddable
public class ShipmentPk implements Serializable {
    private Long countryId;
    private String warehouseCode;
    // no-arg ctor, full ctor, equals/hashCode over BOTH fields
}

@Entity
public class Shipment {
    @EmbeddedId
    private ShipmentPk pk;          // the identity is the pair

    @ManyToOne(fetch = FetchType.LAZY)
    @MapsId("countryId")            // shares the FK column with part of the key
    private Country country;
}
```

**Listing 1.** A frequent real shape: `@MapsId` lets a `@ManyToOne` association *be* part of the key instead of duplicating the column — the join column feeds `pk.countryId`, so there is one physical column and one owner for it.

> [!warning] equals/hashCode on the key is not style advice
> The provider stores entities keyed by identifier in the persistence context and in shared caches. A key class that delegates `equals` to object identity makes the same database row appear as different entries — duplicate loads, broken `Set` semantics, cache misses that never hit. Write structural `equals`/`hashCode` over all key fields, and keep the key class `Serializable` because detached keys cross serialization boundaries (HTTP sessions, caches, async pipelines).

> [!tip] Interview answer
> Composite keys come in two shapes: `@EmbeddedId` makes the key an `@Embeddable` value object — reusable, type-safe, navigated as `pk.field` — while `@IdClass` keeps the columns flat on the entity and names a shadow class that repeats them for identity lookups. Both need structural equals/hashCode, a no-arg constructor, and Serialization, and neither works with `@GeneratedValue` because the key is business-assigned. `@MapsId` connects key parts to association FKs so there is one physical column. I reach for the embeddable when the combination is a genuine domain concept and for join tables with extra columns; and when the composite is just "unique by accident", I push for a surrogate id plus a unique constraint instead — generated keys keep every ORM mechanism, from batching to caching, on its happy path.

See [[How would you explain composite keys in relational databases]], [[What is the JPA Id annotation]], [[What is the difference between JPA FetchType lazy and eager]], [[What is ElementCollection and how does it differ from OneToMany]], and [[How do you choose a JPA inheritance mapping strategy]].
