<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Access #Java/OOP #SRS

# What happens if you try to change a private field from outside its class?

> [!abstract] Short answer
> **The program does not compile.** A `private` field is accessible only inside the enclosing **top-level** class body (including nested types declared there). Another top-level class — even in the same package, even a subclass — cannot read or assign that field. The compiler reports that the field is not visible; nothing is printed and no exception is thrown at run time. What `private` means: [[How would you explain private]]. The four access levels: [[How do Java access modifiers work]]. Package access is the next wider level: [[How does package private visibility relate to encapsulation]].

## Compile error, not a runtime miss

Access is checked on the **name** you write. `other.secret = 1;` from a different top-level type is a compile-time error whether you meant to read or to assign. `private` does not become visible to subclasses the way `protected` does.

**Same class, different instance is still “inside.”** Instance methods of `Box` may assign `other.n` when `other` is also a `Box`. Privacy is per **class**, not per object.

**Nested types share the top-level boundary.** A static nested class or inner class declared in `Box` may assign `Box`’s private fields. That nested type is not “outside the class” for access control. Two sibling nested types in the same top-level class may use each other’s private members as well.

```java
class Box {
    private int n = 0;
    void copyFrom(Box other) { this.n = other.n; } // legal
}

class Meddler {
    void bump(Box b) {
        // b.n = 1; // compile error — different top-level class
    }
}

class SubBox extends Box {
    void bump() {
        // n = 1; // compile error — subclass is still outside private
    }
}
```

**Listing 1.** `copyFrom` may write another instance’s private field. `Meddler` and `SubBox` may not.

```d2
direction: down
try: "assign private field" {
  width: 200
  height: 36
  style.fill: "#fff8e1"
}
in: "same top-level body\n(incl. nested types)" {
  width: 220
  height: 48
  style.fill: "#e8f5e9"
}
out: "other top-level type\n(package peer or subclass)" {
  width: 240
  height: 48
  style.fill: "#ffcdd2"
}
try -> in: "compiles"
try -> out: "compile error"
```

**Fig. 1.** “Outside its class” means outside the enclosing top-level body, not “outside this instance.”

> [!warning] It is not `IllegalAccessException` for ordinary source
> That exception belongs to **reflective** access (`Field.set` and friends) when the runtime refuses the operation. A Java assignment in another class never gets that far: the compiler rejects the field name.

> [!warning] A getter does not make the field assignable
> `b.getN()` from outside still cannot do `b.n = …`. To change the value from outside you need a method the class itself provides (or a wider access modifier). `final` is a separate lock: even inside the class you cannot reassign a `final` field after it is initialized.

> [!tip] Interview answer
> You get a compile-time error, not a runtime exception. `private` is visible only in the enclosing top-level class, including its nested types, and to every instance of that class. A subclass or another class in the same package cannot assign the field. Reflection is a different API and is not what this question is asking.
