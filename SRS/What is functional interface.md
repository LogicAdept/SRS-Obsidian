<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #Java/Lambdas #Java/Versions/8 #SRS

# What is functional interface

> [!abstract] Short answer
> **An interface with exactly one abstract method that is not a public `Object` method — one function contract.** Java 8 can implement it with a lambda or a method/constructor reference. `@FunctionalInterface` (`@since 1.8`) **documents** that intent and makes a second abstract method a compile error; it is **not** required. `default` / `static` methods do not count. `Comparator.compare` is a functional interface even though it also restates `equals`.

## One abstract method, then a lambda

A functional interface represents a **single** function contract: the set of abstract members, ignoring public `Object` methods such as `equals`, has one method (or several override-equivalent inherited abstracts that logically are one). Instances can be created by a class, a lambda, or a method reference ([[How would you explain lambda expressions in Java]], [[How would you explain requirements for a Java functional interface]], [[How would you explain core functional interfaces in java.util.function]]).

`java.lang.Runnable` (`void run()`) is the textbook case. `NonFunc { boolean equals(Object); }` is **not** functional — it adds nothing beyond `Object`. `Comparator<T>` **is** functional: `compare` is the new method; `equals` does not count.

`default` methods have a body, so they are not abstract. An interface can have many defaults (and statics) and still be functional ([[How would you explain default interface methods since Java 8]], [[How would you explain Consumer DoubleConsumer IntConsumer and LongConsumer]]). Declaring `clone()` as a public abstract in an interface **does** count (it is not a public `Object` method), so `Foo { int m(); Object clone(); }` is not functional.

`@FunctionalInterface` is `@Documented`, `@Retention(RUNTIME)`, `@Target(TYPE)`. Compilers must error if it sits on a non-interface or on a type that is not functional. Any interface that meets the definition is still a functional interface **without** the annotation — `Runnable` was a SAM type before 8. The annotation is the `@Override`-style check the dump describes, not a new kind of interface.

```d2
direction: down
fi: "functional interface\n1 abstract method ≠ Object" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
ok: "default / static\nObject equals" {
  width: 240
  height: 50
  style.fill: "#fff8e1"
}
use: "lambda / method ref" {
  width: 220
  height: 45
  style.fill: "#e3f2fd"
}

ok -> fi: "do not count"
fi -> use
```

**Fig. 1.** Count abstracts after dropping public `Object` methods. Defaults never enter that count.

```java
@FunctionalInterface
interface OneShot {
    void go();
    default void twice() { go(); go(); }
}

class Demo {
    static void run() {
        OneShot a = () -> {};
        java.util.Comparator<String> c = String::compareTo;
        // @FunctionalInterface interface Two { void a(); void b(); } // compile error
        // interface OnlyEquals { boolean equals(Object o); }        // not functional
    }
}
```

**Listing 1.** One SAM, extra `default` still functional. `Comparator` is a lambda target because `equals` is ignored. `@FunctionalInterface` on two abstracts does not compile.

> [!warning] `@FunctionalInterface` is optional
> Dump text that says you add the annotation “in order to define” a functional interface is backwards: the **shape** defines it. The annotation only fails the compile if you then add a second abstract method. `equals` on `Comparator` is not a second SAM.

> [!warning] `Object` methods are a trap
> `equals` / `hashCode` / `toString` restated on the interface do not destroy the SAM. A public `clone()` or `finalize()` declaration does. Lambdas cannot use `this` to call the interface’s own `default` methods ([[Which variables can lambda expressions access in Java]]).

> [!tip] Interview answer
> **Functional interface = one abstract method besides `Object`’s publics.** Java 8: lambda or `::`. `@FunctionalInterface` is an optional compiler check (`@since 1.8`). Defaults are allowed. `Runnable`, `Comparator`, `Consumer` / `Function` / `Predicate` / `Supplier`.
