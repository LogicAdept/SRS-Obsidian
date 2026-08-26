<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Async #Java/Annotations #SRS

# What happens when a Spring bean calls its own Async method?

> [!abstract] Short answer
> **`this.asyncMethod()` runs on the caller thread.** Default **`@EnableAsync`** uses **proxy** mode: the `@Async` interceptor never sees **local** calls. The annotation is **ignored** for that invocation. Call **through the proxy** (another bean or self-injection) or switch to **`AdviceMode.ASPECTJ`** with weaving.

## Same hole as `@Transactional`

`EnableAsync` javadoc: proxy mode intercepts **calls through the proxy only**. A local call inside the class **does not** kick in Spring’s interceptor, so `@Async` on that method is ignored. Spring *Task Execution*: same text; for full interception use **`aspectj`** mode plus compile-time or load-time weaving (`spring-aspects`). General proxy story: [[Why does a self-invocation skip Spring AOP advice]].

```java
@Service
public class ReportService {

    public void generate() {
        this.writeAsync(); // synchronous — same thread
    }

    @Async
    public void writeAsync() { /* submitted only if entered via proxy */ }
}
```

**Listing 1.** Conceptual: `generate()` entered the target; `this.writeAsync()` never hits `AsyncExecutionInterceptor`.

Workarounds (proxy mode):

* Call from **another Spring bean** that holds the proxy.
* **Self-inject** the bean and call the async method on that reference (Spring’s proxying docs).
* **`@EnableAsync(mode = AdviceMode.ASPECTJ)`** — no proxy; local calls are woven. `proxyTargetClass` is ignored. AspectJ mode parallel: [[When should you use AspectJ mode for Transactional self-invocation]].

You still need **`@EnableAsync`** (local to that `ApplicationContext`). Executor: unique **`TaskExecutor`**, or an **`Executor` named `taskExecutor`**, else **`SimpleAsyncTaskExecutor`** (new thread per call, not a pool). Qualify with `@Async("otherExecutor")`.

```d2
direction: down
ext: "otherBean.async()" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
proxy: "Async proxy\nsubmits to TaskExecutor" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
self: "this.async()\non the target" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}

ext -> proxy
self -> proxy: "never"
```

**Fig. 1.** Only the green path is asynchronous. `@Async` cannot combine with **`@PostConstruct`**: use a **separate** initializing bean that calls the `@Async` method **on the target bean** (Spring’s example).

> [!warning] “It compiled, so it is async” is false
> Self-invocation **succeeds** and looks like a normal method. No exception, no extra thread. Tests that only call `generate()` miss it.

> [!warning] `void` vs `Future`
> Return type must be **`void` or `Future` / `CompletableFuture`**. `void` cannot pass exceptions to the caller — they are logged unless you set **`AsyncUncaughtExceptionHandler`**. `@Async` is **not** supported on methods in a **`@Configuration`** class.

> [!tip] Interview answer
> **A same-class call to `@Async` stays synchronous — proxy mode never intercepts `this`.** Inject the proxy or another bean, or use AspectJ async mode. Enable with `@EnableAsync`; don’t assume a thread pool unless you configured one.
