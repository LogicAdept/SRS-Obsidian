<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What is the difference between ARG and ENV in a Dockerfile

> [!abstract] Short answer
> `ARG` is a build-time variable: passed with `--build-arg`, usable by instructions that follow its declaration, gone from the container's runtime environment. `ENV` is a runtime variable: baked into the image config, present in `docker run` for every process, inherited by downstream stages and images.

## Lifetime and visibility

`ARG APP_VERSION=1.0` can parameterize `FROM`, `RUN`, and other instructions at build time. `ENV JAVA_OPTS=...` is substituted at build time too, but the variable is then recorded in image configuration and exported to the container process — which is why framework tuning like `-XX:MaxRAMPercentage` is commonly delivered through `ENV` and read by the JVM at startup ([[How does the JVM detect container memory and CPU limits]]).

```dockerfile
ARG BASE=eclipse-temurin:21-jre       # build-time: parameterizes FROM
FROM ${BASE}
ARG BUILD_PROFILE=dev                  # usable by subsequent RUNs only
RUN test "$BUILD_PROFILE" = "dev" || echo "release build"
ENV JAVA_OPTS="-XX:MaxRAMPercentage=75"  # runtime: visible to java in the container
ENTRYPOINT ["sh", "-c", "exec java $JAVA_OPTS -jar app.jar"]
```

**Listing 1.** ARG drives the build; ENV reaches the running process. Shell form is used in the ENTRYPOINT precisely so `$JAVA_OPTS` expands at container start — the exec form would pass it literally.

An ARG can be promoted: `ARG` after `FROM` re-declares stage scope (before `FROM` it is only usable in `FROM` lines), and `ENV B=$A` snapshots a build arg into the runtime environment.

> [!warning] Build args leak through image history
> The Dockerfile reference is explicit: do not pass secrets as build arguments — they are visible in `docker history` output and in provenance attestations. A secret baked into a layer cannot be removed by a later layer either ([[How do Docker image layers relate to a Dockerfile]]). Use BuildKit's `RUN --mount=type=secret` for credentials during the build.

> [!tip] Interview answer
> **ARG exists only during the build and is fed by --build-arg; ENV persists in the image and is exported to the container's process. Use ARG to parameterize base images and build steps, ENV to deliver runtime configuration. And never ship secrets as ARG — docker history exposes them.**

