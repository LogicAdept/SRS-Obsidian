<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS

# What is Spring Boot Initializr?

> [!abstract] Short answer
> **Spring Initializr** is a **project-generation** library and HTTP service: it emits a **JVM project** (Maven or Gradle, language, packaging, coordinates, platform version, dependency **ids**) from **metadata**. The public instance plus IDEs and **`spring init`** wrap that API. It is **not** your running app and **not** a code generator for business logic. The **library itself has no Web UI**; a hosted instance (or an IDE) supplies the form.

## Metadata in, zip out

Official reference: an extensible API to **generate** JVM projects and to **inspect** the metadata (available dependencies, versions, project types). A request is a `ProjectDescription`: `groupId` / `artifactId`, `BuildSystem`, `Packaging`, JVM `Language`, dependency ids, platform `Version`, application name, root package. Generation runs in a dedicated `ProjectGenerationContext`. `initializr-generator-spring` adds **Spring Boot conventions** (for Maven, a `MavenBuildProjectContributor` writes `pom.xml`; other contributors add wrappers, a `@SpringBootApplication` main type, a test, and a config file — a **skeleton**, not features).

Boot’s first-app tutorial: pick the **Web** dependency on the public service and **start coding**; the long path is the same parent + starter by hand ([[What is spring-boot-starter-parent]], [[Which common Spring Boot starters do you know]]). Typical layout matches a standard Boot tree ([[What does a typical Java web application project structure look like]]).

```text
spring init --dependencies=web,data-jpa my-project
```

**Listing 1.** Boot CLI `init` (same service as the public instance). `--list` prints capability ids. Other clients: STS, IntelliJ IDEA Ultimate, NetBeans, VS Code, curl / HTTPie. `GET /` with `Accept: application/vnd.initializr.v2.3+json` returns HAL metadata (`maven-project` / `gradle-project` → `starter.zip`, plus `pom.xml` / `build.gradle` only). Current metadata **v2.3** adds **configuration file format**.

```d2
direction: down
clients: "IDE / CLI / HTTP client" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
meta: "GET /\ncapabilities JSON" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
gen: "ProjectGenerator\nProjectDescription" {
  width: 240
  height: 50
  style.fill: "#fce4ec"
}
out: "starter.zip\nbuild + Boot skeleton" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

clients -> meta
meta -> gen
gen -> out
```

**Fig. 1.** Boot CLI still lists **`init` / `encodepassword` / `shell`** ([[What are the components of a Spring Boot application]]). A custom instance is a **separate** Boot app (`initializr-web` + `initializr-generator-spring` + `initializr-bom`); hitting it without configured metadata returns **empty** select lists.

> [!warning] The library has no UI — and the dump was wrong about “no code”
> Official: **Spring Initializr does not provide a Web UI.** The form you click is the **hosted service** or an **IDE wizard**. The dump’s “no application code” is stale: `initializr-generator-spring` **does** emit a main class and test. It still does **not** write your controllers or domain.

> [!warning] Dependency **id** is not the artifact name
> Capabilities list ids such as `web` and `devtools`. The **jar** follows the chosen Boot generation (Boot **4** Web is **`spring-boot-starter-webmvc`**, not the old `starter-web` name). Compatibility ranges can **hide** a dependency for a Boot version.

> [!tip] Interview answer
> Initializr is the service behind new Boot projects. I choose Maven or Gradle, Java version, and starter ids; it returns a zip with the build and a main class. I use the website, the IDE wizard, or spring init. It is not a runtime and it does not write my business code.
