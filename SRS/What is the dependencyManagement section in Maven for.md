<!--
reps: 0
priority: 0
-->
#Java/Tooling/Maven #SRS

# What is the dependencyManagement section in Maven for

> [!abstract] Short answer
> **It centralizes dependency declarations: versions, scopes, and exclusions are stated once (in a parent or a BOM) and children reference dependencies without restating them.** It is also the tool for controlling transitive versions — a managed version beats dependency mediation. Managing a dependency does not put it on the classpath; each module still declares what it actually uses.

## The two jobs: defaults for children, control of transitive versions

A parent POM states shared artifacts under `<dependencyManagement>`; child POMs then declare `groupId:artifactId` only, inheriting version and scope. The matched identity is `{groupId, artifactId, type, classifier}` — since `type` defaults to `jar` and classifier to none, plain jars match on coordinates alone. The second, heavier use is transitive control: when artifact `X` pulls in a managed artifact transitively, the managed version wins over conflict mediation, so one declared version pins the whole graph.

```xml
<!-- parent pom.xml: state versions once -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-databind</artifactId>
            <version>2.17.1</version>
        </dependency>
    </dependencies>
</dependencyManagement>

<!-- child pom.xml: no version, no scope drift -->
<dependencies>
    <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
    </dependency>
</dependencies>
```

**Listing 1.** Canonical shape from the Maven dependency-mechanism guide: the parent manages, the child references without a version.

```d2
direction: down
own: "dependencyManagement in this POM" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
parent: "inherited from parent POM" {
  width: 300
  height: 80
  style.fill: "#e3f2fd"
}
med: "mediation of transitive conflicts\n(nearest definition, then first declared)" {
  width: 340
  height: 90
  style.fill: "#fff3e0"
}
own -> parent: "current POM beats parent"
own -> med: "managed version beats mediation"
parent -> med: "managed version beats mediation"
```

**Fig. 1.** Where management sits in resolution: this POM's management overrides the parent's, and either overrides mediation of transitive versions.

## Importing BOMs

`<scope>import</scope>` works only on a dependency of type `pom` inside `dependencyManagement`: the imported POM's managed entries are spliced into this POM's management. It composes where single inheritance cannot — several BOMs can be imported, processed recursively; when two imports manage the same artifact, the **first-declared import wins**. This is the "bill of materials" pattern: a library publishes a `pom`-packaging artifact listing its module versions, consumers import it and drop per-artifact versions. Since Maven 4.0 there is also a dedicated `bom` packaging that stays compatible with 3.x clients.

> [!warning] Managed does not mean present — and plugins are not covered
> The classic interview slip: "I added it to `dependencyManagement`, why is my classpath still empty?" Management only supplies values when the dependency is referenced; nothing is resolved for artifacts no one declares. Two more documented edges: management affects project dependencies only — the dependencies of plugins in the same effective POM are outside its reach — and importing a POM that is a submodule of the current build, or circularly importing/parenting each other, fails the build. Also, when an imported artifact's own POM carries transitive dependencies, their versions must be managed too, or resolution fails. How the unmanaged leftovers resolve: [[How does Maven resolve transitive dependencies and conflicts]]; where `import` scope belongs in the scope table: [[What are the dependency scopes in a Maven pom]].

> [!tip] Interview answer
> **dependencyManagement centralizes dependency metadata: the parent or a BOM states versions, scopes and exclusions once, and modules declare artifacts without restating them. It also outranks transitive mediation, so a managed version pins the whole graph, and BOMs arrive through the import scope inside this section. Crucially, managing is not declaring — nothing lands on the classpath until a module actually lists the dependency.**

