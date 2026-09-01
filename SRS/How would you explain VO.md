<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Immutability #Patterns/Enterprise #SRS

# How would you explain VO?

> [!abstract] Short answer
> A **Value Object** is a (usually small) object whose **equality is the values it wraps**, not **identity**. Two `Money(10, "USD")` instances are the same money. Treat them as **immutable** so aliasing cannot change “the same” value in two places. Override **`equals`/`hashCode`** (or use a **record**). Not a DTO: that is a **transfer** role ([[How would you explain DTO]]). Not an entity: entities have identity ([[How would you explain DTO Entity]]). Immutability: [[How would you explain immutable classes in Java]].

## Equality by value, not by reference

**Reference objects** (orders, users, JPA entities) are compared by **identity** (or a stable id). **Value objects** (money, a date range, a 2D point, a phone number) are compared by **their properties**. Default `Object.equals` is identity; a VO **overrides** it and **`hashCode`** to match ([[When should you override equals in Java]]; [[How would you explain override method Object.equals]]). Use `equals`, not `==`, for objects (`String` already works this way).

**Immutability.** If two references are “the same value,” mutating through one is an **aliasing bug** (`java.util.Date.setTime` on a shared date). Do not provide setters; construct a new instance to “change” a value ([[How would you explain copy constructors or defensive copying in Java]]). Platform types in `java.time` and many wrappers follow that model ([[How are immutable objects used in Java APIs]]). `List.of` documents **value-based** instances: equal instances are interchangeable; do not lock on them.

A VO is still a POJO in the ordinary-class sense ([[How would you explain the term plain old Java object POJO]]). A **record** gives private `final` components plus value `equals`/`hashCode`. Records were previewed before they were a standard class form; do not cite “Java 14” as the language release that made them always-on.

**J2EE name clash.** Some old literature used **Value Object** for what is now **Transfer Object / DTO**. If the slide is about JSON across a process boundary, they mean DTO, not this pattern.

```d2
direction: down
id: "entity / reference object\nequals by identity or id" {
  width: 300
  height: 45
  style.fill: "#e3f2fd"
}
vo: "value object\nequals by amount + currency" {
  width: 300
  height: 45
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** Same class shape, different equality rule. Context decides which you need (a postal address can be either).

```java
record Money(int amount, String currency) {
    Money plus(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException();
        }
        return new Money(amount + other.amount, currency);
    }
}

class Use {
    static boolean same(Money a, Money b) {
        return a.equals(b);
    }
}
```

**Listing 1.** Two `new Money(10, "USD")` compare equal. `plus` returns a new value; nothing is mutated.

> [!warning] Old “VO” in J2EE means DTO
> Transfer Object was sometimes labeled Value Object. A DTO may be mutable, may have no real `equals`, and exists to **move data**. A domain VO exists to **be a value**. Ask which they mean.

> [!warning] Mutable value objects alias
> `Date party = retirement; party.setDate(5)` changes retirement too. If it is a value, it must not be mutated—or you copy on every assignment. `java.awt.Point` has `equals` by coordinates **and** public mutable `x`/`y`; do not copy that mix.

> [!warning] `==` is still identity
> `new Money(1, "USD") == new Money(1, "USD")` is false. Collections use `equals`. Value-based JDK types may reuse instances; do not rely on `==` or on synchronizing on the object.

> [!tip] Interview answer
> A Value Object is equal to another when all of its defining fields are equal, not because it is the same instance. Keep it immutable and implement `equals` and `hashCode` (records do that for you). That is not a DTO, and it is not a JPA entity. Some old J2EE texts used “VO” for DTO—disambiguate.
