<!--
reps: 0
priority: 0
-->
#Java/Language/Records/Constructors #SRS

# What is a canonical constructor in a Java record?

> [!abstract] Short answer
> It is the **one constructor whose parameter types match the record header**, in header order. Every record has exactly one, declared **explicitly** (normal or compact) or **implicitly**. That constructor is the only one allowed to initialize the `private final` component fields. Extra constructors may exist, but they must start with `this(...)` and eventually reach this one.

## Header-shaped constructor; two explicit spellings

```d2
direction: down
header: "record Range(int min, int max)" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
canon: "canonical constructor\nRange(int min, int max)" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
fields: "this.min = min\nthis.max = max" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
header -> canon: "same names and types"
canon -> fields
```

**Fig. 1.** No default `Range()` unless you write a non-canonical overload that delegates. The implicit constructor *is* the header-shaped one.

JLS §8.10.4: a record does not get an implicit no-arg constructor. It has a canonical constructor that initializes all component fields. You declare it in one of two ways:

1. A **normal** constructor whose signature is override-equivalent to the derived header signature — same parameter **names** and **types**, not generic, **no `throws`**, **no `this(...)` / `super(...)`**. You assign `this.min = min` yourself.
2. A **compact** constructor — `Range { … }` with no parameter list. Parameters are implicit. You must **not** assign component fields; after the body the compiler does `this.min = min; this.max = max`. See [[What is a compact constructor in a Java record]].

It is a compile-time error to declare **both** a compact constructor and a normal header-matching constructor. There is only one canonical constructor.

```java
record Rectangle(double length, double width) {
    public Rectangle(double length, double width) {
        if (length <= 0 || width <= 0)
            throw new IllegalArgumentException(
                String.format("Invalid dimensions: %f, %f", length, width));
        this.length = length;
        this.width = width;
    }
}
```

**Listing 1.** Explicit normal canonical constructor (Java SE records tutorial `Rectangle`). Parameter names must match the components. Unchecked validation is fine; a `throws` clause is not.

```java
record Rectangle(double length, double width) {
    public Rectangle {
        if (length <= 0 || width <= 0)
            throw new IllegalArgumentException(
                String.format("Invalid dimensions: %f, %f", length, width));
    }
}
```

**Listing 2.** Same canonical constructor in compact form. Equivalent to Listing 1 plus the trailing field assignments.

If you declare neither, the compiler emits a canonical constructor with the same access as the record, no `throws`, and a body that only assigns each component field from the corresponding parameter.

An explicitly declared canonical constructor must be **at least as accessible** as the record: a `public` record’s canonical constructor **must be `public`**. That is why a public record cannot hide construction behind a private canonical constructor ([[How do you implement Singleton with a Java record]]).

Non-canonical constructors: [[Can a Java record declare additional constructors]]. Serialization always reconstitutes a record by calling this constructor ([[How does Java serialization treat record classes]]).

> [!warning] One canonical form
> Compact and full-parameter canonical constructors are two spellings of the **same** constructor. Writing both is a compile-time error. You may combine **one** of those with extra `this(...)` overloads.

> [!warning] No `throws` on the canonical constructor
> Implicit and explicit (non-compact) canonical constructors must not declare `throws`. A compact constructor has no `throws` clause either. Checked exceptions in validation must be wrapped (typically `IllegalArgumentException`) or avoided. `RuntimeException` is the usual validation type.

> [!tip] Interview answer
> **The canonical constructor is the header-shaped one — same parameter names and types as the components — and it is the only constructor that initializes the record’s fields.** You get it for free, or you write it as a normal constructor or as a compact `Name { … }` body. Extra constructors must `this(...)` into that path; you cannot declare two canonical forms.
