<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS

# What methods does the compiler generate for a Java record?

> [!abstract] Short answer
> From the header the compiler supplies a **`private final` field** and a **public accessor `name()`** per component, a **canonical constructor** that assigns those fields, and — unless you declare them — **`equals`**, **`hashCode`**, and **`toString`**. There is **no setter**. `equals` / `hashCode` / `toString` read the **fields**, not the accessors. The `hashCode` mixing algorithm and the exact `toString` text are **not** frozen by the spec.

## Header in, API out

```d2
direction: down
header: "record User(String name, int age)" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
fields: "private final String name\nprivate final int age" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
api: "User(String, int)\nname() / age()\nequals / hashCode / toString" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
header -> fields
fields -> api
```

**Fig. 1.** JEP 395: the header is the state description; construction, access, equality, and display are derived from it.

JLS §8.10.3–8.10.4:

| Member | Implicit if you omit it |
| --- | --- |
| Component field | `private`, `final`, non-`static`, same name and type ([[Are Java record fields final]]) |
| Accessor | `public` instance method, same name, no args, no `throws`, returns the field ([[Can you override a record accessor method]]) |
| Canonical constructor | Header-shaped; assigns each field ([[What is a canonical constructor in a Java record]]) |
| `equals(Object)` | `true` iff the argument is an instance of this record type and every **component field** is equal |
| `hashCode()` | Derived from every component field |
| `toString()` | Derived from the record name plus each component’s name and value |

```java
public record User(String name, int age) {}

User user = new User("John", 25);
user.name();
user.age();
user.equals(new User("John", 25));
user.hashCode();
user.toString(); // typically User[name=John, age=25] — do not parse this
```

**Listing 1.** No `getName()`, no `setName()`. Extra constructors and compact form are opt-in ([[What is a compact constructor in a Java record]]).

Implicit `equals` on a **reference** component is null-safe field `equals` (both null → equal). On a **primitive** it is wrapper `compare(...) == 0`, not raw `==` — that is how `float` / `double` stay consistent with `hashCode` (`NaN`, `-0.0`). `java.lang.Record`: the precise `hashCode` combination and `toString` layout are **unspecified** and may change. Dumps that insist on `Objects.hash(...)` versus a `31 * h` loop are both describing a compiler, not the language.

You may explicitly declare accessors, `equals`, `hashCode`, and `toString`. The copy-equals invariant still applies: `new R(r.c1(), …, r.cn())` must `equals` `r`. Overriding only `equals` still breaks the `hashCode` contract for maps ([[Why are Java records good HashMap keys]]). You cannot add an instance field to cache `hashCode` ([[Can a Java record declare static members and instance methods]]).

Component names cannot be `clone`, `finalize`, `getClass`, `hashCode`, `notify`, `notifyAll`, `toString`, or `wait` — those would clash with `Object` methods.

> [!warning] No setters
> Immutability here means no generated mutators and `final` component fields. A mutable object stored in a component can still change.

> [!warning] `equals` does not call `name()`
> JLS: equality, hash, and string form look at **component fields directly**. An accessor that clips or copies does not change implicit `equals`. If you declare `equals` yourself, keep `hashCode` in step.

> [!tip] Interview answer
> **The compiler turns the header into private final fields, `name()` accessors, a canonical constructor, and component-based `equals` / `hashCode` / `toString`.** There is no setter, and `getName()` is not generated. Do not quote a specific `hashCode` formula or treat `User[name=…]` as a spec; both are unspecified beyond “derived from every component.”
