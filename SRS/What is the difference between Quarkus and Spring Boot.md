<!--
reps: 0
priority: 0
-->
#Java/Quarkus #Java/Spring/Boot #SRS

# What is the difference between Quarkus and Spring Boot?

> [!abstract] Short answer
> Both deliver a runnable Java service with DI, HTTP and production config, but the **work moves to a different phase**: Spring Boot performs **auto-configuration at every startup** (classpath scan, `@Conditional` evaluation, reflection, proxies), while Quarkus performs it **once at build time** and boots from recorded bytecode — its "compile time boot". Practical consequences: Quarkus starts in fractions of a second on the JVM and milliseconds natively with low RSS; Boot starts in seconds. Boot still wins on ecosystem depth and Spring-specific modules; Quarkus wins on startup, memory density and native support.

## The same problems solved at different times

Boot's magic is runtime auto-configuration: `@SpringBootApplication` triggers component scanning and `@Conditional` evaluation on every boot ([[What is @SpringBootApplication]], [[How does Spring Boot auto-configuration decide which beans to create]]). Quarkus runs the analogous discovery during **augmentation** — bean layout, proxy generation, config validation and native metadata are fixed in the artifact, and boot replays recorded steps ([[What happens at build time in Quarkus]]). That is the root of the startup and memory gap, not a faster JIT trick.

```d2
direction: right
sbbuild: "Spring Boot build\njar only" {
  width: 240
  height: 80
  style.fill: "#e3f2fd"
}
sbboot: "Every startup\nclasspath scan, conditions,\nproxies, beans" {
  width: 260
  height: 90
  style.fill: "#ffebee"
}
qbuild: "Quarkus build (augmentation)\nbean layout, config,\nproxies, native metadata" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
qboot: "Every startup\nreplay recorded steps,\nlazy proxies" {
  width: 250
  height: 80
  style.fill: "#e8f5e9"
}
sbbuild -> sbboot
qbuild -> qboot
```

**Fig. 1.** Boot discovers at startup; Quarkus discovers at build. The price moves, it does not disappear: Quarkus builds are slower and build-time configuration is frozen into the artifact ([[What is the difference between build-time and runtime configuration in Quarkus]]).

## What each is best at

- **Startup and memory:** Quarkus JVM boot is sub-second (the official getting-started log shows ~0.9s; a minimal fast-jar app measured 0.792s on JDK 21), native boot is tens of milliseconds. Boot 3 narrows this with AOT but keeps the runtime-discovery model ([[What changed in Spring Boot 3]]).
- **Ecosystem and team:** Boot has the largest extension and hiring ecosystem, richest Spring Security/Batch/Data surface ([[What is Spring Boot]]). Quarkus covers the Jakarta standards and MicroProfile APIs plus a broad extension catalog, but Spring-specific code needs real porting.
- **Native images:** Quarkus treats native as a primary target; extensions supply reflection and proxy metadata automatically ([[How does Quarkus support GraalVM native images]]).
- **Developer loop:** Quarkus dev mode live reloads and provisions test databases automatically ([[How does Quarkus dev mode work]], [[What are Dev Services in Quarkus]]).

> [!warning] Two popular lies
> "Quarkus is just Spring Boot copy-pasted" — false: the runtime architecture differs fundamentally (build-time DI vs runtime auto-configuration). "Quarkus cannot run Spring code" — also too strong: partial Spring API compatibility extensions exist, and plain CDI-like code ports easily; what does not move for free is deep Spring (Security filter chains, Batch, custom starters).

> [!tip] Interview answer
> Both give me a runnable service with DI, HTTP and external config. Boot wires everything at startup by scanning the classpath and evaluating conditions; Quarkus does that work once at build time and boots from recorded state, which is why it starts faster and uses less memory, especially natively. I choose Boot for ecosystem depth and team familiarity, Quarkus when startup, memory density or native builds are the constraint. Neither choice is free — Quarkus pays in build time and frozen build-time config.
