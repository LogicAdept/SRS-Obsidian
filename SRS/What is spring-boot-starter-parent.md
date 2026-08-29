<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Build #SRS

# What is spring-boot-starter-parent?

> [!abstract] Short answer
> **`spring-boot-starter-parent`** is a **Maven parent POM**, not a runtime starter. It gives **plugin defaults** (including a **`repackage`** execution) and **`dependencyManagement` inherited from `spring-boot-dependencies`**, so you omit `<version>` on starters. If a **corporate parent** already owns `<parent>`, **import** that BOM with `<scope>import</scope>` — you keep version management, **not** plugin management.

## Parent POM, not a classpath starter

Official Maven-plugin guide: inherit the parent for **sensible defaults**:

- **Java 17** compiler level, **UTF-8**, compile with **`-parameters`**
- **`dependencyManagement`** from **`spring-boot-dependencies`** (omit versions on managed artifacts)
- An execution of **`repackage`** (`id` **`repackage`**)
- A **`native`** profile for native images
- Resource filtering, including **`application.properties` / YAML** and **`application-{profile}.*`**
- Plugin defaults (Git Commit Id, shade)

```xml
<parent>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-starter-parent</artifactId>
	<version>4.1.1</version>
</parent>
```

**Listing 1.** Only the **Boot version** belongs here. Further `spring-boot-starter-*` dependencies drop `<version>` ([[Why can you omit library versions in a Spring Boot project]]; [[Which common Spring Boot starters do you know]]). Override a managed library with a **property** (`slf4j.version`, …) while you still inherit this parent.

```xml
<dependencyManagement>
	<dependencies>
		<dependency>
			<groupId>org.springframework.boot</groupId>
			<artifactId>spring-boot-dependencies</artifactId>
			<version>4.1.1</version>
			<type>pom</type>
			<scope>import</scope>
		</dependency>
	</dependencies>
</dependencyManagement>
```

**Listing 2.** Corporate-parent path: **BOM import**. You **cannot** override with those version **properties**; put override artifacts in `dependencyManagement` **before** the BOM. You must configure **`spring-boot-maven-plugin`** yourself (no inherited **`repackage`** / Failsafe `classesDirectory`) ([[What is an executable JAR in Spring Boot]]).

Maven filtering on `application.properties` uses **`@..@`** placeholders because Spring already uses `${…}`. Change `resource.delimiter` if you must. `maven.compiler.release` from the parent can block `--add-exports` on system modules — unset it and set `source`/`target` instead.

```d2
direction: right
parent: "spring-boot-starter-parent\n<parent>" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
both: "BOM versions\n+ plugin defaults" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}
bom: "spring-boot-dependencies\nscope=import" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
vers: "BOM versions only" {
  width: 180
  height: 50
  style.fill: "#fce4ec"
}

parent -> both
bom -> vers
```

**Fig. 1.** Gradle does **not** use this parent; the Boot Gradle plugin imports the same BOM. Overriding curated versions can break a release that was tested as a set ([[How do you deploy a Spring Boot application]]).

> [!warning] It never sits on the running classpath
> Despite the **`starter`** name, this artifact is **`packaging=pom`**. Putting it in `<dependencies>` does not add Boot to the app. Dropping the parent **without** importing **`spring-boot-dependencies`** also drops version alignment. The BOM path does **not** copy plugin management — no automatic **`repackage`**, no Failsafe `outputDirectory` default.

> [!warning] `${}` in `application.properties` is Spring, not Maven
> Parent resource filtering switched the Maven delimiter to **`@property@`**. A leftover `@project.version@` (or the reverse) is a common “it works in IDE, wrong in the jar” bug. Property-based version overrides work **only** with the parent, not with a plain BOM import.

> [!tip] Interview answer
> spring-boot-starter-parent is the Maven parent POM: it imports spring-boot-dependencies so starters need no versions, and it wires plugin defaults including repackage. If I already have a corporate parent, I import the BOM instead and I lose plugin management. It is not a runtime starter on the classpath.
