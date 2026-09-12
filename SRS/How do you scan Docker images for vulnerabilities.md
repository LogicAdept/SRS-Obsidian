<!--
reps: 0
priority: 0
-->
#DevOps/Tools/Docker #Security/AppSec #SRS

# How do you scan Docker images for vulnerabilities

> [!abstract] Short answer
> A scanner builds an SBOM (the list of OS packages and libraries an image carries), matches it against CVE advisories, and reports findings by severity — `docker scout cves` does it natively, Trivy and Grype do it standalone. The only real fix is rebuilding on a patched base: you cannot patch a running image in place.

## How scanning actually works

Docker Scout analyzes each image layer, extracts installed packages and language dependencies, and correlates them with an advisory database; the result is a vulnerability report plus an SBOM you can export. A standalone scanner such as Trivy does the same offline against a locally synced advisory DB, which is what most CI pipelines use:

```bash
docker scout cves api:1.42                 # engine-native report
trivy image api:1.42                       # standalone, same idea
trivy image --severity HIGH,CRITICAL \
            --exit-code 1 api:1.42         # gate the pipeline
```

**Listing 1.** Two ways to run the same check: Scout is built into the Docker tooling, Trivy's `--exit-code 1` turns findings into a failing build step.

The findings come in three flavors worth separating in an interview answer: **OS packages** (the base image's OpenSSL, glibc, shell tools), **language dependencies** (the app's own libraries), and **misconfigurations** (running as root, no healthcheck, capabilities) that scanners flag alongside CVEs. Fixing the first class is a rebuild on a newer base — pinning the base by digest ([[What is the difference between an image tag and a digest]]) makes that reproducible; fixing the second is an application dependency update; the third is Dockerfile work. Image weight matters here too: fewer installed packages means fewer advisories to triage ([[How do you reduce the size of a Docker image]]).

```d2
direction: right
img: "image + layers" {
  width: 220
  height: 80
  style.fill: "#e3f2fd"
}
sbom: "SBOM\npackages + libraries" {
  width: 260
  height: 90
  style.fill: "#fff3e0"
}
cve: "CVE advisory DB\n(severity, fix version)" {
  width: 280
  height: 90
  style.fill: "#fff3e0"
}
rep: "report: filter by severity,\nfix = rebuild base or bump dep" {
  width: 340
  height: 100
  style.fill: "#ffebee"
}
img -> sbom
sbom -> cve
cve -> rep
```

**Fig. 1.** Scanning is SBOM against advisories; every remediation path ends in a new image build, not a patch on the old one.

> [!warning] A clean scan is a point-in-time opinion, not a property
> Advisories are published after images ship, so yesterday's clean scan says nothing about today's CVE — scanners must run on a schedule and on every build, not once. The inverse trap also holds: a scanner sees only what the image declares; a runtime zero-day or an exploited endpoint is invisible to it. And triage is part of the job: failing a pipeline on every LOW finding guarantees the gate gets switched off within a month.

> [!tip] Interview answer
> I scan images on every build and on a schedule: docker scout natively, or Trivy in CI with a severity threshold and exit-code gate. The scanner builds an SBOM, matches it against CVE advisories, and separates OS-package issues — fixed by rebuilding on a patched base — from app dependencies and config findings. I pin base images by digest so rebuilds are reproducible, and I keep images small because fewer packages means less triage. A scan is a point-in-time report, so the gate lives in the pipeline, not in a one-off check.
