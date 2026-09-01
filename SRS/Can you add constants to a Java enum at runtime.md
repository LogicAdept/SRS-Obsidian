<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS

# Can you add constants to a Java enum at runtime?

> [!abstract] Short answer
> **No.** An enum class has no instances other than the constants written in its declaration. A running program cannot `new` extra ones, subclass the enum to add names, clone a constant, or construct one by reflection. Adding a constant means **changing the source (or shipping a new class file)** — that is library evolution, not a mutation of a type already loaded.

## The instance set is closed

Each enum constant is an implicit `public static final` field, created when the enum class initializes. `values()` and `valueOf(String)` see exactly those constants, in source order ([[How do you iterate over all Java enum constants]]).

The language then blocks every way of making another instance:

- `new Color()` does not compile — a class-instance creation may not name an enum class ([[Can you create a Java enum instance with new]]).
- You cannot write `enum More extends Color` ([[Can a Java enum extend a class]]). Without constant class bodies the enum is implicitly `final`; with them it is implicitly `sealed` and the only subclasses are those anonymous constant bodies — they do not add names to `values()`.
- `Enum.clone` is `final` and throws `CloneNotSupportedException`.
- `Constructor.newInstance` throws `IllegalArgumentException` when the constructor belongs to an enum class.
- Deserialization reuses the declared constant; it does not materialize a duplicate ([[How does Java serialization treat enum constants]]).

```d2
direction: down
src: "enum Color { RED, GREEN }\n(source / class file)" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
jvm: "Loaded Color\nexactly two instances" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
blocked: "new / subclass / clone / reflection" {
  width: 280
  height: 70
  style.fill: "#ffcdd2"
}
set: "EnumSet.add(Color.RED)\nsubset of existing names" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}

src -> jvm
jvm -> blocked
jvm -> set
```

**Fig. 1.** The constant list is a property of the loaded class. `EnumSet` only selects among names that already exist.

```java
enum Color { RED, GREEN }

// new Color();                      // compile error: not a legal class to instantiate
// enum Extra extends Color { BLUE } // compile error: enum declarations have no extends clause
// Color.values() -> { RED, GREEN }  // no API to append BLUE
```

**Listing 1.** The type offers no operation that grows the constant set after the class is loaded.

An extra `static` field is not a constant either: only names in the constant list become implicit constants and appear in `values()`.

```java
enum Color {
    RED, GREEN;
    public static final Color ALIAS = RED; // another field, not a third constant
}
// Color.values() is still { RED, GREEN }
// Color.valueOf("ALIAS") throws IllegalArgumentException
```

**Listing 2.** Aliases and helpers in the enum body do not enlarge the enum.

## Not the same as `EnumSet.add`

`java.util.EnumSet` is a set whose elements must all come from **one already-declared** enum type ([[What is EnumSet]]). `add` inserts an existing constant into that set; it does not declare a new constant.

```java
enum Color { RED, GREEN }

class Demo {
    void select() {
        java.util.EnumSet<Color> on = java.util.EnumSet.noneOf(Color.class);
        on.add(Color.RED);   // legal: RED already exists
        on.add(Color.GREEN); // legal
        // there is no Color.BLUE to add
    }
}
```

**Listing 3.** Changing which constants are *selected* is not changing which constants *exist*.

## Shipping a new constant is a new class version

If you edit the enum, recompile, and replace the class file, adding or reordering constants is a **binary-compatible** change: old callers still link. Deleting a constant removes a public field and is not recommended for widely distributed types. An exhaustive `switch` compiled against the old constant list may fail at run time if it meets a constant it was not compiled with. That is version skew between binaries — still not “add BLUE while this `Color` class is already loaded.”

> [!warning] `EnumSet.add` does not add an enum constant
> `on.add(Color.RED)` mutates a collection of existing constants. Interview answers that say “you can add to an enum” after using `EnumSet` are talking about the set, not the type. [[Does EnumSet allow null]] is a separate restriction on that collection.

> [!warning] Binary compatibility is not a runtime `add`
> “Adding an enum constant is binary compatible” means a **new** `Color.class` with an extra name still links with old code. It does not mean `Color` grows constants inside one running JVM. Reflection cannot fill that gap: enum constructors are rejected by `Constructor.newInstance`.

> [!tip] Interview answer
> **No — the constants are exactly those in the enum declaration, and the language plus `Enum` block every way to create another instance.** You cannot `new`, subclass, clone, or reflect extra constants. `EnumSet.add` only stores constants that already exist. Extra names belong in a new version of the class, not in a running program.
