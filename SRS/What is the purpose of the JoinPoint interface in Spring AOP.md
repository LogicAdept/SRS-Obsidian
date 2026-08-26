<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# What is the purpose of the `JoinPoint` interface in Spring AOP?

> [!abstract] Short answer
> **`org.aspectj.lang.JoinPoint` is the reflective view of the current join point** in an advice method: signature, arguments, `this` (proxy), and `target` (advised object). Declare it as an advice parameter (typically first). **`ProceedingJoinPoint`** extends it and is required for `@Around` so you can call **`proceed()`**.

## Reflective access from advice

AspectJ’s `JoinPoint` javadoc: it provides **reflective access** to state at the join point and static information about it — primarily for tracing and logging. Spring `@AspectJ` advice uses the same type as a method parameter instead of the AspectJ `thisJoinPoint` keyword.

| Method | Meaning |
| --- | --- |
| **`getSignature()`** | Method (or other) signature at the join point |
| **`getArgs()`** | Argument array |
| **`getThis()`** | Currently executing object — in Spring AOP, the **proxy** (`this` PCD) |
| **`getTarget()`** | Object being advised — the **target** behind the proxy (`target` PCD) |
| **`getKind()`** | Kind string (Spring AOP method execution is `method-execution`) |

`getThis()` / `getTarget()` are **null** when there is no instance (static context / no target). Prefer binding `this(...)` / `target(...)` / `args(...)` on the pointcut when you want typed parameters instead of reflection.

```java
@Before("execution(* com.xyz.service.*.*(..))")
public void logBefore(JoinPoint joinPoint) {
    String name = joinPoint.getSignature().getName();
    Object[] args = joinPoint.getArgs();
    Object proxy = joinPoint.getThis();
    Object target = joinPoint.getTarget();
}
```

**Listing 1.** Conceptual `@Before` using the JoinPoint API. Concept of the site itself: [[What is a JoinPoint in Spring AOP]].

```d2
direction: right
adv: "Advice method" {
  width: 160
  height: 60
  style.fill: "#fff3e0"
}
jp: "JoinPoint\ngetArgs / getSignature" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
proxy: "getThis()\nAOP proxy" {
  width: 160
  height: 60
  style.fill: "#e8f5e9"
}
tgt: "getTarget()\nadvised bean" {
  width: 180
  height: 60
  style.fill: "#fce4ec"
}

adv -> jp
jp -> proxy
jp -> tgt
```

**Fig. 1.** Spring AOP splits proxy (`this`) and target; they are the same object only in full AspectJ execution join points.

> [!warning] `JoinPoint` cannot invoke the target
> `@Around` must take **`ProceedingJoinPoint`** as the **first** parameter — [[What is ProceedingJoinPoint in Around advice]]. A plain `JoinPoint` has no `proceed()`.

> [!warning] `getThis()` is not always the domain object
> Logging `getThis().getClass()` often prints the **CGLIB or JDK proxy** type. Use `getTarget()` (or `AopUtils`) when you need the underlying class.

> [!tip] Interview answer
> **`JoinPoint` is how advice inspects the current method execution** — name, args, proxy vs target. Declare it on `@Before` / `@After*`. For `@Around` you need `ProceedingJoinPoint` so you can `proceed()`. Prefer pointcut binding (`args`, `target`) when you want typed access without reflection.
