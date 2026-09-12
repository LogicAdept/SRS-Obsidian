<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #DevOps/CICD #SRS

# How do you run Docker builds in a CI CD pipeline

> [!abstract] Short answer
> A CI job needs access to a build engine, and there are three ways to get it: point the job at a **host daemon** by mounting `/var/run/docker.sock`, run a **dedicated daemon in Docker** (docker-in-docker, `--privileged`), or use **daemonless builds** with buildx's docker-container driver. Each is a trade between speed, cache sharing, and how badly a compromised job can hurt the host — with the socket mount being the most convenient and the most dangerous.

## The three access models

With the socket mount, the CI container talks to the host's Docker daemon over the Unix socket: builds are fast, images and caches are shared with the host, and every container the job runs is a sibling on the host — which also means the job can start a privileged container or read the host filesystem through a bind mount, because daemon access is host root ([[What does it mean to run a Docker container in privileged mode]] details why). Docker-in-docker starts a separate daemon inside a privileged CI container: clean isolation and a clean cache, at the cost of slower starts, storage overhead, and nested-runtime quirks. Buildx with the `docker-container` driver runs a BuildKit builder in its own container and needs no host daemon at all — it is the model the official CI docs push, together with explicit cache management:

```bash
docker buildx create --use --driver docker-container
docker buildx build \
  --cache-from type=registry,ref=registry/api:buildcache \
  --cache-to type=registry,mode=max,ref=registry/api:buildcache \
  --tag registry/api:1.42.0 \
  --push .
```

**Listing 1.** Daemonless CI build: the builder lives in a container, and the cache travels through the registry instead of living on a pet runner — builds stay reproducible on any agent ([[How does the Docker build cache work]] explains what the cache contains).

## What the pipeline owes the image

The build step earns its keep through what surrounds it: a tag per commit plus the release tag ([[What is the difference between an image tag and a digest]] — and push-by-digest makes artifacts immutable), a scan gate on the built image ([[How do you scan Docker images for vulnerabilities]]), multi-stage so build tooling never ships ([[How would you explain Multi-stage build]]), and registry credentials scoped to push/pull only — never baked into the image or its layers. Self-hosted runners additionally need the daemon's own hardening; the engine docs call the daemon socket the primary attack surface for exactly this reason.

```d2
direction: right
job: "CI job\n(no host daemon access)" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
builder: "BuildKit builder\n(own container)" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
cache: "registry cache\ncache-from / cache-to" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
reg: "push image by tag + digest" {
  width: 300
  height: 90
  style.fill: "#e8f5e9"
}
job -> builder
builder -> cache
builder -> reg
```

**Fig. 1.** The daemonless shape: the job drives an isolated builder; state lives in the registry, not on the runner.

> [!warning] Mounting the Docker socket hands the job root on the host
> The socket is the daemon's control plane: with it, a job — or malicious code in a dependency it installs — can run `--privileged` containers, bind-mount the host root, or create containers that outlive the job. It is also the standard advice on countless blogs, which is what makes it dangerous in an interview answer: name the risk, then prefer a scoped builder or dind on ephemeral runners. And "docker build is hermetic" is false — host daemons and shared caches leak state across jobs unless you isolate the builder and externalize the cache.

> [!tip] Interview answer
> For CI builds I use buildx with a docker-container BuildKit driver: no host daemon access, builder isolated in its own container, cache pulled and pushed through the registry so any ephemeral runner builds warm. The socket mount is fast but gives the job root on the host, and dind needs privileged isolation — both only with ephemerality and trust. Around the build: tag per commit, push by digest, scan the image, and keep build tooling in multi-stage so nothing leaks into the artifact.
