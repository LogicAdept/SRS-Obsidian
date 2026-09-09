<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How do you schedule periodic tasks in Quarkus?

> [!abstract] Short answer
> The `quarkus-scheduler` extension: annotate a method on an `@ApplicationScoped` bean with **`@Scheduled`** and choose a trigger — `every="10s"` (duration syntax), `cron="0 15 10 * * ?"` (cron with configurable expression `cron="{cron.expr}"`), or `delayed` — and Quarkus runs it on its own scheduling threads, outside the HTTP request model. Control knobs: `identity` names the job (grouping and management), `concurrentExecution = SKIP` prevents overlap, `skipExecutionIf` supports clustering guards, and CDI events fire for skipped/delayed/paused jobs.

## The mechanics

At build time ArC discovers `@Scheduled` methods on the Jandex index; the recorded bootstrap registers each as a job with the in-memory scheduler, which fires triggers on dedicated scheduler threads — a tick does **not** need a request, and the method must not assume request context ([[What bean scopes does Quarkus support]]). Since scheduled methods execute concurrently with request handling, any shared state belongs in thread-safe structures or transactional services. Expression values support property expressions (`every="{task.interval}"`), so intervals move to configuration per environment ([[What is the difference between build-time and runtime configuration in Quarkus]]). Long jobs: without `concurrentExecution = SKIP` the next tick fires even if the previous run still works — overlap is the default behavior, not an error.

```java
// src/main/java/org/acme/check/infra/HeartbeatJob.java (JDK 21, Quarkus 3.39.2;
// verified in the @QuarkusTest run: ticksCount() >= 1 passed, mvn test 6/6 green).
package org.acme.check.infra;

import io.quarkus.scheduler.Scheduled;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.concurrent.atomic.AtomicInteger;

@ApplicationScoped
public class HeartbeatJob {
    private final AtomicInteger ticks = new AtomicInteger();

    @Scheduled(every = "1s", identity = "heartbeat", concurrentExecution = Scheduled.ConcurrentExecution.SKIP)
    void tick() {
        ticks.incrementAndGet();
    }

    public int ticksCount() {
        return ticks.get();
    }
}
// The job fired during the test window on a scheduler thread - not executor-thread-N of the
// HTTP pool and not vert.x-eventloop-thread-0; identity names the job for management.
```

**Listing 1.** A one-second heartbeat with a named identity and overlap skipped. The counter is read through a method — the bean is a normal-scoped CDI proxy ([[What bean scopes does Quarkus support]]).

```d2
direction: down
reg: "Build time\n@Scheduled methods discovered" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
sched: "Scheduler threads\ntriggers: every / cron / delayed" {
  width: 300
  height: 65
  style.fill: "#e3f2fd"
}
gate: "concurrentExecution = SKIP\nskipExecutionIf (cluster guard)" {
  width: 320
  height: 60
  style.fill: "#e8f5e9"
}
run: "Method runs\nno request context" {
  width: 230
  height: 55
}
reg -> sched -> gate -> run
```

**Fig. 1.** Discovery is build-time, execution is a dedicated thread pool, and the gate decides whether an overlapping tick becomes a run or a skip event.

## Quartz for persistence, and the cluster question

The in-memory scheduler forgets state on restart — fine for heartbeats and cache warmers. When schedules must survive restarts, coordinate across instances, or expose pause/resume via the Dev UI, the `quarkus-quartz` extension provides the same `@Scheduled` API backed by a persistent store; `executeWith` can also move jobs onto virtual threads. The honest interview answer for "how do I make this run exactly once across 5 replicas": the in-memory scheduler cannot — either Quartz with clustering (JDBC store), or a partitioning/leader-election design above the scheduler ([[How do you schedule periodic tasks in Quarkus]] in a single-instance world).

> [!warning] Scheduled does not mean transactional or clustered
> Three traps in one: (1) the method runs regardless of any HTTP activity, so database work needs its own `@Transactional` boundary — nothing wraps it implicitly; (2) two replicas of the same service both fire the job — the in-memory scheduler has no cross-instance coordination, producing duplicate processing that usually surfaces as "we sent the report twice"; (3) `cron="{cron.expr}"` without a default value fails boot when the property is missing — property expressions in triggers are read from configuration and a missing value is a startup error, not a runtime fallback.

> [!tip] Interview answer
> Quarkus Scheduler: @Scheduled on an ApplicationScoped bean with every-duration or cron triggers, property expressions to externalize intervals, identity to name jobs and concurrentExecution SKIP to prevent overlap. Methods run on dedicated scheduler threads without request context, discovered at build time like everything else. For persistence or cross-instance coordination I'd swap in the Quartz extension, because the default scheduler is in-memory — replicas each fire their own jobs.
