<!--
reps: 0
priority: 0
-->
#Java/Quarkus #Java/Spring/Boot #SRS

# Why does Quarkus start faster than a typical Spring Boot application?

> [!abstract] Short answer
> Because most of the work a Boot application does **on every startup** — classpath discovery, CDI/Spring context assembly, proxy generation, configuration validation — Quarkus does **once, at build time**, and stores the result as recorded bytecode. Booting becomes "execute the precomputed program graph": fewer classes loaded, no runtime classpath scanning, no annotation parsing, beans created lazily. A minimal fast-jar app boots in under a second on the JVM (measured 0.792s on JDK 21 with Quarkus 3.39.2); a native executable boots in tens of milliseconds.

## Where the time goes instead

At startup a Spring Boot app builds its `ApplicationContext` live: component scan, `@Conditional` evaluation, bean definition registration, reflection-driven wiring ([[What is @SpringBootApplication]], [[How does Spring Boot auto-configuration decide which beans to create]]). Quarkus' augmentation phase performs bean discovery on a precomputed **Jandex** index, resolves the [[What is ArC in Quarkus|ArC]] container layout, generates proxies and bootstrap code (Gizmo), and validates configuration — so boot only starts the HTTP layer and replays recorded init steps ([[What happens at build time in Quarkus]]).

```d2
direction: down
scan: "Runtime discovery\nclasspath scan + conditions" {
  width: 270
  height: 80
  style.fill: "#ffebee"
}
wire: "Runtime wiring\nreflection, proxies, parsers" {
  width: 260
  height: 80
  style.fill: "#ffebee"
}
serve: "Serve" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
idx: "Build-time index & resolution\nJandex, bean layout, config" {
  width: 290
  height: 80
  style.fill: "#e8f5e9"
}
rec: "Recorded bytecode in artifact" {
  width: 280
  height: 60
  style.fill: "#e8f5e9"
}
boot: "Boot: HTTP up + replay\n(lazy proxies per call)" {
  width: 270
  height: 70
  style.fill: "#e8f5e9"
}
scan -> wire -> serve
idx -> rec -> boot
```

**Fig. 1.** Left path repeats at every Boot startup; right path is paid once at build. Lazy instantiation shifts the rest: normal-scoped beans appear on first method call through a proxy ([[What is ArC in Quarkus]]).

## Measured shape

```java
// java -jar target/quarkus-app/quarkus-run.jar   (fast jar, Quarkus 3.39.2, JDK 21)
// INFO  [io.quarkus] (main) quarkus-check 1.0.0-SNAPSHOT on JVM
//       (powered by Quarkus 3.39.2) started in 0.792s. Listening on: http://0.0.0.0:8080
// INFO  [io.quarkus] (main) Profile prod activated.
// curl http://localhost:8080/hello -> Hello from Quarkus REST
```

**Listing 1.** Boot log of the minimal scaffolded application: the "started in" line reports JVM boot well under one second, in the same range as the official getting-started output (0.968s). [[What is Spring Boot]]'s equivalent minimal app reports seconds, because it assembles its context at boot.

Three costs explain the remaining gap versus native: class loading of the runtime libraries, JIT warmup, and heap accounting. Native mode removes all three at the price of a slow, memory-hungry build ([[How does Quarkus support GraalVM native images]]).

> [!warning] The cost is moved, not deleted — and startup is not throughput
> Augmentation makes builds notably slower than plain `javac`, and configuration marked build-time is **frozen** into the artifact; changing it requires a rebuild or re-augmentation ([[What is the difference between build-time and runtime configuration in Quarkus]]). Also, "starts fast" does not mean "serves fast": peak sustained throughput on the JVM still benefits from JIT optimization, which native mode trades away.

> [!tip] Interview answer
> Quarkus shifts framework work to the build: bean discovery, proxies and config validation happen during augmentation and are stored as recorded bytecode, so at boot it just opens the HTTP port and replays those steps — no classpath scanning, no live context assembly. That is why sub-second JVM startup is real, and native mode pushes it to tens of milliseconds. The trade-off is slower builds and build-time-only configuration, not free speed.
