<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS

# How do you use schedulers in Spring Boot?

> [!abstract] Short answer
> Put **`@EnableScheduling`** on a `@Configuration` (often the `@SpringBootApplication` class). Annotate a Spring bean method with **`@Scheduled`**: **`fixedDelay`** (gap after the previous run **finishes**), **`fixedRate`** (gap between **start** times), or a **six-field** Spring **`cron`**. Boot then auto-configures a **`TaskScheduler`** (`ThreadPoolTaskScheduler` by default, pool size **1**). Virtual threads swap in **`SimpleAsyncTaskScheduler`** and **ignore** pool properties.

## `@EnableScheduling` turns on the processor; Boot supplies the pool

Framework: `@EnableScheduling` registers the infrastructure that finds `@Scheduled` methods. Boot’s **`TaskSchedulingAutoConfiguration`** then creates a scheduler **when that infrastructure is present** and you have not already defined a `TaskScheduler` / `ScheduledExecutorService` / `SchedulingConfigurer` ([[How do ConditionalOn annotations drive auto-configuration]]). `@Scheduled` alone on a method does **nothing** without `@EnableScheduling`.

```java
@SpringBootApplication
@EnableScheduling
public class SchedulerDemoApplication {

	public static void main(String[] args) {
		SpringApplication.run(SchedulerDemoApplication.class, args);
	}
}
```

**Listing 1.** Enablement. The method must live on a **container bean** (typically `@Component`). Return values are ignored. Multiple `@Scheduled` on one method are **independent** triggers and **may overlap**.

```java
@Scheduled(fixedDelay = 5, timeUnit = TimeUnit.SECONDS)
void afterPreviousFinishes() { }

@Scheduled(initialDelay = 1, fixedRate = 5, timeUnit = TimeUnit.SECONDS)
void fromStartToStart() { }

@Scheduled(cron = "0 0 9-17 * * MON-FRI", zone = "Europe/Berlin")
void weekdaysNineToFive() { }
```

**Listing 2.** Delay vs rate (default unit **milliseconds** if you omit `timeUnit`). **`initialDelay` only** = run **once**. Cron is **second minute hour day-of-month month day-of-week** — **six** fields, not Unix five. `?` is allowed on day-of-month or day-of-week. Macros: **`@hourly`**, **`@daily`**, **`@weekly`**, **`@monthly`**, **`@yearly`**.

```properties
spring.task.scheduling.pool.size=2
spring.task.scheduling.thread-name-prefix=scheduling-
spring.task.scheduling.shutdown.await-termination=true
```

**Listing 3.** Default **`pool.size=1`**: every `@Scheduled` method shares **one** thread, so a slow task **blocks** the others. `await-termination` default **`false`**. With **`spring.threads.virtual.enabled=true`** the scheduler is **`SimpleAsyncTaskScheduler`**; **pool keys have no effect**. Virtual scheduler threads are **daemons** — pair long-running `@Scheduled` apps with **`spring.main.keep-alive=true`** ([[How do you enable virtual threads in Spring Boot]]). `SimpleAsyncTaskScheduler` still runs **`fixedDelay`** work on **one** scheduler thread; Framework recommends **fixed-rate or cron** when you want virtual-thread concurrency.

```d2
direction: down
enable: "@EnableScheduling" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
boot: "TaskSchedulingAutoConfiguration\nTaskScheduler" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
ann: "@Scheduled\nfixedDelay / fixedRate / cron" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

enable -> boot -> ann
```

**Fig. 1.** You enable annotations; Boot sizes the scheduler (`spring.task.scheduling`). Implement **`SchedulingConfigurer`** only if you need a custom `Trigger`. Actuator **`scheduledtasks`** lists what was registered ([[How do you monitor an application with Spring Boot Actuator]]).

> [!warning] One thread is the default, and cron is six fields
> Interview dumps that show `fixedRate = 2000` without saying **milliseconds from start-to-start** mix it up with **`fixedDelay`**. A five-field crontab (`0 * * * *`) is **not** a Spring expression. `@Configurable` + a registered `@Scheduled` bean **double-schedules** the method.

> [!warning] Virtual threads will not keep the JVM alive
> The auto-configured scheduler thread is a **daemon**. A process that only runs `@Scheduled` work can **exit** unless **`spring.main.keep-alive=true`**. Do not raise `pool.size` “for Loom” — those properties are ignored.

> [!tip] Interview answer
> I add @EnableScheduling, then @Scheduled on a Spring bean: fixedDelay from the previous finish, fixedRate from the previous start, or a six-field Spring cron. Boot auto-configures a TaskScheduler — one thread unless I set spring.task.scheduling.pool.size. With virtual threads I get SimpleAsyncTaskScheduler and I set spring.main.keep-alive so the JVM does not exit.
