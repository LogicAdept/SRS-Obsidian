<!--
reps: 0
priority: 0
-->
#Java/OOP #Paradigms/OOP #DataAndState/Mutability/Mutable #Java/Language/Modifiers/Access #SRS

# How would you explain problems with public mutable fields in Java?

> [!abstract] Short answer
> A **`public` non-`final` field** is part of the type’s **contract**: any code that can see the class can **read and assign** it, with **no method** in between to check invariants, copy, lock, or evolve the representation. That is the opposite of encapsulation ([[What is encapsulation]]; [[How would you explain encapsulation in object oriented design]]). `public final` on a **mutable object or array** still leaks mutation. Prefer private state and methods, or an immutable type ([[How would you explain immutable classes in Java]]). Platform example: `java.awt.Point` still has public `x` and `y`.

## The field is the API

Instance fields are variables of the class ([[How would you explain kinds of variables in Java such as local and instance]]). `public` means every client can use a field access expression, including assignment if the field is not `final`. There is no override: a subclass field with the same name **hides** the parent field; two storage locations exist. A hidden field is still reachable with `super` or a cast, so you cannot “replace” a public field with a getter later without breaking callers that assign `p.x = 1`.

**What breaks.**

- **Invariants.** Nothing stops `account.balance = -1`. A setter could reject it; a field cannot.
- **Representation.** You cannot change `int x` to a computed value, a `double`, or a packed long without a source and binary break. Methods can keep the same signature.
- **Aliasing.** `public final int[] xs` or `public final Date d` only freezes the **reference**. Callers mutate the array or date. Same bug as returning a live internal array; copy in and out ([[How would you explain copy constructors or defensive copying in Java]]).
- **Concurrency.** Unsynchronized writes to a shared public field are data races unless the field is `volatile` or you hold a lock. `final` instance fields have freeze semantics after construction; ordinary public fields do not.
- **Collections.** If `equals`/`hashCode` use those fields ([[When should you override equals in Java]]), mutating them while the object sits in a `HashSet` loses the object.

`java.awt.Point` documents public `int x` and `y` and still offers `getLocation()`, which returns a **copy**—the type kept the fields for compatibility and then tried to paper over exposure with methods. APIs that can choose, such as `java.time`, keep state private ([[How are immutable objects used in Java APIs]]). Package-private fields are a narrower leak ([[How does package private visibility relate to encapsulation]]).

```d2
direction: down
pub: "public int balance" {
  width: 200
  height: 40
  style.fill: "#ffebee"
}
any: "any client\nassign, no check" {
  width: 200
  height: 45
  style.fill: "#fff8e1"
}
priv: "private int balance" {
  width: 200
  height: 40
  style.fill: "#e8f5e9"
}
m: "deposit / withdraw\ninvariant, logging, lock" {
  width: 260
  height: 45
  style.fill: "#e3f2fd"
}
pub -> any
priv -> m
```

**Fig. 1.** A public mutable field is an assignment API. A private field is not.

```java
class Account {
    public int balance;
}

class Window {
    public final int[] size;

    Window(int w, int h) {
        this.size = new int[] { w, h };
    }
}

class Use {
    static void breakIt(Account a, Window w) {
        a.balance = -1;
        w.size[0] = 0;
    }
}
```

**Listing 1.** `balance` has no lower bound. `size` is `final` and still mutated through the array.

> [!warning] `public final` does not make a mutable type safe
> It only forbids `w.size = other`. `w.size[0] = 0` and `w.date.setTime(...)` still run. Treat public arrays, collections, and dates as published mutable state. Copy, unmodifiable wrappers, or an immutable type.

> [!warning] Fields hide; they do not override
> `Child.x` and `Parent.x` are different variables. Code compiled against `Parent` still reads `Parent.x`. You cannot intercept assignment. Replacing a field with a method is an API break for every `obj.x =` and `obj.x` use.

> [!warning] Legacy public fields are still a contract
> `Point.x` is assignable. Do not copy that style into new types. Records give private `final` components and accessors; they still must not expose a mutable component without copying.

> [!tip] Interview answer
> Public mutable fields skip encapsulation: callers can break invariants, you cannot change the representation, and there is no place to lock or validate. `public final` on an array or mutable object still lets callers change the contents. Hide fields, mutate through methods or not at all, and copy any mutable state that crosses the boundary.
