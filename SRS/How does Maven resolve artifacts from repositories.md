<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# How does Maven resolve artifacts from repositories

> [!abstract] Short answer
> **There are exactly two repository types: local — the `~/.m2/repository` directory that caches downloads and holds your installs — and remote — Central by default, or an internal company server. A dependency missing locally is fetched from the configured remote and cached; `settings.xml` redirects the machinery: a different `localRepository`, mirrors of Central, offline mode, and credentials.**

## The resolution flow

When a build needs `groupId:artifactId:version`, Maven checks the local repository first: a cached release resolves immediately with no network. A miss triggers a download from the remote — Central unless the POM's `<repositories>` or the settings define otherwise — and the artifact is cached under its coordinate-shaped path. Snapshots are the exception to cache-forever: the remote is consulted again for a newer build of the same version.

```d2
direction: down
need: "Resolve G:A:V" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
local: "Local ~/.m2 repository\nhit?" {
  width: 280
  height: 90
  style.fill: "#e8f5e9"
}
remote: "Remote repository\nCentral, mirror, or internal" {
  width: 320
  height: 90
  style.fill: "#fff3e0"
}
cache: "Cache locally,\nresolve from disk" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}
fail: "Could not find artifact\nBUILD FAILURE" {
  width: 280
  height: 80
  style.fill: "#ffebee"
}
need -> local
local -> cache: "hit (release)"
local -> remote: "miss / newer snapshot"
remote -> cache
remote -> fail: "not found anywhere"
```

**Fig. 1.** Releases: one fetch, cached forever. Snapshots: re-checked against the remote. Everything else is a local-disk lookup.

`~/.m2/settings.xml` (or the global one in the Maven installation) carries the per-machine configuration that must stay out of the POM: `localRepository` (default `${user.home}/.m2/repository` — build servers often relocate it to a shared path), `mirrors` (a `<mirror>` with `mirrorOf>central` reroutes all Central traffic; mappings like `*,!inhouse` exclude internal repositories), `offline` plus the CLI switch `mvn -o` for builds that must not touch the network, and `servers` holding credentials keyed by an `id` that POMs and deploy commands reference.

```xml
<settings>
    <mirrors>
        <mirror>
            <id>company-central</id>
            <url>https://nexus.example.com/repository/public/</url>
            <mirrorOf>central</mirrorOf>
        </mirror>
    </mirrors>
</settings>
```

**Listing 1.** A corporate mirror: every request Maven would send to Central goes to the internal Nexus instead, which proxies Central and adds the company's own artifacts.

> [!warning] "install published it" and the mirror that hides things
> Two recurring lies. First: putting an artifact into the local repository — via `install` — publishes nothing; it serves exactly one machine, and teammates still need a deployed artifact on a remote. Second: a POM that declares its own `<repositories>` (or a settings mirror) silently overrides where artifacts come from — when dependencies "are not being found", the guide's first suspect is an overridden remote repository, not a missing artifact. Central's contents change independently of your build, which is why serious setups proxy it through an internal repository (Nexus, Artifactory) instead of scraping it wholesale. What happens after the fetch — transitive POMs and conflicts: [[How does Maven resolve transitive dependencies and conflicts]]; publishing for the team: [[How do you use your own library in another Java project]]; the command whose install phase lands artifacts in `~/.m2`: [[How would you explain mvn clean install]].

> [!tip] Interview answer
> **Maven has a local cache at ~/.m2 and remote sources — Central by default. Resolution is local-first: a release hit never touches the network, a miss downloads and caches, and snapshots re-check the remote for newer builds. Per-machine behavior lives in settings.xml: localRepository, mirrors of Central, offline mode, and server credentials by id. In companies, an internal Nexus proxies Central and hosts private artifacts — the POM stays clean.**

