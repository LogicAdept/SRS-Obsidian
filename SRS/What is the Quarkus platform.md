<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# What is the Quarkus platform?

> [!abstract] Short answer
> The Quarkus platform is a **curated, version-aligned set of extensions published as BOMs** — the core `quarkus-bom` plus member platform BOMs (for example the Camel Quarkus platform) — imported into your build with a single version. It guarantees that all extensions, their transitive dependencies and the Quarkus core in one application are a tested combination, and it backs the tooling: the extension catalog, project generation, and the `quarkus update` upgrade flow.

## What "platform" means mechanically

A BOM (`<type>pom</type> <scope>import</scope>`) pins versions for every extension the platform contains; application poms then declare extensions **without versions** ([[How do you create a new Quarkus project]]). The platform is what makes `mvn quarkus:update` able to move an entire application across a Quarkus minor or major release: one property change (the platform version) re-resolves every extension to the new aligned matrix, and OpenRewrite recipes repair code and config breakages ([[What does quarkus update do]]). The catalog exposed by `quarkus extension list --installable` and by code.quarkus.io is derived from the platform too — "installable" means "the platform knows a compatible version of it".

Member platforms exist for ecosystems that release on their own cadence while keeping compatibility with a Quarkus stream: a platform release line (for example 3.39.x) has a coordinated set — core BOM plus member BOMs (such as Camel Quarkus) whose extension versions are aligned to it. Applications import either the plain core BOM or a member BOM that itself imports core.

```java
// The platform is visible in any generated pom (Quarkus 3.39.2 skeleton, abridged):
//
// <properties>
//   <quarkus.platform.group-id>io.quarkus.platform</quarkus.platform.group-id>
//   <quarkus.platform.artifact-id>quarkus-bom</quarkus.platform.artifact-id>
//   <quarkus.platform.version>3.39.2</quarkus.platform.version>
// </properties>
//
// <dependencyManagement>
//   <dependencies>
//     <dependency>
//       <groupId>${quarkus.platform.group-id}</groupId>
//       <artifactId>${quarkus.platform.artifact-id}</artifactId>
//       <version>${quarkus.platform.version}</version>
//       <type>pom</type>
//       <scope>import</scope>
//     </dependency>
//   </dependencies>
// </dependencyManagement>
//
// <dependencies>
//   <dependency>
//     <groupId>io.quarkus</groupId>
//     <artifactId>quarkus-rest</artifactId>   <!-- no version - BOM supplies it -->
//   </dependency>
// </dependencies>
//
// $ mvn quarkus:info   (plugin goal reporting what the project imported, verbatim section)
// [INFO] Quarkus platform BOMs:
// [INFO]  - io.quarkus.platform:quarkus-bom:3.39.2
```

**Listing 1.** One import line pins the whole matrix; the `quarkus:info` goal confirms which BOM and which extensions the build resolved — the first diagnostic for "why do I have two versions of X".

```d2
direction: down
bom: "quarkus-bom 3.39.2\ncore extensions, aligned deps" {
  width: 300
  height: 65
  style.fill: "#e3f2fd"
}
members: "Member platform BOMs\ne.g. Camel Quarkus platform" {
  width: 300
  height: 65
  style.fill: "#e3f2fd"
}
app: "Application pom\nsingle import, versionless deps" {
  width: 300
  height: 65
  style.fill: "#fff3e0"
}
tools: "Tooling\ncatalog, create, update recipes" {
  width: 300
  height: 60
  style.fill: "#e8f5e9"
}
bom -> app: "import"
members -> app: "import (includes core)"
app -> tools: "drives"
```

**Fig. 1.** Applications consume aligned BOMs; tooling consumes the platform's catalog metadata — the same source of truth for both ([[What is a Quarkus extension]]).

## Why an interviewer asks about it

The platform is Quarkus' answer to "framework dependency hell": instead of each team discovering that extension A needs Vert.x 4.5 while extension B needs 4.6, the platform publishes combinations its CI actually tests. Maturity grades (stable, preview, experimental) travel with the catalog, so "is this extension safe" has a documented answer. And because upgrade is a first-class flow (platform version bump + recipes), teams can track LTS streams (3.33.x, 3.27.x) deliberately instead of ad hoc version chasing.

> [!warning] A platform import does not magically version-lock anything you pin yourself
> Hand-pinned versions of extensions or of shared transitive dependencies override BOM entries and silently exit the tested matrix. The other misconception: "platform = fat runtime" — importing a BOM adds zero jars; you still declare only the extensions you use, and unused beans are stripped at build time. The cost of the platform is one import line, not bundle size.

> [!tip] Interview answer
> The Quarkus platform is the curated extension set published as BOMs — core quarkus-bom plus member platforms like Camel — imported once so every extension version is an aligned, tested combination. It powers the tooling: the extension catalog, project generation, and quarkus update, which moves the whole app across releases by bumping one property and running OpenRewrite recipes. Practical rule: declare extensions without versions and never pin overrides, or you leave the tested matrix.
