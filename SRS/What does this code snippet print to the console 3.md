<!--
reps: 0
priority: 0
-->
#Career/Interview/Exercises #Java/Lambdas #Java/Language/Modifiers/Final #SRS

# What does this code snippet print to the console 3?

> [!abstract] Short answer
> **Nothing — it does not compile.** The lambda `() -> i++` both **reads and assigns** the local `i`. A local used from a lambda must be **final or effectively final**, so the assignment is a compile-time error and `println` never runs. Why that rule exists: [[How would you explain effectively final]]. What `final` on a variable means: [[What does the final keyword mean in Java]]. Contrast: [[What does the static keyword mean in Java]] does not apply — `i` is a local, not a class variable.

## Why there is no output

```java
public static void main(String args[]) {
    int i = 1;
    Supplier<Integer> s = () -> i++;
    System.out.println(s.get());
}
```

**Listing 1.** The interview snippet. `i++` is an assignment to `i`, so `i` is not effectively final.

A lambda body may use a local, parameter, or exception parameter declared **outside** the lambda only if that variable is never assigned after its initialization (or is declared `final`). Postfix `++` writes the variable. The compiler rejects the lambda. It does not produce `1`, `2`, or any console line.

If the body were `() -> i + 1` (no write to `i`), the code would compile and **print `1`**. `i` stays `1`; the supplier returns a new value.

To **mutate a counter** from a lambda, keep the **variable** effectively final and mutate the **object** it names, for example an `AtomicInteger` or a one-element array. That is a different program, not a way to make Listing 1 print.

```d2
direction: down
q: "() -> i++  with local i" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
err: "compile error\nnot effectively final" {
  width: 220
  height: 48
  style.fill: "#ffcdd2"
}
ok: "() -> i + 1\nprints 1" {
  width: 180
  height: 48
  style.fill: "#e8f5e9"
}
q -> err
q -> ok
```

**Fig. 1.** The `++` is the whole question. Read-only use of `i` would print; assignment does not run.

> [!warning] “What does it print?” can be a trick for “it never runs”
> Do not guess `1` (the postfix result) or `2` (after increment). Those answers describe a program the compiler will not accept. Same trap as assigning to a captured local in an inner class.

> [!warning] `AtomicInteger` does not make `i++` legal
> Replacing `int i` with `AtomicInteger i` and calling `getAndIncrement()` is a **rewrite**. The original `int` local still cannot appear on the left of an assignment inside the lambda.

> [!tip] Interview answer
> It does not print anything: `i++` assigns to the captured local, so `i` is not effectively final and the file does not compile. A lambda may read `i` only if `i` is never reassigned. To increment from a lambda, capture a final reference to a mutable object, not a reassignable `int`.
