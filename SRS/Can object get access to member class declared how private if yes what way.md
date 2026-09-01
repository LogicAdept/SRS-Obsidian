<!--
reps: 0
priority: 0
-->
#Java/Language/NestedClasses #Java/Language/Modifiers/Access #Java/Language/Reflection #SRS

# Can an object access a class member declared `private`, and if so how?

> [!abstract] Short answer
> **Yes.** `private` is a **compile-time** rule about **where the source sits**, not “this object versus that object.” Code in the **top-level class or interface body** that encloses the declaration may use the member: methods of that type, **other instances** of it, and **nested types** nested in it. Outside that body, callers use a non-`private` method the class wrote, or they suppress language checks with reflection.

## The gate is the top-level class body

A `private` field, method, constructor, or member type is usable when the access occurs **inside that enclosing top-level type**. It is **not inherited**. A subclass in another top-level type cannot call `super.hidden()` or read `super.hidden` just because it extends the declaring class ([[How would you explain Java access modifiers and visibility rules]], [[How would you explain private]]).

That is why two `Account` instances can compare each other’s `balance`: the comparison is still written **in `Account`**. A `Stranger` type in the same package cannot name `a.balance` at all.

```d2
direction: down
body: "Top-level class body\n(methods, nested types)" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
ok: "private member usable" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
out: "Any other top-level type" {
  width: 240
  height: 50
}
api: "non-private method\n(getBalance)" {
  width: 260
  height: 55
  style.fill: "#e3f2fd"
}
ref: "getDeclaredField +\nsetAccessible(true)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
body -> ok
out -> api
out -> ref
```

**Fig. 1.** Language access follows the enclosing top-level type. Getters and reflection are how **other** types reach the same data.

```java
class Account {
    private int balance;

    Account(int balance) {
        this.balance = balance;
    }

    boolean sameBalance(Account other) {
        return this.balance == other.balance;
    }

    int getBalance() {
        return balance;
    }

    private class Auditor {
        int peek() {
            return balance;
        }
    }

    static class Ledger {
        int peek(Account a) {
            return a.balance;
        }
    }

    private static class Cell {
        private int n = 7;
    }

    static class Spy {
        int steal(Cell c) {
            return c.n;
        }
    }
}
```

**Listing 1.** `sameBalance` reads another instance. `Auditor` and `Ledger` sit in `Account`’s body, so they may use `private` members of `Account`. `Spy` may use `Cell.n` for the same reason. `Ledger.peek()` with no `Account` argument would not compile: a `static` nested class has **no enclosing instance**, even though `private` still allows `a.balance` when you pass one ([[How would you explain nested classes in Java and when to use each kind]], [[How do you from class get access to field outer class]]).

Access is **symmetric** across nesting: the outer type may read `private` members of its nested types, and sibling nested types may read each other’s. If two nested classes are related by `extends`, a `private` field of the superclass can still be **accessible** (same top-level type) and is still **not inherited**.

A **`private` member class** is itself only accessible inside that same top-level body. Another top-level type cannot name `Account.Auditor` or `Account.Cell`, even if it holds an `Account`. Instantiation of `Auditor` is `new Auditor()` (or `account.new Auditor()`) **in `Account`**, which also supplies the enclosing instance.

## Outside the type: methods, then reflection

`getBalance()` is a non-`private` method. The caller never names `balance`; the method body does, which is legal.

To name the field from another top-level type, reflection looks it up on the **declaring** `Class` with `getDeclaredField` (any declared access, not inherited). `getField` only finds **public** members and will not see `balance`. Then `setAccessible(true)` suppresses language checks **on that `Field` object** so `get` / `getInt` may run. Without the flag, `Field.get` throws `IllegalAccessException`. The field is still `private` in the language ([[What is the difference between getField and getDeclaredField]], [[What does setAccessible do in the Reflection API]]).

```java
import java.lang.reflect.Field;

class Peek {
    static int read(Account a) throws Exception {
        Field f = Account.class.getDeclaredField("balance");
        f.setAccessible(true);
        return f.getInt(a);
    }
}
```

**Listing 2.** Same-module and unnamed-module (typical classpath) code. A named module whose package is not **open** to the caller throws `InaccessibleObjectException` from `setAccessible(true)` (Java SE 9+); `trySetAccessible()` returns `false` instead.

> [!warning] `private` is not per-object
> “Another object cannot see my private fields” is false when that other object’s **code** is the same top-level type. `other.balance` in Listing 1 is the usual interview counterexample. A second top-level class, even a subclass, is the case that fails to compile.

> [!warning] Nested does not mean “no instance needed”
> Nested types get `private` of the enclosing type because their source is inside it. A `static` nested class still cannot use an **instance** member with no `Account` in hand. Inner classes that are not in a static context have an enclosing instance and can write `balance` or `Account.this.balance`.

> [!warning] `getField` and a closed module both look like “reflection failed”
> `getField("balance")` is `NoSuchFieldException`, not an access error. `setAccessible(true)` on JDK 17+ `java.*` internals fails unless the package is opened (`opens` / `--add-opens`). The flag also does not grant write to a non-modifiable `final` (static finals, record fields).

> [!tip] Interview answer
> **Yes — `private` means “only inside the enclosing top-level class,” not “only this instance.”** Nested classes, including static ones, can use those members; a static nested class still needs an outer **instance** to touch instance state. From a different top-level type you go through a non-private method, or `getDeclaredField` plus `setAccessible(true)`, which modules can still refuse.
