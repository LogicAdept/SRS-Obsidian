<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS

# What is the `Pointcut` annotation used for?

> [!abstract] Short answer
> **`@Pointcut` names a reusable AspectJ expression.** Put it on a **`void` method** (the **signature**). The **expression** is the annotation value; the method body stays empty. Advice refers to that name (`@Before("serviceLayer()")`) instead of repeating the string.

## Signature plus expression

Spring *Declaring a Pointcut*: a pointcut has a **signature** (name and parameters) and an **expression**. In `@AspectJ` style the signature is a regular method; the expression is `@Pointcut`. **The method must have a `void` return type.**

```java
@Pointcut("execution(* transfer(..))") // expression
private void anyOldTransfer() {}       // signature — empty body
```

**Listing 1.** Spring’s `anyOldTransfer` example. Advice then uses `@Around("anyOldTransfer()")` or a fully qualified `com.xyz.Pointcuts.anyOldTransfer()`.

Compose named cuts with `&&` / `||` / `!` — [[How do you combine multiple pointcut expressions]]. What goes in the string: [[How do you define a pointcut expression in Spring AOP]], [[What is a Pointcut in Spring AOP]].

You can still inline the same string on `@Before` / `@After*` / `@Around`. Named `@Pointcut` is for sharing and for binding (`args(name)` on the signature parameters).

```d2
direction: right
ann: "@Pointcut(\"execution(...)\")" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
sig: "void serviceLayer() {}" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
use: "@Before(\"serviceLayer()\")" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}

ann -> sig -> use
```

**Fig. 1.** The annotation holds the predicate; the method name is how advice reuses it.

> [!warning] Empty body is required, not optional fluff
> Logic does not belong in the `@Pointcut` method. Matching is the expression string. A non-`void` return type is invalid for this declaration style.

> [!warning] The name is a method reference, not a Spring bean id
> `@Before("serviceLayer")` without `()` is not the usual form. Use **`serviceLayer()`** or `com.example.CommonPointcuts.serviceLayer()`. Java visibility decides who can see a `private` vs `public` cut.

> [!tip] Interview answer
> **`@Pointcut` declares a named, reusable match rule on a `void` method with an empty body.** The AspectJ string is the annotation value. Advice points at that method name so you do not copy-paste `execution(...)` everywhere.
