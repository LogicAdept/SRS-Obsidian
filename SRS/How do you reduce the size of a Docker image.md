<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# How do you reduce the size of a Docker image

> [!abstract] Short answer
> An image is the sum of its layers, so every file any layer ever added is inside it — deleted files in later layers do not free space. The levers: a minimal base image (slim, Alpine, distroless), multi-stage builds that copy only the artifact, combining install and cleanup into one `RUN` layer, a small build context via [[What is a .dockerignore file for]], and for JVM apps a `jlink`-trimmed runtime instead of the full JDK.

## Layer arithmetic first

Each `RUN`/`COPY` instruction adds a layer that captures the filesystem delta. When one layer installs 300 MB of build tools and a later layer deletes them, the image still carries them — the deletion is a whiteout record on top, not an undo ([[How does the overlay2 storage driver work]] explains the mechanics). That is why "install, use, delete in a later step" fails, while "install and clean in the **same** RUN" works:

```dockerfile
# Wrong: 100+ MB of apt lists and compilers stay in layers
RUN apt-get update
RUN apt-get install -y gcc python3
RUN rm -rf /var/lib/apt/lists/*

# Right: one delta, cleaned before the layer commits
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc python3 \
 && rm -rf /var/lib/apt/lists/*
```

**Listing 1.** The same end state, two different images: layer boundaries, not file operations, decide the size.

## The big levers

**Multi-stage builds** keep compilers, caches, and test dependencies in a builder stage and `COPY` only the artifact into the runtime stage — often a 10× drop for JVM images ([[How would you explain Multi-stage build]]). **Base image choice** moves the floor: a full JDK image carries shell, package manager, and hundreds of libraries; slim variants strip locales and tools; distroless images ship only the runtime and no shell or package manager at all, which also shrinks the attack surface. The build docs push exactly this order: multi-stage, then the smallest base that satisfies the runtime, then dependency hygiene like `--no-install-recommends`.

For JVM services there is a fourth lever: `jlink` assembles a custom runtime with only the JDK modules the app uses, so a Spring Boot service can run on tens of MB of runtime instead of a full JDK. Combined with a layered-jar layout, application-only changes also reuse cached base layers ([[How does the Docker build cache work]]).

```d2
direction: right
b: "builder stage\nJDK + compilers + deps" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
a: "artifact\n.jar / binary" {
  width: 220
  height: 80
  style.fill: "#fff3e0"
}
r: "runtime stage\nJRE (jlink) + artifact" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
j: "compilers, apt caches,\nmaven repo never copied" {
  width: 320
  height: 90
  style.fill: "#ffebee"
}
b -> a: "COPY --from"
b -> j: "stays in builder"
a -> r
```

**Fig. 1.** Only the artifact crosses the stage boundary; build-time weight is stranded in the builder image.

> [!warning] Alpine is not a free win for JVM workloads
> Alpine is musl-libc based, not glibc. Native-JNI code, glibc-linked binaries, and some DNS/locale behaviors differ; modern Temurin provides Alpine builds, but a misbehaving musl image costs more debugging time than it saves MB. The pragmatic ladder for Java services: slim Debian base → distroless java → jlink runtime, verifying native dependencies at each step — not "switch to Alpine" reflexively.

> [!tip] Interview answer
> Size is the sum of layers, so I attack it in order: multi-stage build so compilers never reach the final image; a minimal base — slim, distroless, or a jlink-trimmed JVM runtime; one RUN per install-clean pair, because deleting files in a later layer frees nothing; and .dockerignore to keep junk out of the context. I also check the pull cost against the runtime need — an image is a transport unit as much as a runtime.
