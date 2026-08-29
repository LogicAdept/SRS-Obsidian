<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS

# How do you shut down a Spring `ApplicationContext`?

> [!abstract] Short answer
> Call **`ConfigurableApplicationContext.close()`** (it is `Closeable`: try-with-resources works). In a **non-web** process that outlives `main`, also call **`registerShutdownHook()`** so the JVM still closes the context. Both paths run `doClose()`: publish `ContextClosedEvent`, stop `Lifecycle` beans on a regular shutdown, destroy **cached singletons**. That does **not** close a parent context. After close, the context is finished — no refresh or restart.

## `close()` versus the JVM hook

`ApplicationContext` is the client view. Shutdown lives on **`ConfigurableApplicationContext`** (`AbstractApplicationContext` implements it). `close()` releases resources and **destroys cached singleton beans**. It is **idempotent**. It does **not** call `close()` on a parent. An explicit `close()` **unregisters** a previously installed JVM hook.

`registerShutdownHook()` adds at most **one** `Runtime` hook per context. The thread name is `ConfigurableApplicationContext.SHUTDOWN_HOOK_THREAD_NAME` (`"SpringContextShutdownHook"`, Framework **5.2+**). On JVM exit the hook closes the context **unless it is already closed**. Call it as many times as you like; only one hook is stored.

```java
ConfigurableApplicationContext ctx =
        new ClassPathXmlApplicationContext("beans.xml");
ctx.registerShutdownHook();
```

**Listing 1.** Conceptual standalone `main`. When `main` returns, the hook still runs destroy callbacks. If you close in `main` yourself, `close()` drops the hook.

```java
try (ConfigurableApplicationContext ctx =
             new AnnotationConfigApplicationContext(AppConfig.class)) {
    // use beans
}
```

**Listing 2.** Conceptual try-with-resources. `close()` runs when the block exits.

For non-web apps the reference **tells you to register the hook** so singletons actually get destroy methods when the process dies. Spring Boot’s `SpringApplication.setRegisterShutdownHook` defaults to **`true`**. Web `ApplicationContext` implementations already close when the web app shuts down (`ContextLoaderListener.contextDestroyed` closes the **root** `WebApplicationContext`).

```d2
direction: down
paths: "close()  or  JVM hook" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
doclose: "doClose()" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
stop: "LifecycleProcessor\nstop (regular shutdown)" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
destroy: "Destroy cached singletons" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}

paths -> doclose -> stop -> destroy
```

**Fig. 1.** Regular close: `Lifecycle` / `SmartLifecycle` **stop** first, then singleton destroy (`@PreDestroy`, `DisposableBean`, `destroy-method`). `doClose()` also publishes `ContextClosedEvent`. On a cancelled refresh or stop timeout, destroy can run **without** a preceding stop. See [[What destroy callbacks does Spring invoke when a bean is destroyed]].

`stop()` on the context is **not** close. Stopped `Lifecycle` beans can be started again. After `close()`, the context has reached end of life ([[What is the difference between close and refresh on ApplicationContext]]).

Prototype beans are assembled and handed off; the container does **not** run their destroy callbacks on context close.

> [!warning] No hook and no `close()` means no `@PreDestroy`
> A standalone `ClassPathXmlApplicationContext` that you never close and never hook will skip singleton destruction when the JVM exits. Web containers and Boot’s default hook hide this; a plain `main` does not.

> [!warning] Parent contexts keep running
> Closing a child does not close its parent. Each context has its own lifecycle. Closing also does not destroy prototype instances the client still holds.

> [!tip] Interview answer
> Hold a ConfigurableApplicationContext and call close, or registerShutdownHook in a non-web main so the JVM does it. Close destroys cached singletons and publishes ContextClosedEvent; it does not close the parent. Web apps close with the servlet context. Stop is a pause of Lifecycle beans, not the same as close.
