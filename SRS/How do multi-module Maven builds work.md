<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# How do multi-module Maven builds work

> [!abstract] Short answer
> **A parent POM lists its subdirectories in `<modules>`; the reactor — the part of Maven core that handles multi-module builds — collects the modules, sorts them into dependency-correct order, and builds them in that order with one command.** Aggregation (the `<modules>` list) and inheritance (the `<parent>` link) are two separate mechanisms that usually point at the same POM but solve different problems.

## The reactor sorts; your listing only breaks ties

The reactor honors four ordering relationships before it ever looks at the `<modules>` order: a project dependency on another module, a plugin declaration that is another module, a plugin dependency on another module, and a build extension declaration on another module. Only when none of those apply does the declared order decide. Notably, `dependencyManagement` and `pluginManagement` entries do **not** influence the sort — they supply versions, not dependency edges.

```xml
<!-- aggregator + parent POM (packaging pom) -->
<project>
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.demo</groupId>
    <artifactId>demo-parent</artifactId>
    <version>1.0.0</version>
    <packaging>pom</packaging>

    <modules>
        <module>demo-core</module>
        <module>demo-web</module>
    </modules>

    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>com.fasterxml.jackson.core</groupId>
                <artifactId>jackson-databind</artifactId>
                <version>2.17.1</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>
```

**Listing 1.** The dual-role root POM: `<modules>` aggregates the build; `dependencyManagement` gives both children their shared versions. `demo-web` additionally declares a `<parent>` link to inherit coordinates and configuration.

```d2
direction: left
run: "mvn clean install\nat the root" {
  width: 240
  height: 90
  style.fill: "#e3f2fd"
}
reactor: "Reactor\ncollect + sort" {
  width: 200
  height: 90
  style.fill: "#fff3e0"
}
core: "demo-core\n(dependency)" {
  width: 210
  height: 80
  style.fill: "#e8f5e9"
}
web: "demo-web\n(depends on core)" {
  width: 230
  height: 80
  style.fill: "#e8f5e9"
}
run -> reactor
reactor -> core: "1"
reactor -> web: "2"
```

**Fig. 1.** One invocation at the root; the reactor orders `demo-core` before `demo-web` because of the declared project dependency, regardless of listing order.

Reactor behavior is steerable from the command line: `--also-make` adds the selected projects' reactor dependencies, `--also-make-dependents` the projects that need them, `--resume-from` restarts a failed build at a given module, `--fail-fast` (the default) stops on the first failing module while `--fail-at-end` continues and reports everything at the end, and `--non-recursive` builds the current POM while ignoring its modules.

> [!warning] "Modules build in the order I listed them" — and the ~/.m2 detour
> Two traps. First, listing order is only the last tie-breaker; the dependency graph rules, so moving a `<module>` line rarely changes anything and never fixes a bad dependency — and an undeclared reliance on another module (filled only through management or luck) does not reorder the build either, because management entries create no edges. Second, the classic workflow hole: building a single module inside the multi-module tree resolves its sibling dependencies from the local `~/.m2` — if the sibling changed and was never installed there, the module builds against a stale artifact; `mvn clean install` at the root refreshes every module's local artifact in one ordered pass, and `--also-make` builds exactly the upstream slice you need. Version sharing across modules: [[What is the dependencyManagement section in Maven for]]; the command that glues local multi-module work: [[How would you explain mvn clean install]]; what a child POM inherits structurally: [[How would you explain the structure of a Maven pom.xml file]].

> [!tip] Interview answer
> **A multi-module build has an aggregator POM listing modules and, usually the same POM, acting as the inheritance parent. The reactor collects the modules, sorts them by real dependency relationships — project deps, plugin deps, extensions; the modules listing is only the tie-breaker — and builds them in order with one command. That single pass is why root-level mvn clean install keeps sibling artifacts fresh in ~/.m2, with flags like also-make, fail-at-end and resume-from to slice or survive big reactors.**

