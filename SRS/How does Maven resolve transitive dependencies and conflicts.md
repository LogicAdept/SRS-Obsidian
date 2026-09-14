<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# How does Maven resolve transitive dependencies and conflicts

> [!abstract] Short answer
> **Every dependency's own POM is read from the repositories, so its dependencies — and theirs, with no depth limit — join your build automatically. When several versions of one artifact meet, mediation picks the "nearest definition": the version closest to your project in the tree; at equal depth, the first declaration wins.** You pin a version by declaring it directly, managing it, excluding it, or the producer marks it optional.

## Nearest definition wins — depth, not recency

Mediation walks the dependency tree and, for each `groupId:artifactId`, keeps the version with the shortest path to your project. Declaring an artifact directly in your POM makes it depth zero, which is why a direct declaration can always force a version. When two versions sit at the same depth, declaration order decides — the first wins. The model is documented with a tree:

```d2
direction: right
A: "A (your project)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
B: "B" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
C: "C" {
  width: 130
  height: 60
  style.fill: "#e3f2fd"
}
d2n: "D 2.0\n(depth 3)" {
  width: 180
  height: 70
  style.fill: "#ffebee"
}
E: "E" {
  width: 140
  height: 60
  style.fill: "#e3f2fd"
}
d1: "D 1.0\n(depth 2 — wins)" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}
A -> B -> C -> d2n
A -> E -> d1
```

**Fig. 1.** A → B → C → D 2.0 and A → E → D 1.0: the build of A uses D 1.0, the nearer path. Adding D 2.0 as a direct dependency of A would flip the choice.

Four features limit what the transitive graph pulls in. **Mediation** chooses versions as above. **Dependency management** overrides mediation outright for transitive artifacts. **Exclusions** cut a specific edge: if X depends on Y and Y on Z, X may exclude Z for that dependency. **Optional** dependencies are the producer's tool — Y marks Z optional, and consumers of Y get nothing of Z unless they declare it themselves; the guide's phrase is "excluded by default". Scopes limit transitivity too: a `test`-scoped dependency never travels to consumers, and a `provided` transitive dependency under a `compile` parent is omitted entirely.

```xml
<dependency>
    <groupId>com.example</groupId>
    <artifactId>legacy-framework</artifactId>
    <version>4.1</version>
    <exclusions>
        <!-- this edge of the tree is cut -->
        <exclusion>
            <groupId>commons-logging</groupId>
            <artifactId>commons-logging</artifactId>
        </exclusion>
    </exclusions>
</dependency>
```

**Listing 1.** An exclusion is per-dependency, by coordinates, and removes one transitive edge without touching the rest of the tree.

> [!warning] Nearest is not newest — and a wrong winner still compiles
> The popular lie is that Maven upgrades to the latest conflicting version. It does not: a far-away 2.0 can lose to a nearer 1.0 exactly as in Fig. 1, and first-declaration ties mean reordering your `<dependencies>` can silently change versions. The consequence that bites in interviews and in production: the build compiles against the winning version, so a method that exists in 2.0 but not 1.0 only explodes at runtime with `NoSuchMethodError` — nothing at compile time points at the conflict. Diagnose with `mvn dependency:tree`, pin with management, and declare the libraries you actually import directly — the guide's stated best practice — so your build survives your dependencies' own refactors. Version pinning in one place: [[What is the dependencyManagement section in Maven for]]; the scope rules that govern propagation: [[What are the dependency scopes in a Maven pom]]; where the dependency POMs come from: [[How does Maven resolve artifacts from repositories]].

> [!tip] Interview answer
> **Maven reads each dependency's POM and pulls the transitive graph in with no depth limit. Conflicts resolve by nearest definition — shortest path to my project wins, first declaration breaks ties — never by newest version. I can shape the graph with dependencyManagement, which beats mediation, with per-dependency exclusions, and optional flags on the producer side. And since a bad winner only fails at runtime, dependency:tree is the first reflex.**

