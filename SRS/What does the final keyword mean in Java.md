<!--
reps: 0
priority: 0
-->
#Java/Language/Modifiers/Final #SRS

# What does the final keyword mean in Java?

> [!abstract] Short answer
> **`final` means “no more of this kind of change.”** On a **class** (or record): no subclasses. On a **method**: subclasses cannot override or hide it. On a **variable**: assigned **at most once** — after that the variable always denotes the same value (or the same object; the object’s state may still change). Constructors cannot be `final`. Locals that *could* be `final` without writing it are **effectively final**: [[How would you explain effectively final]]. When to write it: [[What are use cases for the final keyword in Java]]. Constant variables: [[What is a compile-time constant in Java]]. Immutability is more than `final`: [[How would you explain immutability and its benefits in Java]].

## Three places, three “no”s

| On this declaration | `final` forbids |
| --- | --- |
| Class | any subclass |
| Instance method | an override in a subclass |
| `static` method | a hiding method of the same signature |
| Field / parameter / local | a later assignment to that name |

A class is `final` when its definition is complete and no subclasses are desired. It cannot also be `abstract`. Methods of a `final` class are never overridden. Records are implicitly `final`; an enum is implicitly `final` or implicitly `sealed`. You cannot write `abstract`/`final`/`sealed`/`non-sealed` on an enum declaration.

A method is `final` to forbid overriding and hiding. A `private` method, and every method declared in a `final` class, **behaves as if** `final`. Interface methods cannot be `final`: [[Why can an interface method not be declared final in Java]]. `final` on a `static` method blocks **hiding**: [[How would you explain the final modifier on a static method in Java]].

A `final` variable (local, parameter, or field) may be assigned only when it is definitely unassigned. Blank `final` **class** fields must be assigned by a static initializer; blank `final` **instance** fields must be definitely assigned (and not definitely unassigned) at the end of **every** constructor. Constructors themselves cannot be `final`. `final` cannot be combined with `volatile`. Interface fields are already implicitly `final`. Record component fields are `private final`: [[Are Java record fields final]].

A **constant variable** is a narrower thing: `final` primitive or `String`, initialized in the **declaration** with a constant expression. A blank `final` filled in a constructor is not a compile-time constant.

```java
final class Unit {
    static final int ZERO = 0;          // constant variable
    final String id;                    // blank instance final
    final int[] cells = { 1, 2 };       // final reference; array still mutable

    Unit(String id) {
        this.id = id;
    }

    final int size() {
        return cells.length;
    }
}
```

**Listing 1.** `Unit` cannot be extended; `size` cannot be overridden; `id` is assigned once per construction; `cells[0] = 9` is still legal.

```java
class Demo {
    void once(final int n) {
        int y = n;
        // n++;  // illegal: parameter is final
        y++;     // y is not final (and not effectively final after this)
    }
}
```

**Listing 2.** Parameters and locals use the same “assign at most once” rule. `++` is an assignment.

```d2
direction: down
kw: "final" {
  width: 120
  height: 36
  style.fill: "#fff8e1"
}
cls: "class → no subclasses" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
m: "method → no override/hide" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
v: "variable → assign once" {
  width: 220
  height: 40
  style.fill: "#f3e5f5"
}
obj: "referent may still mutate" {
  width: 240
  height: 40
  style.fill: "#ffcdd2"
}
kw -> cls
kw -> m
kw -> v -> obj
```

**Fig. 1.** The keyword always forbids a further change of **that** declaration. It does not freeze heap state.

> [!warning] `final` is not `immutable`
> `final Point p` always refers to that `Point`; `p.x = 1` can still run if `x` is not `final`. Arrays and collections held by a `final` field are the usual leak. Do not confuse this with `finally` or `finalize`.

> [!warning] Blank `final` is not a constant variable
> `static final int N;` assigned in a static block cannot be used where a constant expression is required (annotation values, `case` labels, compile-time folding). Effectively final locals are also not constant variables.

> [!tip] Interview answer
> Final on a class bans subclasses, on a method bans override or hiding, on a variable bans a second assignment. A final reference can still point at a mutable object. If you never reassign a local, it is effectively final even without the keyword, which is what lambdas need.
