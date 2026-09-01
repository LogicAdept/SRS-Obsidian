<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS

# Can a Java record declare static members and instance methods?

> [!abstract] Short answer
> **Yes.** A record may declare static fields, static methods, static initializers, instance methods (including `private` helpers), and nested types. It may **not** declare extra instance fields, instance initializers, or `abstract` / `native` methods. Instance state is only the header components.

## What the body may contain

```d2
direction: down
header: "record Temperature(double celsius)" {
  width: 320
  height: 60
  style.fill: "#e3f2fd"
}
ok: "static fields / methods / initializers\ninstance methods, nested types" {
  width: 320
  height: 70
  style.fill: "#e8f5e9"
}
no: "no extra instance fields\nno instance initializers\nno abstract or native methods" {
  width: 300
  height: 90
  style.fill: "#ffebee"
}
header -> ok
header -> no
```

**Fig. 1.** The header is the instance state. Static members and extra instance methods are ordinary class members; extra instance fields are not.

JLS §8.10.2–8.10.3: the record body may contain constructors, members, and **static** initializers. Explicit **class** variables and class methods are permitted. Explicit **instance methods** besides accessors are permitted. A non-`static` field declaration, an instance initializer, or a method that is `abstract` or `native` is a compile-time error. Nested types are allowed; a nested record is implicitly `static`. Same list in JEP 395 and the Java SE record tutorial (`Rectangle` with `goldenRatio` / `createGoldenRectangle`).

Usual access rules apply, so `private` instance and static methods are fine. Nested records and static factories (`Temperature.ofFahrenheit`, `User.anonymous()`) are the same feature: class-level members.

```java
record Temperature(double celsius) {
    static final double ABSOLUTE_ZERO = -273.15;

    static Temperature ofFahrenheit(double f) {
        return new Temperature((f - 32) * 5.0 / 9.0);
    }

    double toFahrenheit() {
        return scale(celsius);
    }

    private static double scale(double c) {
        return c * 9.0 / 5.0 + 32;
    }
}
```

**Listing 1.** Static constant, static factory, instance method, private helper. Component `celsius` is still the only instance field.

```java
record User(String name) {
    static User anonymous() {
        return new User("anonymous");
    }

    record Id(long value) {} // nested record: implicitly static
}
```

**Listing 2.** Static factory and nested record type.

Static fields need not be `final`. The tutorial’s `static double goldenRatio` is assigned in a static initializer. That is **class** state, shared by every instance, not a per-value component.

## Static members are not part of the record value

Implicit `equals`, `hashCode`, and `toString` look at **record components** only. The canonical constructor initializes component fields from the header, not static fields. Changing a static field does not change whether two `Temperature` values compare equal. See [[What methods does the compiler generate for a Java record]] and [[Are Java record fields final]].

Instance methods you add are independent of accessors. You may still declare an explicit accessor; you may not add a second instance field to cache `hashCode`. Extra constructors remain a separate rule: [[Can a Java record declare additional constructors]]. Overriding an accessor: [[Can you override a record accessor method]].

```java
record Rectangle(double length, double width) {
    // BiFunction<Double, Double, Double> diagonal; // instance field — illegal
    // { diagonal = ... }                            // instance initializer — illegal

    static double goldenRatio;

    static {
        goldenRatio = (1 + Math.sqrt(5)) / 2;
    }
}
```

**Listing 3.** Static field plus static initializer compile; the commented instance field and instance initializer do not.

> [!warning] No extra instance field, even `private volatile` for a hash cache
> `private int hash;` or `private volatile int hash;` in the record body is still a non-`static` field declaration — compile-time error. The String-style cached-hash trick is not available. Put derived data in a method, or store it as another **header** component if it is truly part of the value.

> [!warning] `native` and `abstract` methods are also illegal
> Records are implicitly `final` and must not depend on opaque native state. `abstract` / `native` methods in the body are compile-time errors, same as extra instance fields. Instance initializers are banned for the same reason: the header alone defines instance state.

> [!tip] Interview answer
> **Yes — records can have static fields, static methods, static initializers, and extra instance methods, including private helpers and nested types.** What they cannot have is extra instance fields or instance initializers: the header is the whole instance state. Static members are class-level; they do not participate in `equals`, `hashCode`, `toString`, or the canonical constructor.
