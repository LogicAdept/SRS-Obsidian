<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Static #SRS

# How would you explain which Java language constructs can be marked static?

> [!abstract] Short answer
> **Marked** means you write the word `static` on the declaration (or in `import static` / `static { }`). That is legal for **class fields and methods**, **interface methods**, **member classes**, **member interfaces** (optional; they are already `static`), and **static initializers**. Nested enums, nested records, nested interfaces, and local enums/records are **`static` without writing it**. It is **illegal** on constructors, top-level types, anonymous classes, ordinary local classes/interfaces, and local variables. Semantics: [[What does the static keyword mean in Java]]. Methods: [[How would you explain static methods in Java]]. Interface methods: [[How would you explain static methods on Java interfaces]].

## Write it, imply it, or refuse it

A class modifier `static` pertains only to **member** and **local** classes, but a local or anonymous class **declaration must not contain** the token `static`. Local enum and local record classes are the implicit exception. An interface modifier `static` pertains only to **member** and **local** interfaces; you may repeat it on a member interface, not on a local interface.

`static` on a **member class** is what makes it a static nested class rather than an inner class. An inner class itself is not marked `static`, yet since Java SE 16 it may **contain** marked-`static` members.

Constructors cannot be `static` (they always run on the object being built). A method cannot be both `abstract` and `static`. Interface fields are already `public static final`; writing those modifiers is redundant, not a different kind of field. A top-level class or interface cannot be `static` (`public static class Foo` at the top of a file is illegal).

| Construct | Write `static`? |
| --- | --- |
| Field in a class | yes — class variable |
| Field in an interface | already `static` (with `public` `final`) |
| Method in a class or interface | yes — class method |
| Constructor | **no** |
| Member class | yes — not inner |
| Member interface | optional; already `static` |
| Nested enum / record | implicit; do not need the word |
| Local class / local interface | **no** (enum/record local types are implicit) |
| Anonymous class | **no** |
| Top-level class or interface | **no** |
| `static { }` initializer | yes — the keyword *is* the construct |
| `import static` | yes — import declaration |

**Static initializers and static imports use the keyword but are not modifiers on a type member in the field/method sense.** Interface `static` methods: [[How would you explain static methods on Java interfaces]].

```java
class Catalog {
    static int field;
    static void method() {}
    static { field = 1; }
    static class Member {}          // marked
    static interface I {            // marked, already static
        static void helper() {}
    }
    enum Kind { A }                 // nested enum: implicitly static
    class Inner {
        static void also() {}       // marked member of a non-static nested class
    }
}
```

**Listing 1.** Every written `static` here is a legal marking. `Kind` is `static` without the keyword. `Inner` is not marked `static`.

```d2
direction: down
q: "Can this declaration be marked static?" {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
yes: "field, method, member class,\nstatic { }, import static" {
  width: 280
  height: 56
  style.fill: "#e8f5e9"
}
redund: "member interface\n(already static)" {
  width: 220
  height: 48
  style.fill: "#e3f2fd"
}
no: "constructor, top-level type,\nanonymous, ordinary local" {
  width: 280
  height: 56
  style.fill: "#ffcdd2"
}
q -> yes
q -> redund
q -> no
```

**Fig. 1.** “Which constructs” is three buckets: you write it, it is already true, or the compiler rejects it.

> [!warning] Top-level classes are not `static`
> `static` on a class pertains to **member** (and, implicitly, some local) classes. Nested interfaces are `static` whether you write the word or not.

> [!warning] “Any nested class” is the usual over-answer
> Only a **member** class may be marked `static`. A local class in a method cannot. An anonymous class cannot. Nested `enum`/`record`/`interface` are already `static`.

> [!warning] Marking the nested type vs marking a member inside it
> `static class Nested` and `class Inner { static int x; }` are different. The second does not make `Inner` a static nested class; it still has an enclosing instance.

> [!tip] Interview answer
> You can mark fields, methods, member classes, static initializers, and static imports. Nested interfaces, enums, and records are static already. You cannot mark constructors, top-level types, or ordinary local or anonymous classes. Since Java 16 an inner class may still declare static members of its own.
