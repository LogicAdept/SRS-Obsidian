<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# How do you define a pointcut expression in Spring AOP?

> [!abstract] Short answer
> Write an **AspectJ pointcut string** — usually `execution(...)` — as the value of **`@Pointcut`**, or inline it on `@Before` / `@After` / `@Around`. Spring AOP matches **method execution** join points on Spring beans only. Combine designators with **`&&`**, **`||`**, and **`!`**, or compose named `@Pointcut` methods.

## Expression plus signature

A pointcut has two parts: a **signature** (a `void` method that names it) and an **expression** (the `@Pointcut` string). Advice can reuse that name or carry the expression itself.

```java
@Aspect
@Component
public class ServiceLoggingAspect {

    @Pointcut("execution(* com.xyz.service.*.*(..))")
    public void serviceLayer() {}

    @Before("serviceLayer()")
    public void logBefore(JoinPoint jp) {
        // ...
    }
}
```

**Listing 1.** Named pointcut from Spring’s `@AspectJ` style: `execution` is the primary designator; the empty method is only the signature.

`execution` form (optional parts omitted in the usual case):

```
execution(modifiers-pattern? ret-type-pattern declaring-type-pattern?name-pattern(param-pattern) throws-pattern?)
```

Required pieces are **return type**, **name**, and **parameters**. `*` matches any return type; `(..)` matches any argument list; `()` means no args; `(*)` means one arg of any type.

| Expression | Matches |
| --- | --- |
| `execution(* com.xyz.service.*.*(..))` | Any method **in** `com.xyz.service` (not subpackages) |
| `execution(* com.xyz.service..*.*(..))` | Same package **or nested packages** (`..`) |
| `within(com.xyz.service..*)` | Any execution whose declaring type is in that package tree |
| `@annotation(org.springframework.transaction.annotation.Transactional)` | Method that carries that annotation |

Spring also supports `this`, `target`, `args`, `@target`, `@args`, `@within`, and the Spring-only **`bean(idOrName)`** (proxy mode; not native AspectJ weaving). Unsupported AspectJ designators such as `call`, `get`, `cflow` throw **`IllegalArgumentException`**.

```d2
direction: right
sig: "@Pointcut method\n(signature)" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
expr: "AspectJ string\nexecution / within / bean" {
  width: 260
  height: 80
  style.fill: "#fff3e0"
}
match: "Method execution\non Spring bean" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

sig -> expr -> match
```

**Fig. 1.** The annotation holds the expression; matching is limited to proxied method executions. Combine named cuts as in [[How do you combine multiple pointcut expressions]].

> [!warning] One `*` is not a subpackage
> `com.xyz.service.*.*` is types **in that package only**. Subpackages need `com.xyz.service..*.*` (two dots). Interview dumps often swap these.

> [!warning] Proxy matching is not full AspectJ
> Self-invocation inside the target never matches, even if the expression would. JDK proxies intercept **public interface** methods; CGLIB can intercept public/protected (and package-visible if needed). Private methods stay out of Spring AOP — [[Can Spring AOP advise private methods]].

> [!tip] Interview answer
> **Put an AspectJ `execution` (or `within` / `@annotation` / `bean`) string on `@Pointcut` or on the advice annotation.** Spring AOP only matches method executions on Spring beans. Use `..` for subpackages, combine with `&&` / `||` / `!`, and remember the proxy never sees `this` calls.
