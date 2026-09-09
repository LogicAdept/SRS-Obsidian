<!--
reps: 0
priority: 0
-->
#Java/Generics/TypeBounds #SRS

# What is the purpose of type bounds in Java generics

> [!abstract] Short answer
> A bound restricts which type arguments a caller may pass and, in exchange, widens what the generic body may call. `<T>` erases to `Object`, so a bare `T` value only offers `Object` methods; `<T extends Comparable<T>>` erases to `Comparable`, so the body can call `compareTo` directly while callers are locked to types that implement it.

A bound is a contract on a **type parameter** — the declaration-site mechanism distinct from use-site wildcards (see [[What is the difference between extends and super wildcards in Java generics]]). Every type variable has a bound: undeclared means `Object`.

## What a bound promises the body

With `<T extends Comparable<T>>` the compiler knows any `T` value is comparable, so the method body compiles without casts, and the call site rejects types that break the promise:

```d2
direction: right
decl: "<T extends Comparable<T>>\nT max(T a, T b)" {
  width: 320
  height: 100
  style.fill: "#e3f2fd"
}
body: "Body may call:\na.compareTo(b)" {
  width: 250
  height: 90
  style.fill: "#fff3e0"
}
caller: "Caller may pass:\nInteger, String, P..." {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
erase: "Erasure: T -> Comparable\n(leftmost bound)" {
  width: 280
  height: 90
  style.fill: "#ffebee"
}
decl -> body: grants members of the bound
decl -> caller: restricts arguments
decl -> erase
```

**Fig. 1.** One clause, two effects: the body gains the bound's members, the caller is restricted to subtypes, and erasure uses the leftmost bound.

```java
import java.util.Arrays;
import java.util.List;

public class TypeBoundsDemo {

    static <T extends Comparable<T>> T max(T a, T b) {
        return a.compareTo(b) >= 0 ? a : b; // T promises Comparable, so compareTo is callable
    }

    interface Named { String name(); }
    record P(String name, int age) implements Named, Comparable<P> {
        @Override public String name() { return name; }
        @Override public int compareTo(P o) { return Integer.compare(age, o.age); }
    }

    // Multiple bounds: first a class (or none), then interfaces:
    static <T extends Named & Comparable<T>> String describe(T x, T y) {
        return x.name() + " older? " + (x.compareTo(y) > 0);
    }

    public static void main(String[] args) {
        System.out.println(max(3, 7));      // 7
        System.out.println(max("a", "b")); // b
        // max(3, "b"); // compile-time error: String is not Comparable<Integer>

        List<P> people = Arrays.asList(new P("A", 30), new P("B", 41));
        P p1 = people.get(0), p2 = people.get(1);
        System.out.println(describe(p1, p2)); // A older? false
    }
}
```

**Listing 1.** The bound lets the body compare values and makes an incomparable argument a compile-time error.

## Multiple bounds and the JDK idiom

A bound may list a class plus interfaces: `<T extends Class & I1 & I2>`; extra bounds must be interfaces, and the erasure of `T` is the leftmost bound, which links bounds to [[How does type erasure work for Java generics]]. The standard library leans on **recursive bounds** to express "comparable to its own kind": `Collections.max` declares `<T extends Object & Comparable<? super T>> T max(Collection<? extends T> coll)`. The `? super T` relaxes the recursion: if `Person` implements `Comparable<Person>`, then a subclass `Employee` satisfies `Comparable<? super Employee>` through the inherited comparison — a plain `<T extends Comparable<T>>` would reject it.

## Where bounds show up in the API

Any API that needs a capability from an opaque type uses a bound: sorting needs comparability, so `TreeMap` requires keys to be `Comparable` or requires an explicit `Comparator` — see [[What types can you use as TreeMap keys]]. Generic methods that produce values from bounded parameters follow [[How would you explain the PECS rule for generic method signatures]] when the bound interacts with wildcards.

> [!warning] A type-parameter bound is not a wildcard bound
> `<T extends Number>` restricts a declaration and exists at compile time in signatures; `? extends Number` is an unknown argument at a use site. The two are not interchangeable, and only wildcards accept a **lower** bound: `<T super Number>` does not compile, because type-variable bounds exist to promise the body capabilities (upper limits), while `? super` exists to promise a caller a safe sink. Mixing this up is the standard generics trap in interviews.

> [!tip] Interview answer
> Bounds do two jobs at once: they narrow what callers can pass and they widen what the generic code can do with a value. `<T extends Comparable<T>>` means the body can call `compareTo` and only comparable types compile. Bounds can combine a class with extra interfaces, erasure takes the leftmost one, and the JDK's recursive form `T extends Comparable<? super T>` lets inherited comparators work. And remember: lower bounds like `<T super X>` do not exist — that is wildcard-only syntax.

