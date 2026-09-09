<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# How do you create a new Quarkus project?

> [!abstract] Short answer
> Three equivalent entry points: the web generator at **code.quarkus.io** (pick extensions, download the zip), the **Quarkus CLI** (`quarkus create app com.acme:demo`), and the **Maven plugin goal** (`mvn io.quarkus.platform:quarkus-maven-plugin:create -DprojectGroupId=... -DprojectArtifactId=...`). All three produce the same layout — a plain Maven/Gradle project, `pom.xml` importing the platform BOM, `src/main/java` with a generated resource, `application.properties`, and a `@QuarkusTest` — no parent POM and no archetype juggling. The Gradle variant uses the same generator flags.

## What the generator actually produces

The generated project depends on the **platform BOM** rather than pinned extension versions — every extension pulled later inherits the aligned version ([[What is the Quarkus platform]]). The build file declares extensions as plain dependencies (`quarkus-rest`, `quarkus-arc`, ...); the Quarkus Maven plugin (with `<extensions>true</extensions>`) resolves each one's *deployment* artifact automatically during augmentation — you never declare deployment jars yourself ([[What is a Quarkus extension]]). Layout: `org.acme.GreetingResource` with a `/hello` endpoint, a matching `GreetingResourceTest` marked `@QuarkusTest`, an empty `application.properties`, Dockerfile.jvm / Dockerfile.legacy-jar / Dockerfile.native under `src/main/docker`, and the Maven wrapper. First run is `./mvnw compile quarkus:dev` — no separate container step.

```java
// Project skeleton produced by the generator (Quarkus 3.39.2 platform), then verified:
// $ mvn io.quarkus.platform:quarkus-maven-plugin:3.39.2:create \
//       -DprojectGroupId=org.acme -DprojectArtifactId=quarkus-check \
//       -Dextensions="rest"
// $ cd quarkus-check && ./mvnw quarkus:dev
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
// curl http://localhost:8080/hello -> Hello from Quarkus REST   (dev mode, live reload on)
```

**Listing 1.** The one endpoint the skeleton ships with; the same class is covered by a generated `@QuarkusTest` that hits `/hello` and asserts the body — the test runs against the same augmentation artifacts as the app ([[How do you test a Quarkus application]]).

```d2
direction: right
web: "code.quarkus.io\npick extensions in the browser" {
  width: 240
  height: 70
}
cli: "Quarkus CLI\nquarkus create app G:A:V" {
  width: 250
  height: 70
}
mvn: "Maven plugin\nquarkus-maven-plugin:create" {
  width: 250
  height: 70
}
proj: "Same project skeleton\nBOM import, resource + test,\ndockerfiles, wrapper" {
  width: 300
  height: 80
  style.fill: "#e8f5e9"
}
dev: "./mvnw quarkus:dev" {
  width: 230
  height: 50
}
web -> proj
cli -> proj
mvn -> proj
proj -> dev
```

**Fig. 1.** The three entry points differ only in ergonomics; the artifact is the same BOM-aligned skeleton, so teams can mix them without divergence.

## Adding extensions afterwards

`quarkus extension add quarkus-hibernate-orm-panache` (CLI) or `./mvnw quarkus:add-extension -Dextensions="..."` edits the pom for you and restarts the dev-mode process on the fly — the dev loop detects pom changes. Extensions added this way keep platform versions; typing a version manually is what creates the dependency-drift problems the platform exists to prevent.

> [!warning] A version pin on a Quarkus extension is a smell
> The platform BOM fixes tested combinations of every core extension; overriding one version (say, a transitive RESTEasy or Vert.x bump) quietly moves you off the tested matrix and breaks the "one version upgrade for everything" property. The other common trap: copying an old tutorial that references `quarkus-resteasy` (the classic blocking stack) when the current default stack is Quarkus REST — the generator picks current artifacts, hand-copied poms often do not.

> [!tip] Interview answer
> I scaffold with the generator — code.quarkus.io, the Quarkus CLI quarkus create app, or the Maven create goal; they emit the same project: platform BOM import, extension dependencies, a hello resource with a QuarkusTest, Dockerfiles and the wrapper. From there it is mvnw quarkus:dev with live reload, and new extensions go in via quarkus extension add so they stay on platform versions instead of hand-pinned ones.
