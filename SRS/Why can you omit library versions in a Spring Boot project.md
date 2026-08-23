<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Build #SRS

# Why can you omit library versions in a Spring Boot project?

> [!abstract] Short answer
> **Each Spring Boot release ships a curated BOM (`spring-boot-dependencies`)** with tested versions for Spring modules and common third-party libraries (Jackson, Tomcat, Hibernate, …). **`spring-boot-starter-parent`** (or an **import-scoped BOM**) puts that list into Maven **`dependencyManagement`**, so you declare **`spring-boot-starter-*`** and other managed artifacts **without `<version>`** — Boot picks compatible versions for you.

## BOM-driven dependency management

Spring Boot's build-systems guide states that **you do not need to provide a version** for dependencies on Boot's curated list — **Spring Boot manages versions for you**. Upgrading the **Boot version** upgrades the managed stack **consistently**.

Two common Maven setups:

| Setup | What you get |
|---|---|
| **`spring-boot-starter-parent` as `<parent>`** | Dependency management **and** plugin defaults (compiler, surefire, repackage, …) |
| **Import `spring-boot-dependencies` BOM** | Dependency management **only** — use when a **corporate parent POM** already owns the project |

The Maven plugin docs show the import pattern when you **cannot** use `starter-parent`:

```xml
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-dependencies</artifactId>
      <version>3.4.13</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>

<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <!-- no version — resolved from BOM -->
  </dependency>
</dependencies>
```

**Listing 1.** Starters pull in managed transitive versions (embedded Tomcat, Jackson, etc.) without explicit coordinates.

```d2
direction: right
boot: "Spring Boot release" {
  width: 160
  height: 50
  style.fill: "#e3f2fd"
}
bom: "spring-boot-dependencies\n(BOM)" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
pom: "Your pom.xml\nstarter, no version" {
  width: 200
  height: 60
  style.fill: "#e8f5e9"
}
libs: "Jackson, Tomcat,\nHibernate, …" {
  width: 180
  height: 60
  style.fill: "#fce4ec"
}

boot -> bom -> pom -> libs
```

**Fig. 1.** One Boot version pins the whole supported dependency set.

## Overrides and traps

You **can** still set a **`<version>`** (or a BOM property) to **override** Boot's recommendation when needed — the docs explicitly allow that.

Spring also recommends **not specifying Spring Framework's version** separately; it is tied to each Boot release.

Gradle gets the same BOM through the **`io.spring.dependency-management`** plugin (applied by the Spring Boot Gradle plugin), which auto-imports **`spring-boot-dependencies`**.

> [!warning] Boot parent without BOM import loses management
> Dropping **`spring-boot-starter-parent`** **and** failing to **import `spring-boot-dependencies`** brings back **version conflicts** — different transitive JARs resolving to incompatible Jackson, SLF4J, or Hibernate versions. Corporate parents should **import the BOM**, not re-pin every library by hand. See [[What is spring-boot-starter-parent]].

> [!tip] Interview answer
> Spring Boot publishes a curated BOM. starter-parent or an import-scoped spring-boot-dependencies entry supplies dependencyManagement, so you declare starters without versions and get a tested stack. Import the BOM if you use a corporate parent; omitting both parent and BOM is how version fights return.
