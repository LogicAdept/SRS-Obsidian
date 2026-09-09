<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How do you run code at application startup in Quarkus?

> [!abstract] Short answer
> Three build-in ways: **observe `StartupEvent`** (`void onStart(@Observes StartupEvent ev)` on any bean), annotate a bean with **`@Startup`** so the container instantiates it eagerly at boot, or use an **init task** (`QuarkusApplication` main / `@QuarkusMain` for full control of the main method). All of them run in the runtime-init phase — after recorded static init, before the app serves traffic. Shutdown mirrors it with `ShutdownEvent`.

## The mechanisms and their order

An `@Observes StartupEvent` method is the idiomatic hook: when the container finishes building, Quarkus fires the event and every observer runs — and because observers force instantiation of the declaring bean, this is also the standard trick to **eagerly initialize** lazy beans ([[What bean scopes does Quarkus support]]). `@Startup` states the same intent declaratively on the bean class (or producer): the container creates the instance during startup instead of on first use. `@QuarkusMain` replaces the generated main class with yours (`Quarkus.run(...)` inside still boots the container) — used for CLI-style apps that need to drive the lifecycle themselves. Shutdown: `@Observes ShutdownEvent` fires during graceful stop; in JVM mode `@Initialized(ApplicationScoped.class)` fires close to `StartupEvent`, but in native images `@Initialized(ApplicationScoped.class)` fires **during the native build**, while `StartupEvent` fires when the image actually runs — the documented reason to prefer `StartupEvent`.

```java
// src/main/java/org/acme/check/obs/AppLifecycle.java (JDK 21, Quarkus 3.39.2)
package org.acme.check.obs;

import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;

@ApplicationScoped
public class AppLifecycle {
    void onStart(@Observes StartupEvent ev) {
        System.out.println("STARTUP-EVENT observed, app name from event: "
                + ev.getClass().getSimpleName());
    }
}
// Boot output of `java -jar target/quarkus-app/quarkus-run.jar` (verbatim lines):
// 2026-09-09 23:15:30,496 INFO  [io.quarkus] (main) quarkus-check 1.0.0-SNAPSHOT on JVM
//   (powered by Quarkus 3.39.2) started in 3.214s. Listening on: http://0.0.0.0:8080
// STARTUP-EVENT observed, app name from event: StartupEvent
// 2026-09-09 23:15:30,496 INFO  [io.quarkus] (main) Profile prod activated.
// The observer ran inside the same boot window, after the container was recorded and built.
```

**Listing 1.** An observer method fires during startup with zero extra configuration — no `beans.xml`, no listener registration; ArC found the method on the Jandex index at build time ([[What is Jandex in Quarkus]]).

```d2
direction: down
static: "Static init\nrecorded steps replayed" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
fire: "Container up\nStartupEvent fired" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
hooks: "@Observes StartupEvent\n@Startup beans instantiated\ninit tasks / QuarkusApplication.run" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}
serve: "HTTP serving begins" {
  width: 250
  height: 50
}
down: "ShutdownEvent observers" {
  width: 270
  height: 50
  style.fill: "#f5f5f5"
}
static -> fire -> hooks -> serve
serve -> down: "graceful stop"
```

**Fig. 1.** Everything user-visible happens between container build and first request; the shutdown event is the symmetric exit point ([[What are the bootstrapping phases of a Quarkus application]]).

## Choosing between them

Event observation composes: several beans can each react to `StartupEvent` without knowing about each other. `@Startup` expresses "this bean must exist and be ready early" (cache warmers, scheduled-job registration) and reads better than a fake observer. `@QuarkusApplication`/`Quarkus.run()` fits command-line tools that call `await().indefinitely()` or exit explicitly. For migration-critical work that must run only once per pod even with replicas, remember startup code runs **per instance** — leader election or a scheduler belongs to other mechanisms.

> [!warning] Observing StartupEvent is an eager-bean trigger, not a scheduler
> Because observers instantiate their beans, people accidentally pull entire dependency graphs into startup — boot time grows and a failing observer can prevent the app from starting at all. The reverse myth also appears: "put `@Scheduled` on it and it will warm the cache at boot" — scheduled tasks run on their schedule, not at startup. And in native images do not rely on `@Initialized(ApplicationScoped.class)`: it fires during the build, not at runtime — use `StartupEvent`.

> [!tip] Interview answer
> The standard hook is an @Observes StartupEvent method — the container fires it in the runtime-init phase, and observing forces eager instantiation of the bean, which is also how you warm up lazy beans. @Startup declares the same intent on the bean itself, and @QuarkusMain gives you the main method for CLI-style control; ShutdownEvent mirrors it on stop. One nuance worth saying: in native images StartupEvent fires when the image runs, while @Initialized(ApplicationScoped) fires during the build — so StartupEvent is the portable choice.
