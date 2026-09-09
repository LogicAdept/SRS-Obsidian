<!--
reps: 0
priority: 0
-->
#Java/MethodReferences #SRS

# What does the System.out println method reference mean

> [!abstract] Short answer
> **`System.out::println` is an instance method reference to `println` on the object stored in the static field `System.out` (a `PrintStream`).** It is exactly equivalent to the lambda `x -> System.out.println(x)`: wherever a functional interface expects a one-argument consumer, the reference receives that argument as `println`'s parameter.

## Reading the expression left to right

`System.out` is a public static field of `java.lang.System`, typed `PrintStream`, initialized to standard output. `::println` binds the *instance method* `println` of whatever object the left side evaluates to — evaluated once, at reference creation. The compiler checks the target functional interface: for `Consumer<String>` the SAM is `accept(String)`, and `println(String)` matches it.

```java
Consumer<String> printer = System.out::println;   // x -> System.out.println(x)
printer.accept("method reference prints this");

Runnable r = System.out::println;                 // println() with no args also exists
r.run();
```

**Listing 1.** Two different functional targets from the same reference — JDK 21 output:

```java
method reference prints this
```

**Listing 2.** The `Consumer` target calls `println(String)`; the `Runnable` target resolves to the no-arg `println()`. The reference adapts to whichever single method the target interface demands.

The four kinds of method references, with `System.out::println` as the instance-kind example:

| Form | Meaning | Example |
|---|---|---|
| `object::method` | bound instance method | `System.out::println` |
| `Class::staticMethod` | static method | `Integer::parseInt` |
| `Class::instanceMethod` | unbound: first arg is the receiver | `String::length` |
| `Class::new` | constructor reference | `ArrayList::new` |

> [!warning] Out is a mutable field, the receiver is captured early, and it prints wherever stdout goes
> Three details people miss. First, `System.out` is a *writable* public static field (`System.setOut` reassigns it): the reference binds the `PrintStream` object that `out` held **at creation time** — swapping stdout later does not redirect an existing reference (unlike the equivalent-looking lambda, which reads `System.out` on every invocation). Second, argument adaptation is exact: `System.out::println` works for `Consumer<String>`, `Runnable`, `Consumer<Object>`, `IntConsumer`... because `PrintStream.println` is overloaded — but if the target's signature matched no overload, the error appears at the reference site. Third, `System.out::println` in application code is often a smell where a test or abstraction should be — direct stdout coupling; in tests the idiom is to capture or inject a `PrintStream` instead. The mechanism that makes references legal at all — one abstract method per interface — is in [[How would you explain requirements for a Java functional interface]], the four interface shapes in [[What are the main functional interfaces in java.util.function]], and the pre-lambda history in [[How would you explain classic functional style interfaces before java.util.function]].

> [!tip] Interview answer
> **System.out::println is an instance method reference: System.out is a static PrintStream field, and ::println binds its println method. It equals the lambda x -> System.out.println(x) — used as Consumer in forEach or logs. The receiver is captured when the reference is created, so System.setOut later does not redirect it. It is one of four reference kinds: bound instance, static, unbound Class::instanceMethod, and Class::new.**

