<!--
reps: 0
priority: 0
-->
#Methodologies/DDD #SRS

# What is a value object and why should you use one?

> [!abstract] Short answer
> A value object is an immutable object with no identity: it is defined entirely by its attribute values, two instances with equal values are interchangeable, and any "change" produces a new instance. You use them to stop stringly-typed code - `Money`, `Email`, `DateRange` instead of `String`, `String`, `LocalDate` pairs - and to get three free properties: equality that just works, thread safety, and validation that runs once at construction. In DDD they are one of the four tactical building blocks alongside entities, aggregates, and domain services.

## Mechanism: identity-free and immutable

An entity is "which one", a value object is "what value". That single distinction drives the implementation: no `id` field, `equals`/`hashCode` over all attributes, final fields, no setters, and every operation returns a fresh instance. Java 16+ records make the boilerplate nearly free - the record already gives value-based equality and immutability for its components. Validation moves into the constructor, so an invalid value object simply cannot exist; the type system then guarantees every downstream method receives a valid value. This is the structural cure for primitive obsession.

```java
public record Money(long amountMinor, Currency currency) {
    public Money {
        if (amountMinor < 0) throw new IllegalArgumentException("negative amount");
        Objects.requireNonNull(currency);
    }
    public Money add(Money other) {
        if (!currency.equals(other.currency))
            throw new IllegalArgumentException("currency mismatch");
        return new Money(amountMinor + other.amountMinor, currency);
    }
    public Money scale(int percent) {
        return new Money(Math.round(amountMinor * percent / 100.0), currency);
    }
}
```

**Listing 1.** Conceptual. `add` and `scale` never mutate - they return new `Money`. Two `Money(1250, EUR)` values are equal wherever they live, and an amount below zero is unrepresentable.

## Why teams adopt them

Three concrete payoffs. Immutability makes value objects safely shareable across threads and caches - no defensive copies needed ([[How would you explain immutable objects and why they matter]]). Value equality removes the "compare by id" ceremony: a returned `Address` equals the stored one because values match, which also feeds correct `equals`/`hashCode` behavior up the object graph ([[What is the Object equals contract]]). And domain vocabulary improves: a `DateRange` can enforce `start <= end` in one place, instead of every calendar method re-checking two loose `LocalDate`s. Entities can also hold value objects for their measurable parts while keeping identity for themselves, which is the standard split in DDD models ([[What are aggregate aggregate root entity and value object in DDD]]).

> [!warning] "A value object is a small helper class" undersells it
> The discipline is in the contract: no identity, full immutability, value equality, self-validation. A class with a getter/setter pair and a `value` field is a value object only if mutations are impossible and equality is structural. The other common lie: "records are automatically value objects" - a record holding a mutable `List` is as broken as a mutable POJO; shallow immutability is not immutability ([[How would you explain immutable classes in Java]]). And a value object is not a DTO: DTOs exist to cross wire boundaries and may be mutable bags; value objects enforce domain rules. The decision between the two identities - and when a concept should switch sides - is [[What is the difference between an entity and a value object]].

> [!tip] Interview answer
> A value object is an identity-free, immutable type compared by its values - think Money or DateRange. I use them to kill primitive obsession: validation happens once in the constructor, equality is structural, instances are thread-safe, and every operation returns a new value. Records give me most of the mechanics for free, and the domain reads like the business instead of like Strings.
