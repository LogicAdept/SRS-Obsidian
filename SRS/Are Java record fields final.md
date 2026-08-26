<!--
reps: 0
priority: 0
-->
#Java/Language/Records #Java/Immutability #SRS

# Are Java record fields final?

> [!abstract] Short answer
> **Yes.** For each header component the compiler declares a **`private final` component field**. After the canonical constructor finishes, that field cannot be reassigned. The record class itself is also implicitly `final`. Immutability is **shallow**: a mutable object held by a component can still change.

## What the language generates

```d2
direction: down
header: "record User(String name, int age)" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
field: "private final String name\nprivate final int age" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
access: "public name() / age()\nread the fields" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
header -> field: "implicit"
field -> access
```

**Fig. 1.** Header components become private final fields plus accessors — not public writable fields.

JLS §8.10.3: each record component has an implicitly declared field of the same name and type; that field is declared **`private` and `final`**. `java.lang.Record` calls a record a **shallowly immutable** carrier for a fixed set of values. Oracle’s record tutorial: fields are final because the type is meant as a simple data carrier. The record type is **implicitly `final`** (you may write `final record` redundantly on the class).

```java
public record User(String name, int age) {}

User user = new User("John", 25);
// user.name = "Jane";     // no assignable field from outside
// user.name() = "Jane";   // not an l-value
user = new User("Jane", 25); // rebind the variable — new instance
```

**Listing 1.** You cannot reassign component fields after construction; “changing” state means a new record (or mutating a nested mutable object).

## Compact constructor: normalize, do not assign fields

In a **compact** constructor you may reassign the **implicit parameters** (for validation / defensive copies). Assigning a **component field** (`this.name = …`) in that body is a compile-time error; the compiler assigns the fields after the compact body. See [[What is a compact constructor in a Java record]].

```java
public record Scores(List<Integer> values) {
    public Scores {
        values = List.copyOf(values); // parameter reassignment → then field init
    }
}
```

**Listing 2.** Defensive copy into an unmodifiable list before the generated field assignment.

## Shallow vs deep immutability

`final` freezes the **reference** (or primitive) stored in the component field. If the component type is mutable (`ArrayList`, array, legacy `Date`), callers who keep that reference can still mutate it — unless you copy / wrap in the constructor as above. That also breaks map-key contracts if the nested state changes after `put` — see [[Why are Java records good HashMap keys]] and the same shallow story as [[Are Java wrapper types immutable]].

```java
record Box(List<Integer> values) {}
Box b = new Box(new ArrayList<>(List.of(1, 2)));
b.values().add(3); // legal if the list is mutable — field still final
```

**Listing 3.** Final field, mutable contents: the record instance did not rebind `values`, but the list object changed.

> [!warning] Do not write `final` on header components
> `record Point(final int x, final int y)` is **illegal** in standardized records. `RecordComponentModifier` is annotations only; `final` was removed as a redundant header modifier. The **generated fields** are still `private final` — you just must not put `final` in the header.

> [!warning] Accessor is not a field
> Outside the record, use `name()`, not `name`. There is no public component field to assign. Interview shorthand “records have final fields” is about those **private** fields, not about writable JavaBeans properties.

> [!tip] Interview answer
> **Yes — each record component becomes a `private final` field, so the reference or primitive cannot be reassigned after construction.** The record class is implicitly final too. That is shallow immutability: wrap or copy mutable components in a compact constructor if you need a true deep freeze.
