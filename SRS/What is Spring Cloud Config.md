<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/Config #SRS

# What is Spring Cloud Config?

> [!abstract] Short answer
> **Spring Cloud Config** is **server and client** support for **externalized configuration** in a distributed system: one **Config Server** holds properties (default backend **Git**); Boot apps pull them into the Spring **`Environment` / `PropertySource`** model. It is not “only Git” (other backends plug in) and not a replacement for local `application.yml` — remote sources **join** that `Environment`. Identity is **central, environment-aware config**, not messaging or discovery.

## Server and client

A Config Server is a Boot app with `@EnableConfigServer`. Conventional port **8888**. Point Git with `spring.cloud.config.server.git.uri` (a **local** `file://` repo is for tests). The HTTP API serves `/{application}/{profile}/{label}`. Default label is **`master`**; with the Git backend, label can be a branch, tag, or commit ([[What is Spring Cloud]], [[What are the advantages of using Spring Cloud]]).

Clients put **Config Client** on the classpath. Binding is by `${spring.application.name}`, `${spring.profiles.active}`, and optional `spring.cloud.config.label`. Do not prefix the application name with `application-`. Shared files named `application` are always served; extra names go on `spring.cloud.config.name`. Values are ordinary `Environment` properties (`@Value`, `@ConfigurationProperties`).

**Current default (Boot 2.4+):** import, not bootstrap:

```
spring.config.import=optional:configserver:
```

Default server URL is `http://localhost:8888`. Put the URL on the import (`configserver:http://host:8888`) or in `spring.cloud.config.uri` — the **import location wins**. Drop `optional:` to **fail startup** if the server is down. A `bootstrap.yml` is **not** required for this path.

**Legacy config-first bootstrap:** `spring.cloud.bootstrap.enabled=true` (system property / env) or `spring-cloud-starter-bootstrap`, then `spring.cloud.config.uri` in bootstrap config. AOT / native images do **not** support that bootstrap path.

```java
@SpringBootApplication
@EnableConfigServer
public class ConfigServer {

	public static void main(String[] args) {
		SpringApplication.run(ConfigServer.class, args);
	}
}
```

**Listing 1.** Conceptual. Embeddable Config Server.

```
server.port=8888
spring.cloud.config.server.git.uri=file://${user.home}/config-repo
```

**Listing 2.** Conceptual. Git-backed server; use a hosted repo in production.

```d2
direction: down
git: "Git (or other backend)\nlabelled files" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
server: "Config Server :8888\n/{name}/{profile}/{label}" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
env: "Client Environment\n@Value / @ConfigurationProperties" {
  width: 300
  height: 50
  style.fill: "#e8f5e9"
}
git -> server
server -> env
```

**Fig. 1.** Server reads the backend; clients bind the same `Environment` abstractions.

After a Git (or backend) change, **running** beans keep constructor/`@Value` injection until you **refresh**. `@RefreshScope` rebuilds those beans; `/refresh` (HTTP or JMX) calls `RefreshScope.refreshAll()`. Native images: refresh scope is **unsupported** — set `spring.cloud.refresh.enabled=false`.

> [!warning] Import vs bootstrap
> Interview dumps still lead with `bootstrap.properties`. On current Cloud, **`spring.config.import=optional:configserver:`** is the documented default. Bootstrap is an explicit legacy switch. Config Data import may **request the server twice** (default profile, then active profiles) so profiles from the server can activate — that is expected, not a bug.

> [!warning] Changing Git is not a live update by itself
> The client loads remote sources at startup (and on refresh). Editing the repo does not rewrite already-created beans until `/refresh` / `@RefreshScope` (or a restart). Immutable beans need `@RefreshScope` or `spring.cloud.refresh.extra-refreshable`.

> [!tip] Interview answer
> Config is a Git-backed (by default) server plus Boot clients that import those properties into `Environment`. Identify the app with `spring.application.name`. Use `spring.config.import=configserver:` today; treat bootstrap as legacy. `@RefreshScope` is how you pick up a push without a full process restart.
