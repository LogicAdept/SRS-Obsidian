<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is Jandex in Quarkus?

> [!abstract] Short answer
> Jandex is the bytecode **indexing library** Quarkus is built on: it reads compiled `.class` files and produces a compact in-memory index of annotations, classes, methods, fields and inheritance relationships. During augmentation, ArC bean discovery and every extension build step query that index instead of scanning the classpath with class loaders — this is how Quarkus "knows" which classes are beans, REST resources or config mappings without loading them at runtime.

## What the index contains and who consumes it

An index maps each class to its structural metadata: declared annotations (including targets), superclass/interfaces, methods and fields. The Quarkus build produces one synthetic index covering the application classes and its runtime dependencies; build steps receive it as a `CombinedIndexBuildItem` and search it for "classes implementing X", "subclasses of Y" or "things annotated with Z" — exactly the queries bean discovery and integrations need ([[What happens at build time in Quarkus]]). ArC resolves the CDI bean archive from the same index and builds the container layout; JPA, Jakarta REST, Scheduler, Fault Tolerance and practically every other extension find their annotated members the same way ([[What is ArC in Quarkus]]).

For third-party jars whose classes must be discovered (for example an annotated entity living in a shared library), the application indexes them either automatically or explicitly with `quarkus.index-dependency.*` properties in `application.properties` — a build-time declaration, not a runtime scan.

```java
// Build-time view: the index powers discovery of this repository bean
// (JDK 21, Quarkus 3.39.2; mvn test green, bean injected into resources and tests).
package org.acme.check.data;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped                                   // <- found via Jandex index
public class PersonRepository implements PanacheRepository<Person> {
    public List<Person> adults() {
        return find("age >= ?1", 18).list();
    }
}
// No beans.xml, no spring.factories, no runtime scanning: during augmentation ArC read
// @ApplicationScoped and PanacheRepository from the index and registered this bean.
// At runtime the container was already built - startup log showed no discovery phase.
```

**Listing 1.** A bean exists purely because its compiled class was indexed and matched a discovery rule. The same query power is what extensions use internally — for instance to locate all `@Scheduled` methods or all `HealthCheck` implementations.

```d2
direction: right
classes: ".class files\napplication + dependencies" {
  width: 220
  height: 70
}
index: "Jandex index\nannotations, hierarchy,\nmethods, fields" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
arc: "ArC\nbean discovery" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}
ext: "Extension build steps\nREST, JPA, Scheduler..." {
  width: 230
  height: 60
  style.fill: "#e8f5e9"
}
container: "Container layout +\nrecorded bootstrap" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
classes -> index: "offline indexing"
index -> arc
index -> ext
arc -> container
ext -> container
```

**Fig. 1.** Everything downstream of the index is a build-time query over precomputed metadata — which is why the runtime does none of it ([[What are the bootstrapping phases of a Quarkus application]]).

## Index libraries explicitly

When a jar is *not* indexed, its annotated classes are invisible to discovery. Extensions commonly fail with "class X is not a bean / cannot be found" for unindexed dependencies; the fix is the `quarkus.index-dependency.<name>.group-id/artifact-id` triple, or adding the `jandex-maven-plugin` to the library so it ships a `META-INF/jandex.idx` inside the jar. `@RegisterForReflection` and native metadata registration are related but separate concerns — they govern reflection for native images, not bean discovery.

> [!warning] "Jandex indexes source code" — no
> Jandex reads **compiled bytecode**, not Java sources, and its index is consumed **at build time only**. Two popular wrong answers follow from that confusion: claiming runtime classpath scanning still happens "somewhere", and claiming `beans.xml` controls discovery in Quarkus — annotated discovery from the index is the rule, and a `beans.xml` from an unindexed jar will not conjure the jar into the index.

> [!tip] Interview answer
> Jandex is Quarkus' class-indexing library. At build time it indexes the compiled application and its dependencies — annotations, hierarchy, members — and the whole build machinery works off that index: ArC discovers beans, extensions find their annotated classes, integrations wire themselves up. That replaces runtime classpath scanning entirely; if a third-party jar needs discovery, I declare it via quarkus.index-dependency or ship a jandex.idx inside it.
