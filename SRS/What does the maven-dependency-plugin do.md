<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What does the maven-dependency-plugin do

> [!abstract] Short answer
> **It is the diagnostic and manipulation toolbox for dependencies: `tree` shows how artifacts were resolved, `analyze` compares declared against actually used, `copy-dependencies` extracts files, `go-offline` prepares an offline build, and `purge-local-repository` clears a broken cache.** Most goals are run directly from the command line, not bound to the lifecycle.

The plugin exists because the POM only declares what a project depends on; the questions "why is this version here", "do I even use this", "which jar do I ship to a server" need a tool. Its goals complement the resolution mechanism itself ([[How does Maven resolve transitive dependencies and conflicts]] explains mediation; [[What are the dependency scopes in a Maven pom]] explains classpath placement).

## The goals an interview cares about

```d2
direction: right
tree: "dependency:tree\nresolved graph with conflict marks" {
  width: 300
  height: 90
  style.fill: "#e3f2fd"
}
analyze: "dependency:analyze\nused-declared / used-undeclared /\nunused-declared" {
  width: 300
  height: 110
  style.fill: "#e3f2fd"
}
copy: "dependency:copy-dependencies\ncopies dependency files to a folder" {
  width: 320
  height: 110
  style.fill: "#fff3e0"
}
gooff: "dependency:go-offline\nresolves deps + plugins for offline CI" {
  width: 330
  height: 110
  style.fill: "#fff3e0"
}
purge: "dependency:purge-local-repository\ndeletes and optionally re-resolves" {
  width: 340
  height: 110
  style.fill: "#e8f5e9"
}
```

**Fig. 1.** The five goals that come up in real work: one per diagnosis, extraction, offline preparation, and cache repair.

`dependency:tree` prints the resolved graph and marks version conflicts and omitted duplicates — the first command for any "wrong version on the classpath" mystery. `dependency:analyze` classifies each dependency as used-and-declared, used-but-undeclared (it compiles because a transitive dependency leaked it), or declared-but-unused; the `analyze-only` variant skips the forked `test-compile` the default `analyze` performs, so a POM-bound check does not re-run compilation. `copy-dependencies` copies direct and transitive dependency files into a target folder — the manual answer to "how do I ship my lib dir"; the classic interview command `mvn clean dependency:copy-dependencies package` uses it mid-build ([[What happens when you mix phases and plugin goals in one mvn command]] dissects that line). `dependency:get` fetches a single artifact by coordinates into the local cache, and `list-repositories` shows which repositories actually served the build.

> [!warning] `analyze` proves undeclared usage, not correctness
> A clean `analyze` report does not mean your dependency list is honest — it means the compiler did not need anything undeclared for the code paths that compiled. Runtime-only usage (drivers, `ServiceLoader` implementations) stays invisible to bytecode analysis, and `provided`-scope surprises are a classic false positive. Treat it as a lint pass, not a proof.

> [!tip] Interview answer
> **The dependency plugin is the debugging toolkit over the resolved classpath: tree shows the graph and conflicts, analyze flags used-undeclared and declared-unused jars, copy-dependencies exports the files, go-offline pre-fetches everything for an offline CI build, and purge-local-repository repairs a corrupted cache. Goals run directly — `mvn dependency:tree` works even in a POM that never declares the plugin.**
