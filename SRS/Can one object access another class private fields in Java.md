<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/OOP/Encapsulation #SRS

# Can one object access another class private fields in Java?

> [!abstract] Short answer
> **No**, if that field is `private` on a **different top-level class**. Access is a compile-time property of **types**, not of objects: code in class `A` cannot read or write `b.secret` when `secret` is private in `B`. **Same class, different instance** is allowed — that is not another class. Nested types declared in the same top-level class share that body, so they **can** use each other’s private members. Access levels: [[How do Java access modifiers work]]. What `private` means: [[How would you explain private]]. Assignment from outside: [[What happens if you try to change a private field from outside its class]].

## Privacy is per top-level class, not per object

A `private` member is accessible only from within the body of the **top-level** class or interface that encloses its declaration (plus that type’s `permits` clause or record component list). Subclasses do **not** inherit private members. Same package does not help. `protected` and package access are the wider levels: [[When should you use package private visibility in Java]].

“One object” never expands the set. `foo.equals(other)` may read `other.id` when both are `Foo` because the **method body** sits in `Foo`. An object of type `Bar` still cannot name `Foo`’s private field, even if it holds a `Foo` reference.

```d2
direction: down
field: "private field of Foo" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}
same: "code in Foo\n(any Foo instance)" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
nest: "nested types in Foo" {
  width: 220
  height: 45
  style.fill: "#e8f5e9"
}
other: "other top-level class\n(subclass, same package, …)" {
  width: 260
  height: 55
  style.fill: "#ffcdd2"
}
field -> same
field -> nest
field -> other: "compile-time error"
```

**Fig. 1.** The compiler asks which **class body** contains the access, not which object is the receiver.

```java
class Account {
    private int balance;

    Account(int balance) {
        this.balance = balance;
    }

    boolean richerThan(Account other) {
        return this.balance > other.balance; // same class — legal
    }
}

class Auditor {
    boolean inspect(Account a) {
        // return a.balance > 0; // compile-time error — different top-level class
        return false;
    }
}
```

**Listing 1.** `richerThan` may use another `Account`’s `balance`. `Auditor` may not.

```java
class Account {
    private int balance;

    Account(int balance) {
        this.balance = balance;
    }

    static class Snapshot {
        final int amount;

        Snapshot(Account a) {
            this.amount = a.balance; // same top-level body — legal
        }
    }
}
```

**Listing 2.** `Snapshot` is another **class**, but it is nested in `Account`. Private access is the enclosing top-level body, not “this object only.” Nested kinds: [[How would you explain nested classes in Java and when to use each kind]].

Accessibility is determined at compile time from types and modifiers. The program does not start and then throw because of a private field access written in another top-level class — it fails to compile. Encapsulation with package access: [[How does package private visibility relate to encapsulation]].

> [!warning] “Private to the instance” is the usual wrong model
> `other.balance` inside `Account` is legal. Interview answers that say “an object can never see another object’s private fields” fail this `equals` / copy constructor case. The boundary is the class (the top-level nest), not the instance.

> [!warning] A subclass is still another top-level class
> `class PremiumAccount extends Account { int leak() { return this.balance; } }` does not compile if `balance` is private in `Account`. Use `protected` or a package-visible getter if subclasses should see the field.

> [!warning] Nested in a **different** top-level type does not count
> `Bank.Ledger` is nested, but its enclosing top-level class is `Bank`, not `Account`. Only nests inside the declaring top-level type share that private scope.

> [!tip] Interview answer
> No. Private fields of class B are not accessible from class A. Access is compile-time and is based on the enclosing top-level class, not on which object you have. Two instances of the same class may read each other’s private fields, and nested types in that same top-level class may as well. A subclass or another class in the same package still cannot.
