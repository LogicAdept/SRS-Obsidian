<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What is a SNAPSHOT version in Maven

> [!abstract] Short answer
> **`-SNAPSHOT` marks the moving development version of a release line: `1.0-SNAPSHOT` is "the latest code toward 1.0", with no stability guarantee. A release — any version without the suffix — is unchanging. During a release, `1.0-SNAPSHOT` becomes `1.0` and development moves to `1.1-SNAPSHOT`.** Snapshots are re-checked against the remote; releases resolve once and are cached forever.

## One suffix, two resolution behaviors

A release artifact is immutable: once `1.0` is in the local repository, Maven does not re-fetch it — only genuinely missing releases are re-checked, and only with the forced-update flag. A snapshot is a pointer to the latest build of the line: Maven compares the locally cached snapshot's timestamp against the remote's `maven-metadata.xml` and fetches the newer one. The metadata file records each deployed snapshot build, so two builds of `1.0-SNAPSHOT` on different days can be different artifacts under the same version string.

```d2
direction: right
dev: "1.0-SNAPSHOT\nmoving target:\nre-checked against remote" {
  width: 300
  height: 110
  style.fill: "#fff3e0"
}
rel: "1.0\nrelease:\nunchanging" {
  width: 220
  height: 90
  style.fill: "#e8f5e9"
}
next: "1.1-SNAPSHOT\nnext development line" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
dev -> rel: "release process cuts it"
rel -> next: "development continues"
```

**Fig. 1.** The release process renames the current snapshot into the release and opens the next snapshot line — the snapshot is "older" than its release.

How often the remote is consulted is configurable per repository through `updatePolicy`; the local cache still serves the artifact between checks:

```xml
<repositories>
    <repository>
        <id>snapshots-only</id>
        <url>https://repo.example.com/internal</url>
        <snapshots>
            <!-- always | daily (default) | interval:X | never -->
            <updatePolicy>daily</updatePolicy>
        </snapshots>
    </repository>
</repositories>
```

**Listing 1.** The documented choices for `updatePolicy`: `always`, `daily` (the default), `interval:X` in minutes, or `never`. For one-off certainty the CLI flag `mvn -U` (`--update-snapshots`) forces a check for missing releases and updated snapshots.

> [!warning] "Same version" never means "same bits" for a snapshot
> The interview trap is treating `1.0-SNAPSHOT` as a normal version that happens to end oddly. Two machines building an hour apart can compile against different snapshot jars, so a build can break overnight with zero changes on your side — the definition of a non-reproducible build. Hence the hygiene: snapshots are for the development dialogue between producer and consumer (and CI builds of the producer), while anything pinned — a consumer's POM, a release tag, a deployed application — depends only on released versions. "It worked yesterday" plus a green diff is the classic snapshot signature; `mvn -U` plus the metadata timestamps is how you find out what moved. The resolution mechanics behind the re-check: [[How does Maven resolve artifacts from repositories]]; the command that installs a snapshot locally: [[How would you explain mvn clean install]]; why CI pipelines prefer immutable inputs: [[Which CI CD tools do you know]].

> [!tip] Interview answer
> **A SNAPSHOT is the development version of a release line — 1.0-SNAPSHOT means the latest build toward 1.0, and it can change under you; the release 1.0 is immutable. Maven caches releases once but re-checks snapshots against the remote by default daily, or on demand with -U. I use snapshots only between actively developed modules or CI feeds, and pin releases anywhere reproducibility matters — a release process turns 1.0-SNAPSHOT into 1.0 and opens 1.1-SNAPSHOT.**

