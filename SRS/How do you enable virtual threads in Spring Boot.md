<!--
reps: 0
priority: 0
-->
#Java/Concurrency/VirtualThreads #Java/Spring/Boot/Properties #SRS

# How do you enable virtual threads in Spring Boot?

> [!abstract] Short answer
> On **Java 21+**, set **`spring.threads.virtual.enabled=true`** (default **`false`**). That activates `Threading.VIRTUAL`, so auto-configured **Tomcat** / **Jetty** request handling, **`SimpleAsyncTaskExecutor`**, and **`SimpleAsyncTaskScheduler`** use virtual threads. Pool knobs such as `server.tomcat.threads.max` then **do nothing**. Current Boot docs **strongly recommend Java 24+**. Pair long-running **`@Scheduled`** apps with **`spring.main.keep-alive=true`**.

## One flag, several auto-configs

`Threading.VIRTUAL` is active only when the property is **`true` and** the JVM is **Java 21 or later**. On an older JDK the flag is a no-op: `Threading.PLATFORM` stays active ([[How would you explain Virtual Threads]]).

```properties
spring.threads.virtual.enabled=true
spring.main.keep-alive=true
```

**Listing 1.** Enablement. YAML is `spring.threads.virtual.enabled: true`. `spring.main.keep-alive` (default **`false`**) keeps the JVM up when every remaining thread is a **daemon** — virtual threads **are** daemons, so a process that only runs `@Scheduled` work can otherwise **exit**.

With the flag on, Boot’s task auto-configuration no longer builds a `ThreadPoolTaskExecutor` / `ThreadPoolTaskScheduler`. It builds **`SimpleAsyncTaskExecutor`** and **`SimpleAsyncTaskScheduler`** that start a virtual thread per task. Those beans cover `@EnableAsync` (unless you supply `AsyncConfigurer`), MVC async `Callable` handling, WebFlux **blocking** execution, GraphQL async, WebSocket channels, and JPA / `ApplicationContext` bootstrap executors.

```d2
direction: down
flag: "spring.threads.virtual.enabled=true\nJava 21+" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
enum: "Threading.VIRTUAL" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
servers: "Tomcat VirtualThreadExecutor\nJetty factory customizer" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
tasks: "SimpleAsyncTaskExecutor\nSimpleAsyncTaskScheduler" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

flag -> enum
enum -> servers
enum -> tasks
```

**Fig. 1.** The same Environment switch. Tomcat’s `TomcatVirtualThreadsWebServerFactoryCustomizer` installs a `VirtualThreadExecutor` on the protocol handler; Jetty’s `JettyVirtualThreadsWebServerFactoryCustomizer` does the equivalent ([[How do you switch the embedded server from Tomcat to Jetty]]). This is **not** “Netty’s event loop becomes virtual threads.”

```properties
# Ignored once virtual threads are enabled:
server.tomcat.threads.max=200
server.tomcat.threads.min-spare=10
server.jetty.threads.min=8
spring.task.execution.pool.max-size=16
spring.task.scheduling.pool.size=2
```

**Listing 2.** Official appendix wording: those pool properties **don’t have an effect if virtual threads are enabled**. Virtual threads run on the **JVM-wide** carrier pool, not on a Boot-sized executor. Inflating Tomcat’s `max` “just in case” does not buy headroom.

> [!warning] `@Scheduled` will not keep the JVM alive
> The auto-configured scheduler thread is a **virtual (daemon)** thread. If the app has no other non-daemon threads, the JVM **exits**. Set **`spring.main.keep-alive=true`** when the process is supposed to sit there running scheduled work ([[What is the SpringApplication class]]).

> [!warning] Pinning can *drop* throughput
> Boot tells you to read the JDK virtual-thread notes before flipping the flag. **Pinned** virtual threads can make an app **slower**; detect them with JDK Flight Recorder or **`jcmd`**. Current reference docs **strongly recommend Java 24+** (carrier pinning around `synchronized` is a known older-JDK issue — [[How would you explain Virtual Threads synchronized]]). Enabling virtual threads is not a substitute for measuring, and it is not an automatic reason to drop WebFlux ([[When should you use WebFlux versus Spring MVC versus virtual threads]]).

> [!tip] Interview answer
> I set spring.threads.virtual.enabled to true on Java 21 or newer — Boot 4 docs prefer 24. That turns on Threading.VIRTUAL so Tomcat or Jetty handle requests on virtual threads and Boot swaps the auto-configured executor and scheduler to SimpleAsync* types. Thread-pool properties stop applying. If the process lives on @Scheduled work I also set spring.main.keep-alive, because virtual threads are daemons and the JVM would otherwise exit.
