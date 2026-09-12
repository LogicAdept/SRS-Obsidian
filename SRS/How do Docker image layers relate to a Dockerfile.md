<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# How do Docker image layers relate to a Dockerfile

> [!abstract] Short answer
> Roughly one instruction — one layer. Filesystem-carrying instructions (`RUN`, `COPY`, `ADD`) each record a diff of what they changed as a new read-only layer; other instructions (`ENV`, `WORKDIR`, `EXPOSE`, `CMD`, `ENTRYPOINT`) add metadata-only configuration instead. The image is a manifest of those layers; at runtime one writable layer is added for the container.

## Instruction by instruction

Each layer stores only the delta against the layer below, so layers are small, shareable between images (every image reusing `eclipse-temurin:21-jre` shares its layers), and cacheable — the cache rules are in [[How does the Docker build cache work]].

```dockerfile
FROM eclipse-temurin:21-jre          # layer 0: base image layers
WORKDIR /app                          # metadata only
COPY target/app.jar app.jar           # filesystem layer 1
ENV JAVA_OPTS="-XX:MaxRAMPercentage=75"  # metadata only
CMD ["java", "-jar", "app.jar"]       # metadata only (command)
```

**Listing 1.** Only the `COPY` line adds filesystem content here; the rest rides along as image config. `docker history app:1.0` prints exactly this layer-by-layer provenance.

```d2
direction: down
l1: "base image layers (JRE)\nread-only, shared" {
  width: 330
  height: 80
  style.fill: "#e3f2fd"
}
l2: "COPY app.jar -> layer (diff)\nread-only" {
  width: 330
  height: 80
  style.fill: "#e8f5e9"
}
w: "container writable layer\ncreated per docker run" {
  width: 330
  height: 80
  style.fill: "#fff3e0"
}
l1 -> l2: "image"
l2 -> w: "+ runtime"
```

**Fig. 1.** The stack: shared read-only image layers from the Dockerfile, plus the per-container writable layer on top (served by the overlay filesystem — [[How does the overlay2 storage driver work]]).

Because every layer survives in the image, a Dockerfile is also an audit trail: whatever an instruction puts down stays in that layer.

> [!warning] Deleting a file in a later layer does not shrink the image
> `RUN curl -o secret.pem ... && rm secret.pem` in *one* `RUN` is safe; downloading in one `RUN` and deleting in the next is not — the file is baked into the earlier layer and the "deletion" only adds a whiteout in the new one. The same trap leaks credentials copied in and later removed, which is one reason `.dockerignore` ([[What is a .dockerignore file for]]) and multi-stage builds ([[How would you explain Multi-stage build]]) exist.

> [!tip] Interview answer
> **A Dockerfile is a build recipe where filesystem instructions become read-only image layers — one diff per RUN/COPY/ADD — while config instructions become image metadata. Layers stack, are shared and cached across images, and the running container adds its own writable layer. Deleting a file in a later layer never removes it from an earlier one.**

