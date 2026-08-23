<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS

# Which parts of a system would you move into aspects?

> [!abstract] Short answer
> Move **infrastructure that repeats across many classes** but is **not domain logic**: **logging/tracing**, **transaction boundaries**, **security enforcement**, **caching**, **timing/metrics**, and **audit hooks**. Keep **business rules, pricing, workflow decisions, and entity behavior** inside domain/services — aspects should **wrap** join points, not replace them.

## Good candidates for aspects

Spring's AOP glossary treats **transaction management** as the canonical cross-cutting concern; the same pattern applies to other technical behavior that would otherwise be copy-pasted into every method.

| Concern | Typical aspect / Spring mechanism | Why aspects fit |
|---|---|---|
| **Logging / tracing** | `@Before` / `@AfterReturning` on service layer | Same enter/exit format everywhere — see [[Why is logging often implemented as a cross cutting aspect]] |
| **Transactions** | `@Transactional` (proxy AOP) | One declarative boundary around many repositories/services |
| **Security** | `@PreAuthorize`, `@Secured` (method security AOP) + web filters | Authorization spans controllers and services — [[Is security a cross-cutting concern]] |
| **Caching** | `@Cacheable` / `@CacheEvict` | Repeated read-through cache logic extracted from methods |
| **Timing / metrics** | `@Around` with `proceed()` + timer | Latency measurement without polluting business code |
| **Audit / compliance** | `@AfterReturning` logging who changed what | Cross-layer record-keeping unrelated to one aggregate |

Pointcuts let you target **`execution(* …service..*(..))`** (or annotation-driven cuts) so **new methods pick up the behavior automatically**.

```java
@Aspect
@Component
public class PerformanceAspect {

    @Around("@annotation(com.example.Timed)")
    public Object timed(ProceedingJoinPoint pjp) throws Throwable {
        long start = System.nanoTime();
        try {
            return pjp.proceed();
        } finally {
            long ms = (System.nanoTime() - start) / 1_000_000;
            // record metric for pjp.getSignature()
        }
    }
}
```

**Listing 1.** Technical measurement lives in the aspect; the business method stays focused on its job.

## What to leave out of aspects

**Do not** push **core business logic** into aspects:

- validating domain invariants specific to one aggregate
- computing prices, discounts, or eligibility rules
- orchestrating a use-case workflow

Those belong in **domain models and application services** where they are **testable and readable** without reading pointcut expressions.

Also remember **Spring AOP's limits**: default proxy AOP advises **public method executions on Spring beans** only. **HTTP security**, **filter chains**, and **non-bean code** use other mechanisms (Servlet filters, interceptors). Aspects complement — they do not replace — the full stack. See [[What is Advice in Spring AOP]] and [[What is a cross-cutting concern]].

```d2
direction: right
domain: "Domain / use-case logic\n(stays in services)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
aspect: "Aspect layer\n(log · tx · security · cache)" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
join: "Method execution\n(join point)" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}

aspect -> join -> domain: "wraps,\ndoes not replace"
```

**Fig. 1.** Aspects handle repeated technical concerns around business methods.

> [!warning] `@Around` is easy to overuse
> Spring recommends the **least powerful advice** that works — prefer `@Before` / `@AfterReturning` over `@Around` when you are not wrapping `proceed()`. Misused `@Around` can **swallow return values** ([[Why can Around advice lose the join point return value]]) or hide failures. **`this.internal()`** calls skip aspects anyway ([[Why does a self-invocation skip Spring AOP advice]]).

> [!tip] Interview answer
> Put cross-cutting infrastructure in aspects: logging, transactions, method security, caching, timing, audit. Leave business rules in domain code. Spring AOP wraps bean method executions via pointcuts — use the simplest advice type that fits, and remember filters and other layers handle concerns AOP cannot reach.
