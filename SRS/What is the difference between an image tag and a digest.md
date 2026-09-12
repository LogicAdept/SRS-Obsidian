<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #SRS

# What is the difference between an image tag and a digest

> [!abstract] Short answer
> A tag (`eclipse-temurin:21-jre`) is a mutable, human-friendly pointer: anyone with push rights can re-point it to different bytes. A digest (`@sha256:...`) is the content hash of the image manifest — the same digest always resolves to the same bytes, so digest pinning is how builds become reproducible.

## Mutable pointer vs content address

Omitting the tag means `:latest` is assumed — which is just a default tag name, not a "newest" property, and nothing forces it to point at the latest anything. The registry stores manifests ([[What is the OCI and how does Docker relate to containerd and runc]] is where that format is standardized); the digest is computed over that manifest, which itself hashes layer contents, so pinning a digest pins the entire image (multi-architecture images fan out per-platform manifests under one index digest). The image a tag names is the layered artifact of [[What are Docker containers and images at a high level]].

```bash
docker pull eclipse-temurin:21-jre                       # mutable: whatever 21-jre means now
docker pull eclipse-temurin@sha256:9c1c5...d2e           # immutable: exact bytes, any time
docker push myapp:1.4.2
docker push myapp@sha256:7f0a1...44b                     # push by digest after buildx build --push
```

**Listing 1.** Tag pulls are convenient and unstable; digest pulls are verbatim and verifiable — CI pipelines promoting a build record its digest, not its tag.

```d2
direction: right
t1: "tag '21-jre'\n(yesterday) -> manifest A" {
  width: 320
  height: 80
  style.fill: "#fff3e0"
}
t2: "tag '21-jre'\n(today) -> manifest B\nre-pushed by vendor" {
  width: 320
  height: 80
  style.fill: "#ffebee"
}
d: "digest sha256:9c1c...\n-> manifest A, forever" {
  width: 360
  height: 80
  style.fill: "#e8f5e9"
}
t1 -> d: "same content"
```

**Fig. 1.** The tag moved; the digest did not. That is the entire reproducibility argument for pinning digests in Dockerfiles and deployment manifests.

> [!warning] Tags move under you — and :latest moves fastest
> A rebuilt base image under the same tag changes every derived build silently: layers re-download, scans flip red, and "it worked yesterday" has no bytes-level explanation. But digest pinning has a maintenance cost — digests do not receive CVE fixes until someone updates the pin, so pin-and-forget is also wrong; the workable pattern is digest pinned by tooling with automated update PRs ([[What is a CI CD pipeline]] is where that automation lives).

> [!tip] Interview answer
> **A tag is a mutable name for a manifest; a digest is the manifest's content hash and is immutable. Pulling by tag is convenient but non-reproducible — :latest is a default name, not a version promise. Production builds record and pull by digest, accepting the duty to bump pins deliberately for security fixes.**

