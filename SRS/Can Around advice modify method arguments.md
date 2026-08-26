<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# Can Around advice modify method arguments?

> [!abstract] Short answer
> **Yes, in Spring AOP.** `@Around` advice can replace the target method’s arguments by calling `ProceedingJoinPoint.proceed(Object[] args)`. `proceed()` with no array keeps the caller’s original arguments.

Only around advice owns `ProceedingJoinPoint`. Other advice kinds can *read* arguments (for example via `JoinPoint.getArgs()` or `args(...)` binding) but cannot swap what the join point runs with. See [[What is ProceedingJoinPoint in Around advice]] and [[What advice types does Spring AOP support]].

## How argument replacement works

```d2
direction: down
call: "Client calls\nproxied bean method" {
  width: 260
  height: 80
  style.fill: "#e3f2fd"
}
around: "@Around advice\nreceives ProceedingJoinPoint" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
choose: "Which proceed?" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
orig: "proceed()\n→ original args" {
  width: 240
  height: 80
  style.fill: "#e8f5e9"
}
repl: "proceed(Object[])\n→ array becomes args" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}
target: "Target method runs\n(or advice short-circuits)" {
  width: 280
  height: 90
  style.fill: "#f3e5f5"
}

call -> around
around -> choose
choose -> orig
choose -> repl
orig -> target
repl -> target
```

**Fig. 1.** Spring AOP around advice decides whether the target sees the original arguments or a replacement array.

Spring Framework documents this explicitly: `proceed()` without arguments supplies the caller’s originals; the overloaded `proceed(Object[])` uses the array values as the arguments of the underlying method. Spring’s runtime implementation (`MethodInvocationProceedingJoinPoint`, Spring Framework 6.2) also rejects a `null` array and requires the array **length** to equal the join-point argument count, or it throws `IllegalArgumentException`.

```java
@Around("execution(List<Account> find*(..)) && args(accountHolderNamePattern)")
public Object preProcessQueryPattern(
        ProceedingJoinPoint pjp,
        String accountHolderNamePattern) throws Throwable {
    String newPattern = preProcess(accountHolderNamePattern);
    return pjp.proceed(new Object[] { newPattern });
}
```

**Listing 1.** Official Spring shape: bind every method parameter in order, then `proceed` with a same-length `Object[]` (Spring Framework 6.x Declaring Advice).

For portability with AspectJ weaving, Spring recommends that same pattern: bind each target parameter on the advice signature in order, then pass a matching `Object[]` to `proceed`. Spring’s proxy-based semantics treat the array as the full argument list of the join point; classic AspectJ around advice uses a different `proceed` arity rule tied to the advice parameters.

```java
Object[] args = pjp.getArgs();
args[0] = "mutated";
return pjp.proceed(); // still original args
```

**Listing 2.** Conceptual pitfall: `getArgs()` returns a clone; mutating it does not change the invocation unless you pass that array to `proceed(Object[])`.

> [!warning] Wrong array length fails fast
> In Spring AOP, `proceed(new Object[]{...})` must have the **same length** as the advised method’s argument list. A shorter or longer array throws `IllegalArgumentException` (“Expecting N arguments to proceed…”) before the target runs. Wrong **types** are a separate failure later (typically at reflective invoke), not that length check.

> [!warning] Proxy boundary still applies
> Argument rewriting only happens when the call goes through the Spring proxy into advised around advice. A self-invocation on `this` never enters the proxy, so [[Why does a self-invocation skip Spring AOP advice]] applies here too — no around advice, no modified args.

> [!tip] Interview answer
> **Yes — around advice can change arguments with `proceed(Object[])`.** Plain `proceed()` keeps the originals. In Spring AOP the array must match the target method’s arity or you get `IllegalArgumentException`. Mutating `getArgs()` alone is not enough; pass the new array to `proceed`.
