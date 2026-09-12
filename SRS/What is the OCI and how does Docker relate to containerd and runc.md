<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #DevOps/Containerisation #SRS

# What is the OCI and how does Docker relate to containerd and runc

> [!abstract] Short answer
> The Open Container Initiative (2015, founded by Docker, CoreOS and others under the Linux Foundation) owns three specs: **image-spec** (the image format), **runtime-spec** (how to run an unpacked filesystem bundle), and **distribution-spec** (the registry API). Docker donated its format and its runtime `runc` to seed them; today Docker Engine is a client/daemon UX layer over `containerd`, which invokes an OCI runtime (`runc`) to actually start containers.

## The stack under the CLI

When you `docker run`, the CLI calls the daemon's API; the daemon delegates to containerd (supervision, snapshots) which executes runc with an OCI bundle; runc — the reference OCI runtime — talks to the kernel to create the namespaces/cgroups process. Any OCI-compliant runtime can therefore run any OCI image: that is why the same image runs in Docker, Podman, containerd-native, CRI-O, or a Kubernetes cluster ([[What are Docker containers and images at a high level]] is the image/container split; [[What is the difference between an image tag and a digest]] is the registry side).

```d2
direction: down
cli: "docker CLI\n(build, run, compose)" {
  width: 280
  height: 80
  style.fill: "#e3f2fd"
}
dd: "dockerd\nAPI, build, networking, volumes" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
ctd: "containerd\nsupervision, snapshots, transfer" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
runc: "runc (OCI runtime-spec)\nunpacked bundle -> process" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
k: "Linux kernel: namespaces + cgroups" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
cli -> dd -> ctd -> runc -> k: "one run, four layers"
```

**Fig. 1.** Docker is the experience layer; the container itself is born in runc per the OCI runtime spec.

The specs are the contract that de-commoditizes the tooling: image-spec lets registries and builders interoperate (BuildKit, Kaniko, Jib build OCI images without Docker at all — [[How do you deploy a Spring Boot application]] may never touch a Dockerfile), distribution-spec is what every registry API implements, runtime-spec is what runc, crun, and friends implement.

> [!warning] "Docker image" is a colloquialism — and Docker is not the runtime of record
> Saying "Docker image" is fine, but the portable artifact is an OCI image: nothing in the format belongs to Docker Inc. The inverse matters for interviews: Kubernetes removed Docker Engine as a supported runtime (containerd/CRI-O remain), and **nothing about your images changed** — because Kubernetes always talked to an OCI-compatible layer, not to the Docker brand. Docker-the-tool stays a developer UX; the specs carry the portability.

> [!tip] Interview answer
> **OCI standardizes three things: image format, runtime contract, and distribution API — launched in 2015 with Docker's format and runc donated as the reference runtime. Under docker CLI sits dockerd, under it containerd, and runc turns the OCI bundle into the actual namespaced process. So images are portable across Docker, Podman, containerd, Kubernetes — the tool is swappable, the spec is the contract.**

