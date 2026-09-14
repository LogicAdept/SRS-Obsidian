<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What is a Maven archetype

> [!abstract] Short answer
> **An archetype is a packaged project template; `mvn archetype:generate` lists templates from a catalog, copies the chosen one with your `groupId`/`artifactId` substituted, and emits a ready-to-build project.** It is how new Maven projects and new plugin skeletons start without hand-writing the directory layout.

The archetype plugin turns "yet another project with the same structure" into one command. `archetype:generate` is the everyday goal: it reads an archetype catalog — the internal one shipped with the plugin, a local one, or a remote one — asks you to pick an entry (or takes `-DarchetypeGroupId`/`-DarchetypeArtifactId`/`-DarchetypeVersion` directly), fetches the archetype jar from the repository, and processes it into a working project with your coordinates ([[How would you explain Maven]] describes the coordinates themselves). The canonical quick start is the `maven-archetype-quickstart` artifact for a simple app.

## Goals beyond generate

```d2
direction: right
gen: "archetype:generate\nproject from template" {
  width: 280
  height: 90
  style.fill: "#e3f2fd"
}
cfp: "archetype:create-from-project\nreverse: project becomes a template" {
  width: 340
  height: 100
  style.fill: "#e3f2fd"
}
crawl: "archetype:crawl\nscan a repository, refresh catalog" {
  width: 320
  height: 100
  style.fill: "#fff3e0"
}
jar: "archetype:jar (package phase)\npackage the archetype artifact" {
  width: 330
  height: 100
  style.fill: "#fff3e0"
}
```

**Fig. 1.** Generate consumes templates; `create-from-project` plus `jar` produces them, and `crawl` keeps catalogs current.

Templates in both directions make archetypes the standard in-house scaffolding tool: capture the team's golden layout with `create-from-project`, package it with `jar`, publish it to the company repository, and every `generate` against the internal catalog reproduces it. The same mechanism scaffolds the more exotic project kinds — `maven-archetype-plugin` produces a full custom-plugin skeleton ([[How do you write a custom Maven plugin]]), other archetypes pre-configure frameworks.

> [!warning] Generated scaffolding is a starting point, not a standard
> The old quickstart archetype still generates JUnit 3-style setup and a Java version property frozen when the archetype was released — archetypes encode the era they were written in. Interviewers hear it as a red flag when a candidate treats "it worked with the default archetype" as current best practice; check the generated POM and upgrade it ([[How do you bind a plugin goal to a lifecycle phase in Maven]] shows where plugin versions belong).

> [!tip] Interview answer
> **An archetype is a project template distributed through repositories; `mvn archetype:generate` picks one from a catalog and materializes it with your coordinates. Teams publish their own via create-from-project and jar, so scaffolding stays uniform, and plugin developers start from the maven-archetype-plugin template. The generated POM reflects the archetype's age — always review it.**
