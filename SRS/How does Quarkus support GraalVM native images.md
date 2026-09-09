<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How does Quarkus support GraalVM native images?

> [!abstract] Short answer
> Native support is structural, not an afterthought: `./mvnw package -Dnative` produces a **native executable** (application + libraries + a reduced SubstrateVM base) in which startup is tens of milliseconds and RSS is minimal. This works because Quarkus already satisfies the closed-world requirements — DI resolved at build time, no runtime classpath scanning, and **extensions programmatically register** reflection, proxy and resource metadata so you almost never maintain GraalVM JSON configs. Supported distributions: Oracle GraalVM (CE/EE) and **Mandrel**, a downstream of GraalVM CE built from OpenJDK sources and recommended for Linux container targets.

## Why Quarkus fits the closed world

A native build cannot discover anything at runtime: reflection only works for registered elements, dynamic class loading is out. Quarkus' augmentation already computes the bean layout, proxies and bootstrap code ahead of time ([[What happens at build time in Quarkus]], [[What is ArC in Quarkus]]), and the extension model funnels every integration's native metadata into the build — that is the official answer to "why does Quarkus do so much at build time".

```d2
direction: down
jar: "JVM mode\nfast jar + HotSpot" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
warm: "Fast boot (~1s), JIT warmup,\nbest peak throughput" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
nat: "Native mode\npackage -Dnative -> runner binary" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
nboot: "Boot tens of ms, low RSS,\nno JIT warmup, slower build" {
  width: 290
  height: 80
  style.fill: "#e8f5e9"
}
jar -> warm
nat -> nboot
```

**Fig. 1.** The two run modes trade opposite properties: JVM wins peak throughput via JIT; native wins boot time, RSS and cold-start density — the decision is per workload, not global.

## Building and distributions

The native build runs GraalVM's native-image inside the augmentation; without a local GraalVM/Mandrel, `./mvnw package -Dnative -Dquarkus.native.container-build=true` drives a builder container instead (the usual CI route). Mandrel is the recommended distribution for Linux containers; for macOS or Windows desktop targets Oracle GraalVM builds are the documented path. The produced executable contains the application code, required libraries, the Quarkus runtime services and a reduced VM base — which is precisely what makes the "smaller VM base" startup benefit official rather than anecdotal.

```java
// Build:   ./mvnw package -Dnative -Dquarkus.native.container-build=true
// Run:     ./target/quarkus-check-1.0.0-SNAPSHOT-runner
// (the runner is the executable; no JVM is installed on the host at runtime)
```

**Listing 1.** Conceptual command shape from the native guide (not executed in this environment — no container runtime here): the artifact is a host executable, not a jar; container-image packaging steps are documented separately in the same guide.

> [!warning] Native is not strictly better
> Peak throughput typically ends up **below JIT** for long-running hot code, builds are slow and memory-hungry, and some platform features narrow (reflection only via registration, dynamic proxies at build time, finalization differences). Also, JVM-mode profiling intuition does not transfer: GC and compiler behavior differ ([[What is the JVM]]). The honest rule: pick native for cold-start and memory-density requirements (serverless, scale-to-zero, dense pods), stay on the JVM for compute-heavy long-running services ([[When should you use Quarkus instead of Spring Boot]]).

> [!tip] Interview answer
> Quarkus fits native images because its architecture is already closed-world: beans, proxies and config are resolved at build time, and extensions register reflection and proxy metadata programmatically, so a native build needs almost no hand-written GraalVM config. package -Dnative emits a runner executable with a reduced VM that boots in tens of milliseconds with low RSS. The trade-offs are slow builds and peak throughput below JIT, so native is for cold-start-sensitive, memory-dense deployments and the JVM mode remains for throughput work.
