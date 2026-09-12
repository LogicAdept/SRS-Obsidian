<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #DevOps/Containerisation #SRS

# What are Docker containers and images at a high level

> [!abstract] Short answer
> An **image** is an immutable, versioned package of an application: a stack of read-only filesystem layers plus configuration (entrypoint, env, ports). A **container** is a running process instantiated from that image, adding one writable layer on top. Docker is the tooling (CLI client + daemon) that builds, ships, and runs those containers.

## The build / ship / run flow

Docker uses a client-server architecture: the `docker` client talks to the daemon (`dockerd`) over a REST API on a Unix socket or network interface, and the daemon does the actual building, pulling, and running. A `Dockerfile` describes how to build an image; the registry (Docker Hub by default) stores and distributes images; `docker run` turns an image into a container.

```d2
direction: right
build: "docker build\nDockerfile -> image" {
  width: 250
  height: 90
  style.fill: "#e3f2fd"
}
reg: "Registry\nDocker Hub / private\npush : pull <-" {
  width: 260
  height: 100
  style.fill: "#fff3e0"
}
run: "docker run\nimage + writable layer\n-> running container" {
  width: 260
  height: 100
  style.fill: "#e8f5e9"
}
build -> reg: "docker push"
reg -> run: "docker pull / run"
```

**Fig. 1.** Images are built once, pushed to a registry, and pulled anywhere; running a container layers a writable directory over the read-only image layers.

A minimal Java image builds and runs like this:

```dockerfile
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY target/app.jar app.jar
ENTRYPOINT ["java", "-jar", "app.jar"]
```

**Listing 1.** A Dockerfile whose image contains a pinned JRE plus one application JAR; `docker build -t app:1.0 .` produces the image, `docker run app:1.0` starts a container from it.

The image is the unit you version and promote: the same bytes (`app:1.0`) run identically in dev, CI, and production, which is why the deployment side of microservices builds on it ([[What is the service per container pattern]] pins one image per service). Building and running are decoupled by the registry, the same way CI separates build and deploy artifacts ([[How would you explain CI CD pipeline]]).

## What the container adds at runtime

When the daemon starts a container it combines the image's read-only layers with a fresh writable layer, sets up isolation (namespaces) and resource limits (cgroups) — the mechanics are in [[How does Docker isolate containers with Linux namespaces and cgroups]] and [[How does the overlay2 storage driver work]]. Writes go to the writable layer and disappear with the container; anything that must survive gets a volume.

> [!warning] "It ran in the container, so the data is there"
> The writable layer is ephemeral: `docker rm` destroys it. Files written inside a running container are not part of the image, and `docker commit`-style snapshots are the exception, not the workflow. Persistent data belongs in a volume ([[What is the difference between volumes and bind mounts in Docker]]), not in the container layer.

> [!tip] Interview answer
> **An image is the immutable artifact — layered filesystem plus startup config — that you build once and store in a registry. A container is a process created from that image: Docker adds a writable layer, isolates it with namespaces, and limits it with cgroups. Docker itself is the client-daemon tooling around that build-ship-run flow.**

