<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What happens at build time in Quarkus?

> [!abstract] Short answer
> After `javac` finishes, Quarkus runs **augmentation**: extensions' build steps discover beans on a Jandex index, resolve the CDI container layout, validate and record configuration, generate proxies and bootstrap bytecode (Gizmo), and collect native-image metadata. The result is an artifact that starts from recorded state instead of rediscovering it — the mechanism behind [[Why does Quarkus start faster than a typical Spring Boot application]].

## The augmentation pipeline

Quarkus reads your classes through **Jandex** annotation indexes (not runtime classpath scanning), then executes the **build-step graph**: each extension's deployment artifact declares `@BuildStep` methods that consume and produce **build items**, and the plugins wire the steps into a dependency-ordered plan. Steps do not run arbitrary code at boot; they **record** instructions, and the recorder (Gizmo) generates the bytecode that will replay them during STATIC_INIT or RUNTIME_INIT phases. Classes needed only for the build stay out of the runtime artifact.

```d2
direction: down
javac: "javac compiles app classes" {
  width: 260
  height: 60
  style.fill: "#e3f2fd"
}
jandex: "Jandex index\nannotations, no scanning" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
steps: "Build-step graph\n@BuildStep produce/consume items" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
rec: "Recorders + Gizmo\ngenerated bootstrap bytecode" {
  width: 290
  height: 80
  style.fill: "#fff3e0"
}
art: "Artifact\nfast jar or native executable" {
  width: 290
  height: 70
  style.fill: "#e8f5e9"
}
javac -> jandex -> steps -> rec -> art
```

**Fig. 1.** Augmentation is a separate phase after compilation. The same pipeline prepares native-image metadata, which is why native builds need no hand-written reflection JSON for Quarkus-managed code ([[How does Quarkus support GraalVM native images]]).

## What a build step looks like

```java
// Extension deployment code (runs inside the augmentation phase, not in your app)
@BuildStep
@Record(ExecutionTime.RUNTIME_INIT)
void bindGreetingService(CodeGenContext context) {
    // consumes/produces build items; writes recorded bootstrap instructions
}
```

**Listing 1.** Conceptual shape of a deployment-time step (extension internals, not application code): `@BuildStep` marks the method, `@Record(...)` selects the init phase whose replay will execute the recorded calls. Application code never writes this; it only benefits from it ([[What is a Quarkus extension]]).

Configuration is processed here too: properties are bound and validated during the build, and values marked build-time are recorded into the artifact ([[What is the difference between build-time and runtime configuration in Quarkus]]). For applications the visible artifacts of augmentation are the `target/quarkus-app` fast-jar layout (jar builds) and the runner binary (native builds).

> [!warning] "Build time" is not "compile time" and augmentation is not optional
> A plain `javac` or an IDE quick-build does **not** run augmentation — starting a half-built artifact fails with missing augmentation output, and IDEs delegate to the Quarkus plugins for that reason. This phase is also why adding an extension or changing build-time config requires a **full rebuild**, not a hot reload ([[How does Quarkus dev mode work]]).

> [!tip] Interview answer
> After normal compilation Quarkus runs augmentation: extensions execute build steps over a Jandex index, the CDI container layout is resolved, configuration is validated and recorded, and Gizmo generates the bootstrap bytecode. The artifact then boots by replaying those recorded steps instead of scanning and wiring at runtime. It is the core architectural move of Quarkus — work happens once in the build, startup only executes it.
