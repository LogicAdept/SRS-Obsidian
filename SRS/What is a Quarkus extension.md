<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is a Quarkus extension?

> [!abstract] Short answer
> An extension is Quarkus' unit of integration: a **pair of Maven artifacts** — a **runtime** jar (the API and classes your application sees) and a **deployment** jar (build steps, recorders and native-image metadata consumed during augmentation). Your project depends only on the runtime artifact; the build tool plugin pulls the deployment counterpart automatically. Extensions "configure, boot and integrate" a technology, and they carry the GraalVM metadata so the same application builds natively without hand-written reflection JSON.

## Two artifacts, one dependency

The deployment artifact contains `@BuildStep` processors that run in the augmentation phase and produce the recorded bootstrap bytecode; the runtime artifact contains whatever must exist at runtime (APIs, runtime recorders, integration classes). The dependency direction is strictly one-way: **deployment may depend on runtime, never the reverse** — a runtime-to-deployment dependency would drag build machinery into every application.

```d2
direction: down
user: "Application pom\nio.quarkus:quarkus-hibernate-orm" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
rt: "Runtime artifact\nAPIs, runtime classes" {
  width: 250
  height: 70
  style.fill: "#e8f5e9"
}
dep: "Deployment artifact\n@BuildStep, recorders, native metadata" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
aug: "Augmentation\nbuild items wired, bytecode recorded" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
art: "Artifact boots replaying recorded steps" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}
user -> rt
user -> dep: "plugin-resolved,\nnever declared"
dep -> aug -> art
```

**Fig. 1.** Users declare the runtime GAV; the Maven/Gradle plugin resolves the deployment sibling for augmentation. The plugins even validate the graph and warn about missing deployment dependencies of your own custom extensions.

## What extensions contribute

At build time their steps consume and produce **build items**, discover beans on the Jandex index, bind configuration (each documented property, including whether it is build-time-fixed), and register reflection/proxy/resource metadata for native compilation. At runtime the artifact replays the recorded steps — that is how a database pool or the HTTP layer comes up without runtime discovery ([[What happens at build time in Quarkus]]).

```java
// application-side view: an extension is just a dependency...
// <dependency>
//   <groupId>io.quarkus</groupId>
//   <artifactId>quarkus-hibernate-orm</artifactId>
// </dependency>
// ...but augmentation reads its deployment jar to wire beans, config and native metadata.
```

**Listing 1.** Conceptual view (not compiled): from the application's perspective adding an extension is a normal dependency; the interesting half — the deployment jar — is resolved by the Quarkus plugin and never appears in your build file.

The catalog lives at quarkus.io/extensions and code.quarkus.io; every extension carries a maturity status — **stable** (backward compatibility taken seriously), **preview** (no compatibility guarantees yet) or **experimental** — so a team can judge risk before adopting ([[What is Quarkus]]).

> [!warning] "Extension" is not "library"
> Adding a plain library jar gives you classes; adding an extension gives you **build-time integration** — recorded wiring, config binding and native metadata. That is also why extensions cannot be swapped at runtime, why version bumps go through the platform BOM (extensions are versioned with the Quarkus platform), and why an extension's configuration has a documented build-time/runtime split ([[What is the difference between build-time and runtime configuration in Quarkus]]).

> [!tip] Interview answer
> An extension is two jars: the runtime artifact my code depends on, and a deployment artifact the Quarkus plugin pulls in that runs build steps during augmentation — bean discovery, config binding, recorded bootstrap and native-image metadata. Dependencies point one way: deployment may reference runtime, never the reverse. Extensions ship with a maturity status and are versioned with the platform, and they are the reason a Quarkus app needs no hand-written GraalVM reflection configuration.
