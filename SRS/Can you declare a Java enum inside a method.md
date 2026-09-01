<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/Versions/16 #SRS

# Can you declare a Java enum inside a method?

> [!abstract] Short answer
> **Yes, since Java 16.** An enum may be top-level, a member of a class or interface, or a **local enum class** in a block (a method, constructor, or initializer). Older dumps that say “never inside a method” are describing pre-16 Java. A local enum is implicitly `static`: you must not write `static` on it, and it cannot capture the enclosing instance or local variables.

## Three places an enum may live

An enum declaration is a class declaration. It can appear:

1. **Top-level** — `public` or package-private (same file-name rules as a class).
2. **Member** — nested in a class or interface. Nested enums are implicitly `static`. A member enum may repeat `static` and may be `public`, `protected`, or `private`.
3. **Local** — immediately inside a block. Legal from Java 16, alongside local records and local interfaces.

Enums still cannot be declared `abstract`, `final`, `sealed`, or `non-sealed` anywhere ([[Can a Java enum extend a class]]). `strictfp` on a class is obsolete.

```d2
direction: down
top: "top-level\nenum Color" {
  width: 200
  height: 60
  style.fill: "#e3f2fd"
}
mem: "member of a class\nimplicitly static" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
loc: "inside a method (16+)\nlocal, implicitly static" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

top -> mem
mem -> loc
```

**Fig. 1.** Same enum rules in all three positions; only the nesting and modifiers change. Local enums are the Java 16 addition.

```java
class Parser {
    enum Mode { FAST, SAFE } // member; implicitly static
    static enum Also { X }   // static is redundant, legal on a member

    void parse(String raw) {
        enum Kind { JSON, XML, TEXT } // local enum — Java 16+
        Kind k = Kind.valueOf(raw);
    }
}
```

**Listing 1.** Member enum (always legal since enums existed, Java 5) and a local enum inside a method.

A local enum, like any local class or interface, cannot have `public`, `protected`, `private`, or `static`. It is not a member of the enclosing class.

## Implicitly `static` — no capturing

A local **normal** class is an inner class and may use enclosing instances and effectively final locals. A local **enum** (and a local record) is implicitly `static`, so it is not an inner class. From its body you cannot refer to enclosing type parameters, instance members, local variables, or parameters.

```java
void parse(String raw) {
    String prefix = raw.substring(0, 1);

    enum Kind { JSON, XML }

    // enum Label {
    //     A;
    //     String text() { return prefix + name(); } // compile error: captures prefix
    // }

    Kind k = Kind.JSON;
}
```

**Listing 2.** The local enum compiles; using `prefix` inside it does not. Pass data into methods as arguments instead.

```java
void m() {
    // public enum Kind { A }  // compile error: local types have no access modifier
    // static enum Kind { A }  // compile error: must not write static on a local enum
    enum Kind { A, B }
}
```

**Listing 3.** Conceptual: the implicit `static` is not something you spell on a local declaration.

> [!warning] Pre-16 interview answers say “no”
> That was true when enums were only top-level or members ([[In which Java version were enums introduced]] — the type itself is Java 5). Java 16 allowed local enum classes in the same nested-static work as local records. Saying “records can be local, enums cannot” is the outdated half of that pair.

> [!warning] Do not treat a local enum like a local inner class
> `class Local {}` inside a method can capture `this` and effectively final locals. `enum Kind { … }` in the same method cannot. Writing `static enum` to “make that obvious” is itself a compile-time error on a local declaration.

> [!tip] Interview answer
> **Yes as of Java 16 — you can declare an enum in a method; it is a local enum class and is implicitly static.** Nested enums inside a class were already legal and implicitly static. You cannot write `static` or an access modifier on the local form, and it cannot capture enclosing state. Answers that forbid method-local enums are pre-16.
