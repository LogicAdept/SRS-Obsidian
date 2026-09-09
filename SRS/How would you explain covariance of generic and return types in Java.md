<!--
reps: 0
priority: 0
-->
#Java/Generics #Java/OOP #SRS

# How would you explain covariance of generic and return types in Java

> [!abstract] Short answer
> Java has two different covariance stories. Covariant **return types** in overriding are allowed: an override may narrow the return type to a subtype. Covariant **generic subtyping** is forbidden: `List<Integer>` is not a `List<Number>`, because generics are invariant; arrays are covariant and pay for it with runtime `ArrayStoreException`.

The two senses share a word but live in different places: one is about the return type of an overridden method, the other about the subtype relation between parameterized types. Interviewers use the shared name to catch people who know one and not the other.

## Covariant return types in overriding

When a method overrides another, its return type may be a **subtype** of the original — this is return-type-substitutability, allowed for reference types since Java 5. The caller's code stays valid because every `Dog` is an `Animal`; the JVM bridges the gap with a synthetic bridge method carrying the erased signature that delegates to the narrowed one — the same mechanism [[How does type erasure work for Java generics]] inserts for generic overriding. [[Can you declare a narrower return type when overriding a method]] drills the rules: primitives must match exactly, reference types may narrow.

## Generic types are invariant

`List<Integer>` and `List<Number>` are unrelated types. The reason is the aliasing problem: if `List<Integer>` were a `List<Number>`, code holding the `List<Number>` reference could `add(1.5)` into a list someone else reads as integers, and the type system would be lying. Arrays took that deal — `Integer[]` **is** a `Number[]` — so the JVM checks every array store at runtime and throws `ArrayStoreException` when covariance is abused. Generics moved the same check to compile time, at the cost of invariance, which [[What is the difference between an array and an ArrayList]] makes visible in everyday APIs.

```d2
direction: down
arr: "Arrays: covariant" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
arrOk: "Integer[] IS-A Number[]\ncompiles" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
arrFail: "nums[0] = 1.5\nArrayStoreException at runtime" {
  width: 340
  height: 90
  style.fill: "#ffebee"
}
gen: "Generics: invariant" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
genFail: "List<Integer> is NOT List<Number>\ncompile-time error" {
  width: 340
  height: 90
  style.fill: "#e8f5e9"
}
wild: "Wildcards restore flexibility\nList<? extends Number>" {
  width: 340
  height: 90
  style.fill: "#e8f5e9"
}
arr -> arrOk
arrOk -> arrFail
gen -> genFail
genFail -> wild
```

**Fig. 1.** Arrays buy covariance with a runtime check; generics refuse it and hand the flexibility problem to wildcards.

```java
import java.util.ArrayList;
import java.util.List;

public class CovarianceDemo {

    static class Animal {
        @Override public String toString() { return "Animal"; }
    }
    static class Dog extends Animal {
        @Override public String toString() { return "Dog"; }
        @Override public Dog clone() { return new Dog(); } // covariant return (Object->Animal->Dog chain)
    }

    public static void main(String[] args) {
        Animal a = new Dog().clone(); // Dog return type, no cast
        System.out.println(a); // Dog

        // Arrays are covariant: Integer[] IS-A Number[]
        Number[] nums = new Integer[3]; // compiles
        try {
            nums[0] = 1.5; // compiles, fails at runtime
        } catch (ArrayStoreException e) {
            System.out.println("ArrayStoreException"); // runtime guard for covariance
        }

        // Generics are invariant: List<Integer> is NOT a List<Number>
        // List<Number> bad = new ArrayList<Integer>(); // compile-time error
        List<Integer> ints = new ArrayList<>();
        ints.add(1);
        System.out.println(ints.get(0)); // 1 — no ArrayStoreException possible in pure generic code
    }
}
```

**Listing 1.** The override narrows the return type legally; array covariance defers its safety check to runtime.

## Where the flexibility went

Use-site variance returns what declaration-site invariance removes: `List<Integer>` **is** a `List<? extends Number>` and a `List<? super Integer>`, which is how library APIs stay usable — [[How would you explain wildcard bounded and unbounded types in Java generics]] and [[How would you explain the PECS rule for generic method signatures]] cover the mechanics. A botched wildcard cast, unlike an array store, still fails at compile time; the residual runtime risk is the unchecked cast, whose delayed explosion surfaces as [[When can a ClassCastException be thrown in Java]].

> [!warning] "Generics are covariant" is a legendary lie
> Java generics are **invariant** by design; only wildcards introduce variance, and only at the use site. Mixing this up with covariant return types — a different feature with a similar name — is the standard trap. The arrays comparison cuts the other way too: array covariance is widely considered a design flaw, which is why `List<Integer>` cannot flow into `Object[]`-style APIs, and why `Arrays.asList` returns a fixed-size view instead of an array wrapper.

> [!tip] Interview answer
> Two features share the word. Return types: overriding may narrow to a subtype — covariant returns since Java 5, backed by bridge methods. Generic types: invariant — `List<Integer>` is not `List<Number>`, because covariance would let a `Double` sneak into an integer list; arrays are covariant and pay with `ArrayStoreException` at runtime. Java's answer for generics is use-site variance: `? extends` for reads, `? super` for writes.

