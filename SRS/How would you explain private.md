<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #SRS

# How would you explain private?

> [!abstract] Short answer
> **`private`** means the member or constructor is accessible only from the **body of the enclosing top-level class or interface** (plus that type’s `permits` clause, and a record’s component list). Nested types in that same nest may use it. Other top-level types — even in the same package, even subclasses — may not. It is **per-instance** only in folklore: two `Box` instances may read each other’s `private` fields **inside `Box`**. Catalog: [[How do Java access modifiers work]]. Outside access: [[What happens if you try to change a private field from outside its class]]. Constructors: [[How would you explain private constructors and common patterns that use them in Java]].

## The nest, not “this object”

Accessibility is compile-time. A `private` member is not inherited. A `private` method is not overridden: a subclass may declare the same signature with no “at least as much access” rule. Top-level types cannot be `private`; only members (including member classes) can. Interface methods may be `private` (helpers with a body); interface **fields** cannot — they are implicitly `public static final`: [[How would you explain default modifiers for fields and methods inside interfaces]].

All constructors `private` (and at least one declared, so no public default constructor) prevents `new` from outside the class. Nested types in the same top-level type still can call that constructor.

```java
class Box {
    private int n;

    Box(int n) { this.n = n; }

    boolean sameSecret(Box other) {
        return this.n == other.n; // same top-level body
    }

    static class Holder {
        int peek(Box b) { return b.n; } // nested in Box
    }
}

class Neighbor {
    int peek(Box b) {
        return b.sameSecret(b);
        // return b.n; // compile-time error
    }
}

class Sub extends Box {
    Sub() { super(0); }
    int steal() {
        // return n; // compile-time error: not inherited
        return 0;
    }
}
```

**Listing 1.** `other.n` is legal in `Box`. `Neighbor` and `Sub` cannot name `n`.

```java
class ClassOnly {
    private ClassOnly() {}
    static String just = "only the lonely";
}
```

**Listing 2.** No accessible constructor for outside code, so no `new ClassOnly()`.

```d2
direction: down
top: "top-level Box body\n(+ nested types)" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
ok: "this.n  /  other.n  /  Holder" {
  width: 260
  height: 44
  style.fill: "#e8f5e9"
}
no: "Neighbor  /  Sub  /  other packages" {
  width: 280
  height: 44
  style.fill: "#ffcdd2"
}
top -> ok: "private allows"
top -> no: "compile-time error"
```

**Fig. 1.** `private` is the top-level nest. Same package is not enough; subclass is not enough.

> [!warning] `private` is not “only this instance”
> Access is by **where the code is written**, not by which object is the receiver. `this.n` and `other.n` are both fine in `Box`. The tutorial slogan “only in its own class” misses nested types sharing the nest.

> [!warning] A test class is just another top-level type
> It cannot name `private` members. That is the language rule, not a style plugin. Reflection can bypass compile-time access; it does not make those members part of the type’s contract.

> [!tip] Interview answer
> Private means the enclosing top-level type body, including its nested types. Subclasses do not inherit it, and same-package neighbors cannot see it. Two instances of that class may touch each other’s private fields inside that body. A private constructor is how you stop outside code from calling new.
