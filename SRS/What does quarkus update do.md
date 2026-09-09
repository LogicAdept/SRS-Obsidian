<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What does quarkus update do?

> [!abstract] Short answer
> `quarkus update` (CLI) / `mvn io.quarkus.platform:quarkus-maven-plugin:update` is the **upgrade automation command**: it bumps the platform version and then runs **OpenRewrite recipes** that rewrite the project across the release — dependency versions, renamed configuration keys, moved/renamed APIs and classes — producing a diff the developer reviews rather than a from-scratch migration. It automates "a subset" of the migration: the mechanical, well-mapped changes; design-level breaks still need human work.

## The mechanics of an automated upgrade

The command's engine is OpenRewrite — a rewrite engine with recipes that parse code into a lossless tree and apply transformations. Quarkus ships recipes per release that encode the migration matrix: new BOM alignment, config property renames (for example the packaging property relocations and the RESTEasy Reactive → Quarkus REST renames across 3.x), annotation moves, deprecated-API replacements in source and documentation. After the run, `git diff` shows exactly what changed; the update guide lists reasons expected rewrites can be missing (unparseable sources, custom code paths recipes cannot map, third-party extensions lagging the release). Running update **per minor stream** is the recommended rhythm — accumulate it and the eventual major-version jump shrinks to routine size.

```java
// Upgrade flow as documented (Quarkus 3.39.2 era), abridged:
//
// $ quarkus update                     # CLI form
//   -or-
// $ mvn io.quarkus.platform:quarkus-maven-plugin:3.39.2:update -N
//
// What the run did to this deck's demo project shape (representative, not verbatim):
//   pom.xml:                <quarkus.platform.version> -> next stream
//   application.properties: renamed quarkus.* keys rewritten
//   src:                    deprecated API usages replaced by current ones
//
// Post-update verification checklist (the guide's own advice):
//   1. mvn -q clean verify      # tests + ITs are the contract
//   2. review the git diff for property renames touching prod config
//   3. check third-party extensions resolved to platform versions
// (Conceptual listing: the command mutates the project; the verified run of this deck
//  executed builds/tests only - the update flow is quoted from the official update guide.)
```

**Listing 1.** Marked `Conceptual`: the command is a project mutation, not an app feature. The interview narrative: version bump + OpenRewrite recipes + reviewable diff, with tests as the acceptance gate ([[What is the Quarkus platform]] — the BOM is what makes the version bump meaningful).

```d2
direction: down
old: "Project on platform 3.3x\nextensions aligned" {
  width: 280
  height: 60
}
cmd: "quarkus update\nplatform bump + OpenRewrite recipes" {
  width: 340
  height: 65
  style.fill: "#fff3e0"
}
diff: "Reviewable git diff\nversions, config keys, APIs" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
human: "Human work\ndesign-level breaks, docs, review" {
  width: 320
  height: 60
  style.fill: "#e8f5e9"
}
new: "Project on new stream\nverify: mvn clean verify" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}
old -> cmd -> diff -> human -> new
```

**Fig. 1.** The command covers the mechanical lane; the developer covers judgment — and the test suite is the contract that the mechanical part is complete.

## Why this exists as a first-class command

Quarkus moves in minor streams with documented LTS lines; the ecosystem contract is that upgrades should be *routine*. Recipes turn tribal migration knowledge (which property renamed, which class moved package) into executable, versioned automation maintained by the project itself — the alternative being stale migration wikis. The same recipe infrastructure serves migration *between* frameworks in some Quarkiverse tooling, but the flagship use is platform upgrades ([[What does quarkus update do]] — this card's command — versus ad hoc `sed`-style migrations).

> [!warning] "quarkus update makes my code work on the new version" — only the mapped subset
> The guide says it plainly: the command automates only part of the migration. Assuming full coverage produces the classic incident — the update ran clean, tests were skipped, and an unmapped behavioral change (a renamed property the recipe missed because it lived in a generated file, or a third-party extension pinned outside the platform) surfaces in staging. Conversely, running update without a VCS diff review means accepting bulk rewrites blind. And recipes do not upgrade your third-party libraries beyond what the platform aligns.

> [!tip] Interview answer
> quarkus update is the upgrade command built on OpenRewrite: it bumps the platform BOM and runs release-specific recipes that rewrite dependency versions, renamed config keys and moved APIs into the new stream, leaving a reviewable diff. It automates only a subset — design-level changes and unmapped code still need me — so the discipline is: run it per minor stream, review the diff, and let mvn verify be the acceptance gate. The platform BOM is what makes a one-property version bump meaningful.
