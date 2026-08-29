<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS

# What is Spring Boot DevTools?

> [!abstract] Short answer
> **`spring-boot-devtools`** is a **development-time** module: **automatic restart** (two classloaders), **dev property defaults** (template cache off, error details on, tracing sample **100%**), optional **remote** update, and (Boot **4.1: deprecated**) LiveReload. It is **disabled** for **`java -jar`** / a production classloader. Mark Maven **`optional`**, Gradle **`developmentOnly`**. Never force restart on in production.

## Faster loop, not a production feature

Official aim: make development **more pleasant** ([[What is Spring Boot]]). Restart watches **classpath directories**. Eclipse **save** or IDEA **Build Project** (or `mvn compile`) must **update the classpath** — editing source without compile does nothing. Static files under `/static`, `/public`, `/templates`, … **do not** restart (they used to LiveReload). Each restart logs a **condition-evaluation delta** ([[How can you debug which auto-configuration classes applied]]).

```xml
<dependency>
	<groupId>org.springframework.boot</groupId>
	<artifactId>spring-boot-devtools</artifactId>
	<optional>true</optional>
</dependency>
```

**Listing 1.** Dump omitted **`optional`**. That flag (Gradle `developmentOnly`) keeps DevTools **off** transitive dependents. Repackaged JARs **exclude** it unless you set plugin `excludeDevtools=false` (and Maven `includeOptional`) — only for **opt-in remote** use ([[What is an executable JAR in Spring Boot]]).

Restart uses a **base** classloader (third-party jars) and a **restart** classloader (your code). Throw away the restart loader = faster than a cold start. **JRebel** disables restart in favor of reload. **AspectJ weaving** is unsupported. Disable the JVM **shutdown hook** and restart **breaks**. Completely off: set **`spring.devtools.restart.enabled=false` as a system property before `SpringApplication.run`** (file-only still creates the restart loader).

```properties
spring.devtools.add-properties=false
```

**Listing 2.** Skip automatic **dev defaults** (`spring.thymeleaf.cache=false`, `spring.web.resources.cache.period=0`, `spring.h2.console.enabled=true`, `management.tracing.sampling.probability=1.0`, …). Global machine defaults: `$HOME/.config/spring-boot/spring-boot-devtools.properties` (no profiles in that file).

```d2
direction: down
dev: "spring-boot-devtools\n(optional / developmentOnly)" {
  width: 300
  height: 60
  style.fill: "#e3f2fd"
}
rst: "restart classloader\nclasspath directory changes" {
  width: 280
  height: 60
  style.fill: "#fff3e0"
}
prod: "java -jar → DevTools off" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

dev -> rst
dev -> prod
```

**Fig. 1.** **LiveReload is deprecated as of Boot 4.1** with **no replacement**; at most one server, and restart must be on. Remote: `spring.devtools.remote.secret`, **not WebFlux**, **not production**, trusted network or TLS. `@RestartScope` keeps Testcontainers across restarts (Gradle: `testAndDevelopmentOnly`).

> [!warning] `-Dspring.devtools.restart.enabled=true` on `java -jar` is a security risk
> Official: do **not** do that in production. Remote DevTools is **opt-in** and the same warning. Multi-module classloading bugs: try disabling restart, then `META-INF/spring-devtools.properties` `restart.include.*` / `restart.exclude.*`.

> [!warning] Not hot-swap and not a starter
> JVM hot-swap still exists and is limited; DevTools **restarts**. It is **`spring-boot-devtools`**, not `spring-boot-starter-devtools`. `bootRun` needs **forking enabled**. Trigger file: `spring.devtools.restart.trigger-file` on the classpath.

> [!tip] Interview answer
> DevTools is a development dependency that restarts the app when classpath files change, using two classloaders so third-party jars stay loaded. It turns caches off so templates and static files update. It is off for a packaged jar. I mark it optional. LiveReload is deprecated in Boot 4.1. I never enable it in production.
