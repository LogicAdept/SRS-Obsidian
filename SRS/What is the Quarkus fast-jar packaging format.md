<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is the Quarkus fast-jar packaging format?

> [!abstract] Short answer
> Fast-jar is the **default package type**: `mvn package` produces a **`target/quarkus-app/` directory** — `quarkus-run.jar` (the entry point), `app/` (your classes), `lib/` (dependencies), `quarkus/` (generated and transformed bytecode) — run with `java -jar target/quarkus-app/quarkus-run.jar`. Its layered layout plus a custom classloader give faster startup and lower memory than a single flat classpath or an uber-jar; the whole directory must travel together (containers copy it entirely). Uber-jar and native executable are opt-in alternatives.

## Layout and why it is fast

The directory split is the mechanism: `quarkus-run.jar` is a thin launcher whose manifest points at structured layers; the runtime classloader reads `app/`, `lib/` and `quarkus/` separately, so class loading starts from a precomputed index instead of scanning one giant jar — fewer file handles, better locality, and the generated `generated-bytecode.jar`/`transformed-bytecode.jar` carry the recorded bootstrap classes ([[What are the bootstrapping phases of a Quarkus application]]). The build also emits `quarkus-app-dependencies.txt` (the library list) for tooling. Because startup cost depends partly on class loading volume, the layout is a real contributor to the "starts in milliseconds-to-seconds" story — alongside the build-time work itself ([[Why does Quarkus use less memory than traditional Java stacks]]).

```java
// Verified packaging of this deck's demo application (JDK 21, Quarkus 3.39.2):
// $ mvn package -DskipTests
// $ ls target/quarkus-app/
// app                                 <- application classes
// lib                                 <- third-party jars (netty, vertx, ...)
// quarkus                             <- generated-bytecode.jar, transformed-bytecode.jar,
//                                        quarkus-application.dat
// quarkus-app-dependencies.txt
// quarkus-run.jar                     <- entry point
//
// $ java -jar target/quarkus-app/quarkus-run.jar
// 2026-09-09 23:15:30,496 INFO  [io.quarkus] (main) quarkus-check 1.0.0-SNAPSHOT on JVM
//   (powered by Quarkus 3.39.2) started in 3.214s. Listening on: http://0.0.0.0:8080
// 2026-09-09 23:15:30,496 INFO  [io.quarkus] (main) Profile prod activated.
// $ curl http://localhost:8080/demo/price/sku123
// 600
// Deploy = copy the WHOLE quarkus-app directory; missing files break the boot.
```

**Listing 1.** The layout as produced, then booted: a directory artifact, not a single jar — the Dockerfile.jvm the generator ships does exactly this copy before `java -jar`.

```d2
direction: down
mvn: "mvn package\n(default package type)" {
  width: 240
  height: 55
}
dir: "target/quarkus-app/\nquarkus-run.jar | app/ | lib/ | quarkus/" {
  width: 380
  height: 65
  style.fill: "#e3f2fd"
}
cl: "Layered classloader\nindexed startup, no uber classpath" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}
run: "java -jar quarkus-run.jar\ncopy the directory as a unit" {
  width: 320
  height: 60
}
alt: "Alternatives: uber-jar (one fat jar)\nnative executable (quarkus.native)" {
  width: 360
  height: 60
  style.fill: "#f5f5f5"
}
mvn -> dir -> cl -> run
dir -> alt
```

**Fig. 1.** Default path vs opt-in alternatives; uber-jar trades startup friendliness for deployment convenience ([[How does Quarkus support GraalVM native images]] is the third target).

## Deployment implications

Container images built from fast-jar (the provided Dockerfile.jvm) copy `quarkus-app/` wholesale and run the launcher — layer caching benefits because `lib/` changes less often than `app/`. Uber-jar (`quarkus.package.jar.type=uber-jar` in current docs, previously `quarkus.package.type`) exists for environments that insist on one artifact; the docs note its classloading is slower. Legacy-jar remains for exotic agents. The subtle interview point: fast-jar is not an executable-jar-in-the-java-se-sense — you cannot lift `quarkus-run.jar` out of the directory and expect it to run.

> [!warning] "quarkus-run.jar is self-contained" — it is not
> The launcher resolves its siblings by relative path: shipping only the jar (or restructuring the directory) is a guaranteed boot failure, and the error message rarely says "you copied the wrong thing". The mirrored confusion: calling the format "the fast jar" and assuming a magic inside — the speed comes from layout + recorded bootstrap + build-time work, not from a different bytecode format. Also property-name precision: the uber-jar switch moved across versions; quoting the old `quarkus.package.type` as current docs without checking dates you.

> [!tip] Interview answer
> The default packaging is the fast-jar: target/quarkus-app with quarkus-run.jar as entry point plus app, lib and quarkus directories — the quarkus layer carries generated and transformed bytecode from augmentation. A layered classloader indexes it, which helps startup and memory versus one flat classpath; deployment copies the whole directory, which is what the shipped Dockerfile.jvm does. Uber-jar and native executable are alternatives — uber-jar for single-artifact shops, native for the closed-world build.
