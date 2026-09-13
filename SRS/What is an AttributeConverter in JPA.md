<!--
reps: 0
priority: 0
-->
#Java/Persistence/Hibernate/Mapping #Java/Persistence/JPA #SRS

# What is an AttributeConverter in JPA?

> [!abstract] Short answer
> An **`AttributeConverter`** is a class that converts **one entity attribute type ↔ one JDBC column type**: `AttributeConverter<X, Y>` with `convertToDatabaseColumn(X)` and `convertToEntityAttribute(Y)`. You attach it with **`@Converter`** (optionally **`autoApply = true`** to hit every attribute of that type). It runs on load and on store, and inside queries the provider applies it to literals and parameters so **`where e.status = :status` still matches the stored representation**. Standard uses: enums stored as a **business code** instead of `name()`, booleans as `'Y'/'N'`, small value objects (email, money) as one column, column-level **encryption/masking** at the persistence boundary. The spec **forbids** converters on id, version, and relationship attributes. The senior pitfall: a converter that transforms values non-trivially can turn an index-friendly comparison into a function-per-row one — know what SQL your converter produces.

## The mechanics

```java
@Converter(autoApply = true)
public class OrderStatusConverter
        implements AttributeConverter<OrderStatus, String> {

    @Override
    public String convertToDatabaseColumn(OrderStatus status) {
        return status == null ? null : status.getCode();   // "NEW", "PD", "SH"
    }

    @Override
    public OrderStatus convertToEntityAttribute(String code) {
        return code == null ? null : OrderStatus.fromCode(code);
    }
}
```

**Listing 1.** One converter covers every `OrderStatus` attribute in the application; without `autoApply` you would annotate each field with `@Convert`.

The conversion is **symmetric and total**: whatever the column returns on load goes through `convertToEntityAttribute`, whatever the entity holds at flush goes through `convertToDatabaseColumn`. Bad data becomes a load-time exception — a corrupted code fails on `find`, not on some later business call, which is exactly the value of the boundary: the entity never sees the storage representation. For enums the standard mapping is `name()`/`ordinal()`; a converter switches you to stable codes so reordering constants or renaming the enum stops being a data migration.

## Where it applies — and where it must not

The spec applies converters to **basic attributes only**: id attributes, version attributes, relationship attributes and elements of relationships are excluded (element collections of basic types *are* covered). Query handling: literals and bound parameters are converted so equality predicates work against the stored form; range predicates and `LIKE` see the converted representation too. What you must check with your provider version is **whether the conversion lands on the column side or the parameter side** — `"where upper(code) = ?"`-shaped SQL kills index usage ([[What is the JPA Column annotation]] defines the column the converter writes into; the index lives there, not in the entity).

Three boundary rules keep converters sane:

- **Pure functions.** No `EntityManager` access, no caching of entity state, no lookups that depend on the current transaction — converters run inside load and flush paths where reentrancy is a landmine.
- **One type, one meaning.** `autoApply` on a widely used type (say `String`) silently rewrites every mapping of that type; reserve `autoApply` for narrow domain types (`OrderStatus`, `Email`) and leave primitives alone.
- **Storage stability.** The converter becomes the contract between Java and the schema; changing the code set is a data migration with the converter as its pivot, so version the codes like an API.

## Converter versus the alternatives

For a **single column holding a composite value** (code list, phone, coordinates), a converter is the lightest tool: no extra table, no entity ([[What is ElementCollection and how does it differ from OneToMany]] covers the case where the value set deserves its own table). For **queryable structured data** (JSON columns with path predicates), providers offer type mappings beyond the JPA minimum, and the converter is the fallback with the least query power: comparisons see the raw column, so structural predicates degrade to full scans. For **encryption**, the converter is the right interception point, with the caveat that encrypted columns can only be compared by exact value after conversion — ranges are gone.

> [!warning] `autoApply` is a global rewrite
> Declare a converter for a common type with `autoApply = true` and every mapped field of that type in every entity starts converting — including ones you never thought about. The failure mode is silent: no mapping error, just unexpected stored values. Scope `autoApply` to dedicated domain types and apply everything else explicitly with `@Convert`.

> [!tip] Interview answer
> An `AttributeConverter` is the JPA hook between one entity attribute type and one column type: `convertToDatabaseColumn` on flush, `convertToEntityAttribute` on load, applied to literals and parameters in queries so equality still matches. I use it for enums as stable business codes instead of `name()`, for value objects stored in one column, and for column-level encryption. The limits: ids, versions and relationships cannot be converted; the converter must be a pure function; and a non-trivial conversion can move the transformation to the wrong side of the comparison and cost me the index — so I check the generated SQL whenever a converter participates in a hot predicate.

See [[What is the JPA Column annotation]], [[What is the JPA Id annotation]], [[What is ElementCollection and how does it differ from OneToMany]], and [[What kinds of queries can Hibernate run]].
