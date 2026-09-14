<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What are Maven plugins and how are goals invoked

> [!abstract] Short answer
> **A Maven plugin is a deliverable JAR that carries one or more goals; a goal is the smallest unit of build work.** You reach a goal either through a lifecycle phase that has it bound, or by invoking it directly — fully qualified (`mvn org.apache.maven.plugins:maven-compiler-plugin:3.13.0:compile`), shortened with a version-less coordinate, or by a short prefix (`mvn compiler:compile`).

Maven itself is just a core engine that manages a project, the POM, and the lifecycles; compiling, testing, packaging, and installing are all done by plugins. A plugin groups related goals: the compiler plugin owns `compile` and `testCompile`, the clean plugin owns `clean` ([[How would you explain mvn clean install]] shows it in a real build log). The documentation's own example of a minimal plugin is the clean plugin, whose single goal deletes the directory named by its `outputDirectory` parameter, defaulting to `${project.build.directory}`.

## Build plugins vs reporting plugins

The official catalog splits plugins into two types. **Build plugins** run during the default/clean lifecycles and are configured in the `<build>` element of the POM. **Reporting plugins** run during site generation and are configured in `<reporting>` — their output becomes part of the generated project site. A few plugins exist in both roles (Checkstyle, for example, has a build goal and a site report). See [[Which core plugins does Maven ship with]] for the catalog itself.

## Three ways a goal reaches the command line

```d2
direction: down
phase: "Via a lifecycle phase\nmvn package" {
  width: 300
  height: 85
  style.fill: "#e8f5e9"
}
binding: "Runs every goal bound to each phase\nfrom validate up to package" {
  width: 340
  height: 85
  style.fill: "#e8f5e9"
}
fq: "Fully qualified goal\nmvn org.apache.maven.plugins:maven-compiler-plugin:3.13.0:compile" {
  width: 460
  height: 100
  style.fill: "#e3f2fd"
}
short: "Version-less goal\nmvn org.apache.maven.plugins:maven-compiler-plugin:compile" {
  width: 420
  height: 100
  style.fill: "#e3f2fd"
}
prefix: "Prefix form\nmvn compiler:compile" {
  width: 260
  height: 85
  style.fill: "#fff3e0"
}
phase -> binding
fq -> short -> prefix
```

**Fig. 1.** Phase invocation walks the lifecycle; the three direct forms differ only in how much of the plugin's coordinates you type.

For the prefix form, Maven maps the short name `compiler` to a `groupId:artifactId` by querying repository metadata. Two conventions feed the mapping: a plugin named `${prefix}-maven-plugin` (`hello-maven-plugin` → prefix `hello`) and, for Apache's own group, `maven-${prefix}-plugin` (`maven-compiler-plugin` → prefix `compiler` under `org.apache.maven.plugins`). A company plugin can still get a short prefix by adding its groupId to `<pluginGroups>` in `settings.xml`. When you drop the version on a direct invocation, Maven picks the newest release of that plugin available in your local repository — reproducible builds pin plugin versions in the POM instead ([[How do you bind a plugin goal to a lifecycle phase in Maven]]).

> [!warning] `maven-` prefix is reserved
> Naming your plugin `maven-<something>-plugin` is strongly discouraged: that pattern is reserved for official Apache Maven plugins under `org.apache.maven.plugins`, and the guide treats its misuse as a trademark infringement. Name third-party plugins `<yourplugin>-maven-plugin` — [[How do you write a custom Maven plugin]] walks the full layout.

> [!tip] Interview answer
> **Maven is a core engine plus plugins; every real build action is a plugin goal. A plugin groups related goals, and you invoke a goal through a lifecycle phase or directly — by full coordinates, without a version, or by prefix like `compiler:compile`. Prefixes come from naming conventions or `pluginGroups` in settings.xml. Build plugins live in `<build>`, reporting ones in `<reporting>`.**
