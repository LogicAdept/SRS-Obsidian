<!--
reps: 0
priority: 0
-->
#Java/OOP #Java/Language/NestedClasses #Java/Lambdas #SRS

# How would you explain nested classes in Java and when to use each kind?

> [!abstract] Short answer
> **A nested class is any class declared in the body of another class or interface** — member, local, or anonymous. Use a **member** class for a helper that several methods (or other types) must name; **inner** if it needs the enclosing instance, **`static` nested** if it does not. Use a **local** class when that helper lives in one block and needs a constructor, extra methods, or several instances. Use **anonymous** for a single instance with extra fields or methods; use a **lambda** for a single abstract method with no extra state.

## Nested is the umbrella

A **top-level** class sits in a compilation unit. **Nested** means the declaration occurs inside another type. That splits into a **member** class (in the class body), a **local** class (in a block), or an **anonymous** class (`new Type() { }` or an enum constant body). **Inner** means nested and not (explicitly or implicitly) `static` ([[How would you explain categories of Java classes such as nested and anonymous]]).

Why nest at all: the helper is used in one place, it can see `private` members of the enclosing type ([[How can a nested class access fields of its enclosing class]]), and the code sits next to the use.

```d2
direction: down
need: "Need a type next to its only client?" {
  width: 280
  height: 50
}
member: "Several methods / other types\nmust name it" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
inner: "Needs enclosing instance\n→ inner member" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
st: "No enclosing instance\n→ static nested" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
block: "Only this block, may capture locals" {
  width: 300
  height: 50
  style.fill: "#fff3e0"
}
local: "Name, ctor, extra methods,\nmore than one instance" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
anon: "One instance; extra fields\nor methods" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}
lam: "SAM, no extra state\n→ lambda" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
need -> member
member -> inner
member -> st
need -> block
block -> local
block -> anon
block -> lam
```

**Fig. 1.** Placement first (member vs this block), then inner vs `static`, then named local vs anonymous vs lambda.

## When to pick which

**Static nested member** — same needs as a small top-level class, but it belongs next to `Outer` and may be `private`. You do **not** want an implicit enclosing instance. Instance fields of `Outer` are still reachable as `o.field`, including `private` ones; you just pass `o` ([[How would you explain static nested classes in Java]], [[How do you from class get access to field outer class]]).

**Inner member** — several places in `Outer` (or a caller with an `Outer`) must construct it, and it should read **non-public instance** state as `n` or `Outer.this.n`. Each inner instance is tied to one enclosing instance (`outer.new Inner()`).

**Local class** — the type is needed only in **one block**, you need a **name**, a **constructor**, **extra methods**, or **more than one instance**, and you may capture **effectively final** locals ([[How would you explain local classes in Java and their scoping rules]]). If you would have written a member class except you also need those locals, stay local.

**Anonymous class** — you would have written a local class **once**, and you need **fields or extra methods** the supertype does not have (or a one-site override of several methods). No explicit constructor ([[What are anonymous classes and where are they used]]).

**Lambda** — you are passing **one unit of behavior** (per-element action, completion, error). You need a simple instance of a **functional interface** and none of the above (no constructor, no named type, no extra fields or methods) ([[How would you explain lambda expressions in Java]]).

```java
class Ledger {
    private int total;

    static class Sum {
        static int of(int a, int b) {
            return a + b;
        }
    }

    class Line {
        private final int amount;

        Line(int amount) {
            this.amount = amount;
        }

        int remaining() {
            return total - amount;
        }
    }

    void once(int extra, java.util.List<String> names) {
        class Counter {
            private int c;

            Counter(int start) {
                c = start + extra;
            }

            int next() {
                return ++c;
            }
        }
        Counter a = new Counter(0);
        Counter b = new Counter(10);
        a.next();
        b.next();

        names.sort(new java.util.Comparator<String>() {
            @Override
            public int compare(String x, String y) {
                return Integer.compare(x.length(), y.length());
            }
        });
        // names.sort((x, y) -> Integer.compare(x.length(), y.length()));
    }
}
```

**Listing 1.** `Sum` is a static nested helper. `Line` needs this `Ledger`. `Counter` is local: named, has a constructor, two instances, captures `extra`. The `Comparator` is a SAM — the commented lambda is the usual replacement unless you add fields or methods.

> [!warning] “Static nested if you don’t need outer fields” means no enclosing instance
> A `static` nested class may still read `private` instance fields given an `Outer` reference. Pick `static` when the helper must not be glued to one `Outer` object (and when you do not want that hidden enclosing-instance field).

> [!warning] Inner instances keep the outer alive
> `outer.new Inner()` associates the inner object with that `Outer`. Do not use an inner member (or a non-static-context local/anonymous class) for a helper that should outlive or be shared without a particular outer instance — that is a `static` nested class.

> [!warning] SAM + extra state is not a lambda
> A lambda cannot declare instance fields or a constructor. If the callback needs those, keep an anonymous or local class. A two-method type is not a functional interface; a lambda cannot replace it.

> [!tip] Interview answer
> **Nested means declared inside another type: member, local, or anonymous. Inner means it has (or can have) an enclosing instance.** Use static nested for a namespaced helper, inner when it must see `this` of the outer, local when one method needs a named type plus locals, anonymous for a single decorated instance, and a **lambda** for a single abstract method with no extra state.
