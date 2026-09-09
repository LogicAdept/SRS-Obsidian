<!--
reps: 0
priority: 0
-->
#Java/FunctionalInterfaces #SRS

# How would you explain requirements for a Java functional interface

> [!abstract] Short answer
> **A functional interface is an interface with exactly one abstract method — the SAM rule.** Default and static methods do not count (they have bodies), and redeclaring a public `Object` method (`toString`, `equals`) does not count either. `@FunctionalInterface` is an optional marker that makes the compiler enforce the rule; lambdas and method references create its instances.

## What counts toward "exactly one abstract method"

The annotation's own javadoc states the contract: conceptually exactly one abstract method; default methods are not abstract; and an abstract method overriding a public `java.lang.Object` method does not count, because any implementation already has one from `Object`. Static methods with bodies do not count either.

```d2
direction: right
sam: "One abstract method\n(the target type)" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
no1: "default methods\nhave bodies -> don't count" {
  width: 300
  height: 90
  style.fill: "#fff3e0"
}
no2: "static methods\nhave bodies -> don't count" {
  width: 290
  height: 90
  style.fill: "#fff3e0"
}
no3: "abstract toString/equals\n(Object override) -> don't count" {
  width: 330
  height: 90
  style.fill: "#fff3e0"
}
sam -> no1
sam -> no2
sam -> no3
```

**Fig. 1.** Only one bodyless method is allowed; the three exclusion rules are what people miss.

```java
@FunctionalInterface
interface Validator {
    boolean valid(String input);                    // THE abstract method

    default Validator and(Validator other) {        // default: does not count
        return s -> valid(s) && other.valid(s);
    }
    static Validator notEmpty() {                   // static: does not count
        return s -> !s.isEmpty();
    }
    String toString();                              // Object override: does not count
}

Validator v = Validator.notEmpty().and(s -> s.length() < 10);
System.out.println(v.valid("hello") + " / " + v.valid(""));
```

**Listing 1.** Verified on JDK 21: `true / false`. One SAM plus defaults, statics, and an `Object` redeclaration — still a functional interface.

## Why the rule exists

A lambda `x -> x * x` has no name — the compiler must map it onto exactly one method signature: which interface, which method. Zero abstract methods leaves the lambda no target; two leaves ambiguity. The `@FunctionalInterface` annotation is *informative*, not required — any SAM interface accepts lambdas — but it converts a design mistake (someone adding a second abstract method and breaking every lambda client) into a compile-time error at the interface itself. Instances can also come from method references and constructor references, not just lambdas. The standard library set lives in [[What are the main functional interfaces in java.util.function]], and the pre-Java-8 ancestors that were retrofitted with the same shape are in [[How would you explain classic functional style interfaces before java.util.function]].

> [!warning] Two classic miscounts
> First: "an interface with `@FunctionalInterface`" is not the definition — the annotation is a check, not the rule; unmarked SAM interfaces (`Runnable` before the annotation existed, `Comparator`) are equally functional. Second, the count is per-interface including inherited abstract methods: extending another interface adds its abstract methods to the count — an interface extending two SAMs with different signatures is not functional, while one extending a SAM and overriding `Object` members still is. Also note the annotation does not make a class or an abstract class a lambda target — only interfaces.

> [!tip] Interview answer
> **A functional interface has exactly one abstract method. Defaults, statics, and redeclarations of public Object methods don't count toward that one. @FunctionalInterface is optional — it just asks the compiler to enforce the rule. The single method is what makes lambdas and method references possible: the compiler needs exactly one target signature.**

