<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

> [!abstract] Short answer
> **Use a sealed class or interface when you need a fixed set of *kinds*, not a fixed set of *instances*.** An `enum` is a closed list of singletons. A `sealed` type is a closed list of permitted subtypes — each subtype can have its own fields, constructors, and many objects. Keep the enum when the domain is named constants (`PENDING`, `ACTIVE`) that `EnumSet` / `==` / `ordinal()` can treat as one universe.

## Fixed values vs fixed kinds

An enum class models “this type has only these instances” ([[How would you explain Java enum types]]). That is why `Planet.EARTH` is unique, why `switch` on an enum needs no `default` when every constant is listed, and why `EnumSet` exists ([[What special collections exist for Java enums]]).

Sometimes the domain is “there are only these *kinds* of value,” and each kind is a real class with its own state. `OrderPlaced` has an id and a time; `OrderCancelled` has a reason; you will construct many of each. That is not an enum: enum constants all share the same fields, each name is one object, and you cannot `new` another ([[Can you create a Java enum instance with new]]). JEP 409’s split is exactly that: enums for a fixed set of values; sealed types for a fixed set of kinds.

A sealed hierarchy also does what an enum cannot as a *class*: it may extend another class, put permitted subtypes in other compilation units of the same module, and give each alternative a name you can use in APIs ([[Can a Java enum extend a class]]). Constant-specific bodies on an enum are anonymous subclasses; they are not types you declare in `permits`. Abstract methods on an enum still live on one enum type ([[Can a Java enum have abstract methods]]).

Both shapes can be switched exhaustively: enum *constant* labels since Java 5; sealed *type* patterns from pattern-matching `switch` (Java 21) ([[Can you use a Java enum in a switch]], [[How would you explain Sealed classes]]). Sealed types are a Java 17 language feature.

```d2
direction: down
en: "enum Status { PENDING, ACTIVE }\nfixed instances, same shape" {
  width: 340
  height: 70
  style.fill: "#e3f2fd"
}
se: "sealed interface Event permits …\nfixed kinds, each a class, many instances" {
  width: 380
  height: 70
  style.fill: "#e8f5e9"
}

en -> se: "need different data per kind"
```

**Fig. 1.** Same “closed set” idea. Enums close the instance list. Sealed types close the subtype list.

```java
enum Status { PENDING, ACTIVE, CLOSED }

sealed interface Event permits OrderPlaced, OrderCancelled {}

record OrderPlaced(String orderId) implements Event {}
record OrderCancelled(String orderId, String reason) implements Event {}

class Demo {
    static String describe(Event e) {
        return switch (e) {
            case OrderPlaced p -> p.orderId();
            case OrderCancelled c -> c.reason();
        };
    }
}
```

**Listing 1.** `Status` is three singletons. `Event` is two kinds; each `record` can be instantiated freely.

> [!warning] Do not seal a hierarchy that should have been an enum
> If every alternative is a nameless singleton with the same fields, `enum` gives `name()`, `valueOf`, `EnumSet`, and identity `==`. A sealed interface of empty records is a heavier enum without those tools.

> [!warning] Constant-specific class bodies are not a sealed domain model
> `PENDING { … }` is still one `Status` instance. You cannot pass “the PENDING type” around, give it different constructors, or put it in another file. When the cases must be types, use `permits`.

> [!tip] Interview answer
> **Prefer `enum` for a fixed set of instances; prefer `sealed` for a fixed set of kinds whose subtypes carry different state and many objects.** Enums cannot extend another class and cannot grow extra instances. Sealed types (Java 17) close the subtype list with `permits` and pair with exhaustive pattern `switch`. Do not replace `PENDING`/`ACTIVE` with sealed empty types just to look modern.
