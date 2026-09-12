<!--
reps: 0
priority: 0
-->
#Security/CICD #SRS

# What is an SBOM

> [!abstract] Short answer
> A Software Bill of Materials (SBOM) is a **machine-readable inventory of the components that make up a software artifact** - direct and transitive dependencies, versions, licenses, and relationships - shipped alongside the build. NIST SP 800-218 makes it an SSDF practice: PW.4.4 calls for "provenance data for all components of each software release (e.g., in a software bill of materials [SBOM])", and the NTIA minimum elements it references define the baseline fields. The payoff is answering "are we affected by CVE X?" from inventory instead of archaeology.

## The minimum elements and formats

The NTIA baseline every useful SBOM carries: **supplier, component name, component version, unique identifiers, dependency relationships, author and timestamp**. Two formats dominate:

- **SPDX** (Linux Foundation, ISO-standardized) and **CycloneDX** (OWASP-origin, security-oriented) - both represent components and dependency graphs; tooling converges on supporting both.
- An SBOM is generated at build time from the actual dependency resolution - a lockfile is the input side; the SBOM is the *published, consumable* statement including transitive closure and relationships.

```d2
direction: right
b: "Build\nresolves deps" { width: 160; height: 70; style.fill: "#e3f2fd"
sb: "SBOM published\nSPDX / CycloneDX" { width: 240; height: 80; style.fill: "#fff3e0"
cve: "New CVE lands" { width: 170; height: 70; style.fill: "#ffebee"
ans: "Match SBOM -> affected builds\nin minutes, not days" { width: 300; height: 80; style.fill: "#e8f5e9"
b -> sb -> ans
cve -> ans
```

**Fig. 1.** The operational point: the inventory already exists when the vulnerability news breaks - matching is a query, not a fire drill ([[What is the difference between CVE and CVSS]] supplies the identifiers being matched).

## What it is used for

- **Vulnerability response**: next Log4Shell arrives, the SBOM tells which services ship the library and at which versions - the difference between a targeted hotfix and an org-wide grep.
- **Supply-chain provenance**: SSDF PW.4's umbrella - reused components are well-secured and their provenance recorded; paired with signed builds and artifacts it evidences that what was built is what was shipped ([[How do you scan Docker images for vulnerabilities]] produces image-level SBOMs).
- **License and compliance posture**: the same inventory answers license obligations; regulators and large buyers increasingly request SBOMs as delivery hygiene.

> [!warning] "We generate an SBOM, so we have supply-chain security"
> Generating is the easy half: an SBOM nobody consumes goes stale and answers nothing - the value is in the pipeline that regenerates it per release and the tooling that matches new CVEs against it automatically. And completeness matters: transitive dependencies, OS packages, and non-library blobs are the parts naive generators miss - the report that says "zero components" for your base image is lying ([[What is DevSecOps]] is the framework that makes SBOM consumption a practice rather than an artifact).

> [!tip] Interview answer
> An SBOM is the machine-readable ingredient list for a build - components, versions, relationships, in SPDX or CycloneDX, with NTIA's minimum elements as the floor. SSDF PW.4.4 asks for exactly this provenance. Its payoff is response speed: a new CVE becomes a query against known inventory, and the honest caveat is that an SBOM nobody regenerates and matches is just a stale file.
