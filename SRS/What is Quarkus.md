<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is Quarkus?

> [!abstract] Short answer
> Quarkus is a **full-stack Java framework** built around **build-time processing**: it resolves as much framework work as possible during the build (DI wiring, configuration, native-image metadata) so the runtime boots fast and stays small. It is **standards-based** (Jakarta REST, CDI, JPA, MicroProfile APIs) on top of a **Vert.x reactive core**, treats **Kubernetes** and **GraalVM native executables** as first-class targets, and is positioned as "Supersonic Subatomic Java". Current generation is **Quarkus 3.x** (Jakarta namespace); current line **3.39**, LTS streams **3.33** and **3.27**.

## What it is made of

Quarkus is not a new language runtime — the working parts come from the established ecosystem (Hibernate ORM, Eclipse Vert.x, Netty, RESTEasy). What Quarkus adds is the **augmentation machinery**: every capability is packaged as an [[What is a Quarkus extension|extension]] with a runtime part and a build-time part, and the DI layer is **ArC**, a build-time CDI Lite container ([[What is ArC in Quarkus]]). Configuration is unified through one system of sources and profiles ([[How do you configure a Quarkus application]]).

```d2
direction: down
app: "Your application\nREST resources, CDI beans, config" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
q: "Quarkus layer\nextensions + ArC + config + dev tooling" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
std: "Standards implementations\nJakarta REST, CDI Lite, JPA, MicroProfile" {
  width: 320
  height: 80
  style.fill: "#e3f2fd"
}
core: "Eclipse Vert.x + Netty\nreactive core" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
rt: "HotSpot JVM  or  native executable" {
  width: 320
  height: 60
  style.fill: "#ffebee"
}
app -> q -> std -> core -> rt
```

**Fig. 1.** Quarkus sits between your code and proven libraries; the same artifact tree targets JVM or native mode. The reactive core under the stack is why the HTTP layer can run blocking and non-blocking endpoints side by side ([[How does Quarkus unify imperative and reactive programming]]).

## The smallest official app

```java
package org.acme;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Path("/hello")
public class GreetingResource {

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String hello() {
        return "Hello from Quarkus REST";
    }
}
```

**Listing 1.** The getting-started endpoint, verbatim shape. `@Path` / `@GET` are Jakarta REST annotations, not Quarkus-specific ones. Scaffolded from code.quarkus.io, it boots on the JVM in under a second and answers on `http://localhost:8080/hello` ([[How does Quarkus dev mode work]]).

Projects are scaffolded from **code.quarkus.io** or the Maven archetype; `quarkus-bom` imports let you omit extension versions. The license is Apache 2.0 and artifacts are on Maven Central, so it drops into normal Maven/Gradle builds.

> [!warning] Not an application server and not a Spring clone
> There is no deployed container you drop WARs into — Quarkus builds a **runnable jar or native executable** with just the framework parts your code touches. And while a Spring-style compatibility layer exists (`spring-di`, `spring-web`, `spring-data-jpa`), it is **partial**: deep Spring-specific code does not move for free ([[What is the difference between Quarkus and Spring Boot]]). Also false is "Quarkus is only for microservices" — the docs never define it that way, and a plain JVM-mode monolith is a normal use.

> [!tip] Interview answer
> Quarkus is a build-time-oriented Java framework: DI, configuration and native-image metadata are resolved during the build, so startup is fast and the memory footprint small. It is standards-based — Jakarta REST, CDI, JPA — over a Vert.x reactive core, and it treats Kubernetes and GraalVM native as first-class targets. I would pick it where startup and memory density matter, and I would not describe it as either a Spring replacement or an application server.
