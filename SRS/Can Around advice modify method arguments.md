<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# Can Around advice modify method arguments?

> [!abstract] Short answer
> **Yes.** `@Around` advice calls **`ProceedingJoinPoint.proceed(Object[] args)`** and Spring uses that array as the arguments of the **target method**. `proceed()` with no array keeps the caller’s originals. The advice must still **return** the `proceed()` result (or a deliberate substitute).

## `proceed(Object[])` replaces the call

Spring Framework *Declaring Advice*: invoking `proceed()` without arguments supplies the **caller’s original** arguments. The overload **`proceed(Object[])`** uses the array values as the arguments when the underlying method runs.

First parameter of `@Around` must be **`ProceedingJoinPoint`**. Return type should be **`Object`** so the caller sees the real result — [[Why can Around advice lose the join point return value]].

```java
@Around("execution(List<Account> find*(..)) && args(accountHolderNamePattern)")
public Object preProcessQueryPattern(ProceedingJoinPoint pjp,
        String accountHolderNamePattern) throws Throwable {
    String newPattern = preProcess(accountHolderNamePattern);
    return pjp.proceed(new Object[] { newPattern });
}
```

**Listing 1.** Conceptual pattern from Spring’s “Proceeding with Arguments” example — bind `args(...)` then pass a new array into `proceed`.

For **Spring AOP + AspectJ weaving** compatibility, bind **each** join-point parameter on the advice signature in order, then pass a matching `Object[]`. Native AspectJ `proceed` uses different arity rules (advice parameters, not join-point parameters); Spring’s proxy path is simpler: the array **is** the target invocation args.

```d2
direction: right
caller: "Caller\noriginal args" {
  width: 180
  height: 70
  style.fill: "#e3f2fd"
}
around: "@Around\nbuild Object[]" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
target: "Target method\nreplaced args" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

caller -> around -> target
```

**Fig. 1.** The interceptor sits between caller and target; only `proceed(Object[])` changes what the target receives. See [[What is ProceedingJoinPoint in Around advice]].

> [!warning] Array must be a legal invocation
> Length and types must match the target method. A mismatched array fails at invoke time (typical reflection `IllegalArgumentException`), not as a compile-time AspectJ check in Spring proxy mode.

> [!warning] `proceed()` without an array does not rewrite args
> Mutating a bound parameter variable (the `String name` advice argument) does **not** change the target call unless you pass a new `Object[]` into `proceed`.

> [!tip] Interview answer
> **Yes — around advice can replace arguments with `pjp.proceed(new Object[]{ … })`.** Spring feeds that array to the target method. No-arg `proceed()` keeps the originals. Return the `proceed()` value so the caller still sees the method result.
