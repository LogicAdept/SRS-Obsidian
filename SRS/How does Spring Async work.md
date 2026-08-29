<!--
reps: 0
priority: 0
-->
#Java/Async #Java/Annotations #SRS

# How does Spring Async work?

> [!abstract] Short answer
> **`@EnableAsync`** registers an advisor. A call **through the Spring proxy** to an **`@Async`** method is submitted to a **`TaskExecutor`** and the caller returns at once (`void`, or a **`Future` / `CompletableFuture`**). Default advice mode is **`PROXY`**: **`this.asyncMethod()`** is a **local call** and **does not** go async. Framework fallback executor is **`SimpleAsyncTaskExecutor`** (new thread per task). Boot already supplies a pooled **`AsyncTaskExecutor`** (or virtual-thread `SimpleAsyncTaskExecutor`) for `@EnableAsync`. Void exceptions are **logged** unless you set an **`AsyncUncaughtExceptionHandler`**.

## Proxy submits a `Runnable`; the caller does not wait

`@EnableAsync` on a `@Configuration` class turns on `AsyncAnnotationBeanPostProcessor`. The interceptor wraps matching beans. On an incoming proxy call it builds a `Runnable`/`Callable` and **`TaskExecutor.execute` / `submit`**. The proxy returns immediately. The worker thread then runs the target method ([[What happens when a Spring bean calls its own Async method]]).

```java
@Configuration
@EnableAsync
class AsyncConfig {}

@Service
class MailJob {
	@Async
	void send() { /* worker thread */ }

	@Async
	CompletableFuture<String> compute() {
		return CompletableFuture.completedFuture("ok");
	}
}
```

**Listing 1.** Enablement plus two signatures. Allowed returns: **`void`** or **`Future`** (including **`CompletableFuture`**). The **target** that returns a `Future` typically uses **`CompletableFuture.completedFuture(value)`**; the **proxy** hands the caller a real async future. **`@Async` is not supported on methods declared in a `@Configuration` class.** Class-level `@Async` marks every method. Qualifier: `@Async("otherExecutor")` (bean name, `@Qualifier`, `${…}`, or SpEL).

Executor lookup (Framework): unique **`TaskExecutor`**, else an **`Executor` named `taskExecutor`**, else **`SimpleAsyncTaskExecutor`**. **`AsyncConfigurer.getAsyncExecutor()`** overrides that. Boot’s task auto-config already exposes an **`AsyncTaskExecutor`** used for `@EnableAsync` — `ThreadPoolTaskExecutor` by default, **`SimpleAsyncTaskExecutor` with virtual threads** if `spring.threads.virtual.enabled=true` ([[How do you enable virtual threads in Spring Boot]]). A custom `Executor` bean makes Boot **back off** that auto-config for `@Async` unless you use `AsyncConfigurer` / `applicationTaskExecutor` / `spring.task.execution.mode=force`.

```d2
direction: down
caller: "Other bean\nmailJob.send()" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
proxy: "AOP proxy\nAsyncExecutionInterceptor" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
exec: "TaskExecutor\nsubmit / execute" {
  width: 220
  height: 50
  style.fill: "#e8f5e9"
}
target: "Target method\non worker thread" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}

caller -> proxy -> exec -> target
```

**Fig. 1.** Same-class `this.send()` never hits the proxy (`AdviceMode.PROXY`). **`ASPECTJ`** weaving intercepts local calls (`spring-aspects` + compile/load-time weaving). Default **`proxyTargetClass=false`** (JDK interface proxies).

Void `@Async`: exceptions **cannot** travel to the caller; default handler **logs** them. **`Future`**: the exception surfaces on **`get()`**. Register **`AsyncUncaughtExceptionHandler`** via **`AsyncConfigurer`**. **`AsyncConfigurer` beans initialize early** — inject other beans **`@Lazy`**.

```java
@PostConstruct
void init() {
	this.send(); // still the target, not the proxy
}
```

**Listing 2.** Illegal pairing: **`@Async` + `@PostConstruct` on the same bean**. Use a **second** bean whose `@PostConstruct` calls the **injected** (proxied) collaborator.

> [!warning] Self-invocation is the usual “@Async did nothing”
> The interceptor never runs for `this`. Private / `final` methods are not useful proxy join points. This is the same AOP limit as `@Transactional`. Switching to AspectJ is the documented escape hatch, not “make the method package-private.”

> [!warning] Framework’s default pool is not a pool
> **`SimpleAsyncTaskExecutor`** starts a **new thread per invocation** when no `TaskExecutor` exists. That is the Framework fallback, not Boot’s usual auto-config (8-core `ThreadPoolTaskExecutor` unless you already defined an `Executor`). Do not treat MVC **callable** async or WebFlux as `@Async` ([[What is the difference between Spring MVC async and WebFlux]]).

> [!tip] Interview answer
> @EnableAsync adds a proxy advisor. Calls through the bean proxy submit the method to a TaskExecutor and return void or a Future immediately. this.foo() stays synchronous. Void failures are only logged unless I set AsyncUncaughtExceptionHandler. Boot already gives me an AsyncTaskExecutor; without Boot, Spring falls back to SimpleAsyncTaskExecutor, which is not a bounded pool.
