<!--
reps: 0
priority: 0
-->
#Logging #Java/Spring/Framework/AOP #SRS

# Why is logging often implemented as a cross cutting aspect?

> [!abstract] Short answer
> **Logging is needed across many layers and classes** but is **not core business logic** — a classic **cross-cutting concern**. An **aspect** with a **pointcut** lets you **log once** (entry, exit, timing, errors) for whole packages (e.g. `service.*`) instead of copying **`log.info(...)`** into every method.

## Logging cuts across the application

Spring's AOP glossary defines an **aspect** as modularization of a concern that **cuts across multiple classes**. **Transaction management** is the textbook example; **logging**, **security**, and **timing** follow the same pattern.

Without AOP, each service/repository method tends to accumulate:

- duplicate **enter/leave** log lines
- inconsistent **message format** and **levels**
- forgotten logging on new methods

AOP applies the behavior **declaratively** at **join points** (in Spring AOP: **method executions** on proxied beans) matched by a **pointcut**, keeping domain code focused on business rules. See [[What is a cross-cutting concern]] and [[What is an Aspect in Spring AOP]].

```java
@Aspect
@Component
public class LoggingAspect {

    private static final Logger log = LoggerFactory.getLogger(LoggingAspect.class);

    @Before("execution(* com.example.service..*(..))")
    public void logEntry(JoinPoint jp) {
        log.info("→ {} args={}", jp.getSignature(), jp.getArgs());
    }

    @AfterReturning(pointcut = "execution(* com.example.service..*(..))", returning = "result")
    public void logReturn(JoinPoint jp, Object result) {
        log.info("← {} returned {}", jp.getSignature(), result);
    }
}
```

**Listing 1.** One aspect targets the whole service layer — no per-method log boilerplate.

## Why aspects fit logging especially well

| Benefit | How aspects help |
|---|---|
| **Single place to change** | Adjust format, level, or MDC in one `@Aspect` class |
| **Layer-wide coverage** | Pointcut `execution(* …service..*(..))` picks up new methods automatically |
| **Separation of concerns** | Business methods stay free of infrastructure noise |
| **Composable with other advice** | Same proxy chain also runs **transactions**, **security**, **caching** |

Spring recommends the **least powerful advice type** that suffices: use **`@Before`** / **`@AfterReturning`** for simple logging; reserve **`@Around`** for timing or when you must wrap **`proceed()`** — and always **return** `proceed()`'s value if you use `@Around` ([[Why can Around advice lose the join point return value]]).

```d2
direction: right
biz: "OrderService\nPaymentService\n…" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
aspect: "LoggingAspect\n(pointcut + advice)" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
log: "Single logging policy\napplied everywhere" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}

biz -> aspect -> log
```

**Fig. 1.** Cross-cutting logging modularized outside domain classes.

> [!warning] Aspects are not the only logging tool
> **SLF4J calls inside methods** remain appropriate for **domain-specific** messages (order id, business event). Aspects excel at **technical** cross-cuts (method boundary, latency). **`this.internal()`** self-invocations **skip** the proxy — no aspect logging there ([[Why does a self-invocation skip Spring AOP advice]]). Very hot paths may prefer manual logging or metrics over broad `@Around` overhead.

> [!tip] Interview answer
> Logging spans many classes but is not business logic — a cross-cutting concern. Aspects plus pointcuts let you apply entry/exit/timing logs once across a layer instead of duplicating log statements. Spring AOP weaves advice at runtime on proxied beans; use the simplest advice type that fits, usually @Before or @AfterReturning rather than @Around unless you need to wrap the call.
