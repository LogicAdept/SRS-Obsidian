<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# How do you create a Java enum with no instances?

> [!abstract] Short answer
> **Declare no enum constants.** The constant list is optional: `enum Empty { }` already has zero instances. If you want static members, put a **semicolon** where the constants would have been, then the members. There is still no `new`, no reflective construction, and `values()` is a zero-length array.

## Empty constant list

An enum class has no instances other than its constants ([[Can you create a Java enum instance with new]]). Omit every constant and you get a type with an empty instance set. That is legal; it is just unusual — most enums are a non-empty fixed set.

```d2
direction: down
body: "enum E { … }" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
zero: "{ }  or  { ; members }\nzero constants" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
one: "{ INSTANCE; }\nsingleton" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}

body -> zero
body -> one
```

**Fig. 1.** Zero constants vs one constant are different answers. Empty is not a singleton ([[How does an enum provide a Singleton]]).

```java
enum Empty { }

enum Holder {
    ; // empty constant list, then members

    static int sizeOf(String s) {
        return s.length();
    }
}

// Empty.values().length == 0
// Empty.valueOf("X") throws IllegalArgumentException
// new Empty() does not compile
```

**Listing 1.** `Empty` is a type with no constants. `Holder` is the utility-holder shape: semicolon, then static API. Both have zero instances.

The semicolon is **not** what creates emptiness. `EnumBodyDeclarations` starts with `;`, so you need that token before fields and methods. With no members, `{ }` is enough.

```java
enum Broken {
    static int n = 1; // compile error: members must follow `;` after the (empty) constant list
}
```

**Listing 2.** Conceptual: the leading semicolon is a separator, not a “no instances” keyword.

You still cannot add instances later ([[Can you add constants to a Java enum at runtime]]). An empty enum cannot declare `abstract` methods — that rule requires at least one constant with a class body ([[Can a Java enum have abstract methods]]). Constructors may exist but have nothing to construct ([[Can you declare a constructor inside a Java enum]]).

People sometimes pick this over a class with a private constructor because the language already forbids `new` and `Constructor.newInstance` on enums. A private-constructor utility class is still the usual style for static helpers; the empty enum is the “the JVM will not give you an instance” variant of the same idea.

> [!warning] Empty enum ≠ singleton enum
> `enum Unit { INSTANCE }` has **one** instance. `enum Empty { }` has **none**. Interviewers who ask for a singleton enum want a single named constant, not an empty body.

> [!warning] The semicolon is only required before members
> Dumps say “the semicolon makes it have no instances.” `enum E { }` already has none. The `;` is required once you write fields or methods after an empty (or non-empty) constant list.

> [!tip] Interview answer
> **Leave the constant list empty — `enum E { }` has zero instances.** If the type also holds static members, write `enum E { ; static … }`. `values()` is empty, `valueOf` always fails, and you still cannot `new` it. That is a utility holder, not a singleton.
