<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS

# Can you override a record accessor method?

> [!abstract] Short answer
> **Yes, in the record’s own body** — you **explicitly declare** the accessor that would otherwise be generated. It must be a `public` instance method, same name as the component, same return type, no parameters, not generic, no `throws`. You cannot change that signature. You cannot override it in a subclass: the record class is implicitly `final`. Explicit accessors were allowed from the first preview (JDK 14), not only from Java 16.

## Explicit accessor, not a subclass override

```d2
direction: down
header: "record User(String name)" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
implicit: "implicit public String name()\nreturns the component field" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
explicit: "optional explicit name()\nsame signature, your body" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
header -> implicit: "if omitted"
header -> explicit: "if declared"
```

**Fig. 1.** “Override the accessor” means replace the implicit method in this record. There is no subclass to override in.

JLS §8.10.3: for each component there is an accessor, declared **explicitly or implicitly**. If you declare it, the return type must match the component, the method must not be generic, and it must be a `public` instance method with no formal parameters and no `throws` clause. `java.lang.Record`: if you omit it, the implicit body returns the component field.

`@Override` is legal on that method even though it does not override a superclass method. JLS §9.6.4.4: in a record, `@Override` may mark an accessor for a record component (so renaming the component without updating the method is a compile error). That `@Override` meaning was added in the second preview; **declaring** the accessor itself was already in JEP 359.

Records are implicitly `final`, so a subtype cannot override `name()`. See [[What methods does the compiler generate for a Java record]] and [[Are Java record fields final]].

```java
public record Point(int x, int y) {
    // public String x() { return String.valueOf(x); } // wrong return type

    @Override
    public int x() {
        return x;
    }
}
```

**Listing 1.** Same signature is required. A different return type is not an accessor and does not compile.

```java
record Rectangle(double length, double width) {
    @Override
    public double length() {
        System.out.println("Length is " + length);
        return length;
    }
}
```

**Listing 2.** Explicit accessor with extra behavior, still returning the component. Same shape as the Java SE tutorial.

## Keep the copy-equals invariant

`Record` requires: if `R copy = new R(r.c1(), r.c2(), …)`, then `r.equals(copy)`. JLS: implicit `equals` / `hashCode` / `toString` read **component fields**, not accessors. An accessor that returns a different value than the field (clip, `toUpperCase()`, a live mutable view) compiles, but a round-trip through accessors and the canonical constructor can yield a value that is not `equals` to the original. JLS’s `SmallPoint` example is that failure.

`java.lang.Record` lists the good reasons to declare an accessor (or the canonical constructor): validate arguments, **defensive copies** of mutable components, or normalize a group of components. Logging is legal; inventing a second representation in the accessor is not. Compact constructors are usually where you normalize stored state: [[What is a compact constructor in a Java record]].

```java
public record User(String name) {
    public String name() {
        return name.toUpperCase(); // compiles; stored field is unchanged
    }
}

User u = new User("Ada");
User copy = new User(u.name());
boolean same = u.equals(copy); // false — "Ada" vs "ADA"
```

**Listing 3.** Same-signature accessor is allowed. Returning a transformed value breaks the copy-equals invariant unless the field already holds that value.

> [!warning] Same signature, including `public` and no `throws`
> You cannot make the accessor `private`, add parameters, change the type, make it generic, or declare `throws`. Those declarations are not accessors; they collide with the mandated method or fail §8.10.3.

> [!warning] `equals` does not call your accessor
> Implicit `equals` / `hashCode` compare the **fields**. A “pretty” accessor that clips or uppercases is the JLS bad-style case: two records with the same fields compare equal, then copying via accessors produces a different record. Prefer a defensive copy that still represents the stored component, or normalize in the constructor so field and accessor agree.

> [!tip] Interview answer
> **Yes — you can explicitly declare a component accessor, but it must stay a public no-arg method with the component’s type; that is not subclass overriding, because records are final.** Changing the return type does not compile. Keep `r.equals(new R(r.c1(), …))`; a typical sound reason is a defensive copy of a mutable component.
