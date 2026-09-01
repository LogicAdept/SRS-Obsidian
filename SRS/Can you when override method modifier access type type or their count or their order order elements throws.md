<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/Exceptions/Checked #Java/OOP/Polymorphism #SRS

# Can you when override method modifier access type type or their count or their order order elements throws?

> [!abstract] Short answer
> **Override keeps the signature.** You may **widen** access, **narrow** a **reference** return type, **rename** parameters, **drop or narrow checked `throws`**, and **reorder `throws` types**. You may **not** narrow access, widen a reference return, change primitive/`void` returns, or add a new checked exception that is not a subtype of one already thrown. Change parameter **types, count, or order of types** and it is **overloading**, not overriding. Access: [[Can you use a weaker access modifier when overriding a method]]. Return type: [[Can you declare a narrower return type when overriding a method]]. `throws`: [[How do checked exceptions work with method overriding]].

## Signature vs everything else

Two methods override when they have the same name, the same type parameters, and the same formal **parameter types** (override-equivalent signatures). Parameter **names** are not in the signature. Return type, access, and `throws` are separate override checks, not part of the signature. Overload vs override: [[How would you explain Overload vs Override]]. Overriding: [[How would you explain method overriding in Java]].

| What you change | Still an override? | Rule |
| --- | --- | --- |
| Access | yes, if not narrower | at least as much access; `public` stays `public` |
| Return type | yes, if substitutable | reference **subtype** (Java 5+); primitive identical; `void`/`void` |
| Parameter **names** | yes | not in the signature |
| Parameter **types, count, or type order** | **no** — that is overload | different signature |
| `throws` types | yes, if not more checked | no extra checked exceptions; subtypes and unchecked OK |
| Order of `throws` names | yes | the clause is a set of types |

A `Super` variable must still be able to invoke the method. Narrower access would make `Super s = new Sub(); s.m();` illegal at the call site that compiled against `Super`. Broader checked `throws` on `Sub.m()` would force callers who only know `Super` to miss a checked exception. Broader checked `throws`: [[What happens if an override declares a broader checked exception than the parent]].

```d2
direction: down
sig: "name + parameter types\n(the signature)" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
keep: "same signature → override\nthen check access, return, throws" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
ovl: "different types/count/order\n→ overload, not override" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
sig -> keep
sig -> ovl
```

**Fig. 1.** The compiler does not “guess which parent method you meant.” Either the signatures are override-equivalent, or you overloaded.

```java
class Animal {}
class Dog extends Animal {}

class Base {
    protected Animal find(String key) throws java.io.IOException {
        return new Animal();
    }
}

class Sub extends Base {
    @Override
    public Dog find(String id) throws java.io.FileNotFoundException {
        return new Dog();
    }
}
```

**Listing 1.** Still an override: wider access (`protected` → `public`), covariant return (`Animal` → `Dog`), renamed parameter (`key` → `id`), narrower checked `throws` (`FileNotFoundException` is an `IOException`).

```java
class Base {
    Animal find(String key) throws java.io.IOException {
        return new Animal();
    }
}

class Other extends Base {
    Animal find(int key) { return new Animal(); }           // overload — int vs String
    Animal find(String key, String extra) { return new Animal(); } // overload — count
    Animal find(Object key) { return new Animal(); }        // overload — type
}
```

**Listing 2.** Different parameter types or count: new methods, no `@Override`. `Other` still inherits `find(String)`.

```java
// Conceptual: does not compile as overrides
class Base {
    public Animal find(String key) throws java.io.IOException {
        return new Animal();
    }
}

class Bad extends Base {
    @Override
    protected Animal find(String key) throws java.io.IOException { // narrower access
        return new Animal();
    }

    @Override
    Animal find(String key) throws Exception { // broader checked throws
        return new Animal();
    }
}
```

**Listing 3.** Conceptual. Weaker access and extra checked exceptions (`Exception` is not a subtype of `IOException` in the “already thrown” direction) are compile-time errors. Unchecked `RuntimeException` in `throws` is allowed. `throws` as a clause: [[How would you explain the throws clause for checked exceptions]]. Checked vs unchecked: [[What is the difference between checked and unchecked exceptions]].

Omitting `throws` on the override is legal. Callers who use the **subclass** type then need not handle the parent’s checked exceptions. Callers who use the **superclass** type still see the parent `throws`. The parent clause is not “copied onto” the child.

> [!warning] Reordering `int, String` is a new signature
> `m(int, String)` and `m(String, int)` overload. Reordering `throws IOException, SQLException` does not. Parameter **names** `m(String a)` vs `m(String b)` still override.

> [!warning] “You can add exceptions if they are subclasses” applies to **checked** types already on the parent
> You may throw `FileNotFoundException` when the parent throws `IOException`. You may **not** add `SQLException` if the parent never mentioned it or a supertype of it. `RuntimeException` and `Error` are not checked, so they do not count as “more checked exceptions.”

> [!warning] `@Override` fails when you accidentally overloaded
> Changing a parameter type looks like an override in a review and is an overload at compile time. Put `@Override` on every intended override so that mistake is a compile-time error.

> [!tip] Interview answer
> When overriding, keep the same name and parameter types. You may widen access, use a narrower reference return type, rename parameters, and drop or narrow checked throws — order in throws does not matter. Change parameter types, count, or type order and you overloaded instead. You cannot narrow access or add a new kind of checked exception.
