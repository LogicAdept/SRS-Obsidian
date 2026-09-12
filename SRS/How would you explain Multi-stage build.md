<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# How would you explain Multi-stage build

> [!abstract] Short answer
> A multi-stage build uses several `FROM` sections in one Dockerfile: early stages hold heavyweight toolchains (Maven, JDK, npm), and the final stage copies **only the build artifacts** out of them. The shipped image contains just the runtime — no compilers, caches, or build tools — so it is smaller and has a smaller attack surface.

## Stages, naming, and COPY --from

Stages are numbered from 0 or named with `FROM ... AS name`, and `COPY --from=stage` pulls selected paths out of an earlier stage. Everything not copied into the final stage is left behind — the SDK, the dependency cache, intermediate classes never reach the artifact.

```dockerfile
# syntax=docker/dockerfile:1
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /src
COPY pom.xml .
RUN mvn -B dependency:go-offline          # dependency layer caches until pom changes
COPY src ./src
RUN mvn -B package -DskipTests

FROM eclipse-temurin:21-jre AS runtime
RUN useradd -r app
USER app
WORKDIR /app
COPY --from=build /src/target/app.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Listing 1.** The canonical Java split: build in a Maven+JDK image, ship in a JRE-only image. The final image has no Maven, no sources, no local repository — and runs as a non-root user.

```d2
direction: right
b1: "stage: build\nmaven + JDK 21\npom, sources, ~/.m2" {
  width: 300
  height: 100
  style.fill: "#fff3e0"
}
arrow: "COPY --from=build\nonly app.jar" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
b2: "stage: runtime\nJRE 21 + app.jar" {
  width: 280
  height: 100
  style.fill: "#e8f5e9"
}
b1 -> arrow -> b2
```

**Fig. 1.** One Dockerfile, two images: the fat builder stays in CI, the slim runtime goes to the registry. Layer ordering (pom first, sources later) keeps dependency downloads cached — see [[How does the Docker build cache work]].

Because each stage is itself an image, you can also build only part of the pipeline (`docker build --target build`) for test images, and stages run in parallel when they do not depend on each other.

> [!warning] COPYing directories wholesale defeats the point
> `COPY --from=build /src/target/ ./target/` drags test-jars, `maven-status`, and build junk into the final image; copy the specific artifact. And a multi-stage Dockerfile does not fix a leaking layer inside a stage — anything committed in an earlier layer survives ([[How do Docker image layers relate to a Dockerfile]]), so secrets still need `--mount=type=secret` or a build-time ARG kept out of the final stage ([[What is the difference between ARG and ENV in a Dockerfile]]).

> [!tip] Interview answer
> **Multi-stage means several FROM stages in one Dockerfile: toolchain stages build the artifact, the final stage copies only that artifact via COPY --from. You ship a JRE-only image without Maven, sources, or caches — smaller, faster to pull, fewer CVEs. Name the stages, copy the exact artifact, and order layers pom-first so dependency downloads stay cached.**

