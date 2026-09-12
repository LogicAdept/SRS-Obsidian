<!--
reps: 0
priority: 0
-->
#Java/OOP/Encapsulation #Paradigms/OOP #Java/Language/Modifiers/Access #SRS

# What is encapsulation?

> [!abstract] Short answer
> **Encapsulation** is putting **state and the methods that maintain it in one class** and **publishing only a chosen API**. Callers depend on `call()`, not on fields or helper methods. That lets you change the implementation without changing clients. Java does it with **access modifiers**, not a keyword `encapsulate`. Design: [[How would you explain encapsulation in object oriented design]]. vs abstraction: [[What is abstraction]]; detail: [[What is the difference between abstraction and encapsulation]]. Private vs other classes: [[Can one object access another class private fields in Java]]. Principles: [[What are the main oop principles]].

## Combine, then hide

The dump’s two parts are both required: **bundle** (fields live with the methods that use them) and **hide** (those fields are not the API). A class of public fields is a bundle without hiding ([[How would you explain problems with public mutable fields in Java]]).

**Access.** `private` is the usual field default: usable in the **nest** (the top-level class and its nested types), not from another top-level class. `public` methods are the steering wheel. Package-private is a team boundary ([[How does package private visibility relate to encapsulation]]). `protected` is for subclasses—still a published contract.

**Goal.** The **binary and source contract** of the class is the public (and protected) members. You can rewrite a `private` helper, change field types, or cache, and callers of `call()` keep compiling. Returning a live internal array or a mutable `Date` undoes that ([[How would you explain copy constructors or defensive copying in Java]]). Large systems: [[What practical benefits does encapsulation bring to large systems]].

The car story in the dump is the same idea as abstraction’s “pedals vs gearbox.” Abstraction names **which operations exist**; encapsulation names **what you must not touch**. You need both: `public void call()` (abstraction of “make a call”) plus `private` line setup (encapsulation).

```d2
direction: down
api: "public call()" {
  width: 160
  height: 36
  style.fill: "#e8f5e9"
}
hid: "private line, year, company" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
api -> hid: "uses"
```

**Fig. 1.** Clients see `call`. They cannot call the private helper or assign the fields.

```java
class Phone {
    private final int year;
    private final String company;

    Phone(int year, String company) {
        this.year = year;
        this.company = company;
    }

    private void openLine() {}

    public void call() {
        openLine();
    }

    int year() {
        return year;
    }

    String company() {
        return company;
    }
}
```

**Listing 1.** `year` and `openLine` are not the API. `call` is. You can change `openLine` without touching callers of `call`.

> [!warning] `private` is nest-wide, not “this object only”
> Another instance of the same class can read `this.year` on a parameter. A nested class can too. A different top-level class cannot. Getters that return a mutable object still leak.

> [!warning] All-`private` is not the goal
> If every member is hidden, nobody can use the type. Encapsulation is **selective** publication: a small public surface, a large private interior. `public` fields are the usual failure, not “too many public methods” by itself.

> [!warning] Encapsulation is not abstraction
> Abstraction: depend on `Shape`. Encapsulation: `side` is `private`. A public-field `class Shape { public int side; }` has a type name and no encapsulation.

> [!tip] Interview answer
> Encapsulation means the class keeps its data and the code that maintains that data, and other types use only the methods you mark as the API. In Java that is `private` state plus `public` operations. The point is that you can change fields and helpers without breaking callers. It is not the same as abstraction, and it is not “make everything private.”
