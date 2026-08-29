<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #SRS

# How do you change the port of the embedded server?

> [!abstract] Short answer
> Set **`server.port`** (default **`8080`**) in `application.properties` / YAML, as a JVM system property, as **`SERVER_PORT`**, or as **`--server.port=9090`**. **`server.port=0`** asks the OS for a **free** port (typical for parallel tests). **`server.port=-1`** starts a `WebApplicationContext` with **HTTP off**. **`management.server.port`** is the **Actuator** port, not the app server.

## Same property, several PropertySources

In a standalone Boot app the embedded container (Tomcat, Jetty, Undertow, or Netty) listens on **`server.port`**. Relaxed binding accepts `SERVER_PORT`. Command-line arguments beat `application.properties` ([[What is Spring Boot property source precedence]]).

```properties
server.port=9090
```

**Listing 1.** File form. YAML is `server.port: 9090` (or nested `server: { port: 9090 }`).

```bash
java -jar myapp.jar --server.port=9090
```

**Listing 2.** CLI form of the same key. `SERVER_PORT=9090` is the environment-variable spelling.

`server.port=0` scans for an **unassigned** port using OS natives so two processes do not collide. After the container is up, the bound port is `local.server.port` (`@LocalServerPort` in tests — a meta-annotation for `@Value("${local.server.port}")`). `@SpringBootTest(webEnvironment = RANDOM_PORT)` uses that random-port setup.

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
class MyWebIntegrationTests {

	@LocalServerPort
	int port;
}
```

**Listing 3.** Test-only injection of the port that was actually bound. Do not `@Value("${local.server.port}")` in ordinary application beans: the property is set **after** the server starts, and those beans are created **too early**.

```d2
direction: right
props: "server.port\nfile / SERVER_PORT / --server.port" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
bind: "Embedded WebServer\ndefault 8080" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
special: "0 = random free\n-1 = HTTP off" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

props -> bind -> special
```

**Fig. 1.** One property drives the main HTTP port ([[Which embedded containers are supported by Spring Boot]]). `0` and `-1` are the special values, not “pick Tomcat’s default”.

> [!warning] `management.server.port` is not `server.port`
> Actuator shares the **application** port unless you set **`management.server.port`**. Changing only `server.port` moves **both** when they still share a port. A separate management port (and `management.server.address` / `base-path`) is a **second** server — health checks on 8080 will miss it. `management.server.port` does **not** change Tomcat/Netty’s main listen port.

> [!warning] Random port is not available at bean construction
> `server.port=0` means “bind later”, not “the Environment already knows the number”. Read `local.server.port` from a `WebServerInitializedEvent` / `WebServerApplicationContext`, or from `@LocalServerPort` in a **test**. Injecting it into a `@Component` constructor usually yields an unresolved placeholder or the unset value.

> [!tip] Interview answer
> I set server.port — default 8080 — in application.properties, SERVER_PORT, or --server.port. Zero means bind a free port, which is what RANDOM_PORT tests do; minus one turns HTTP off but still builds a web context. management.server.port is Actuator’s port, a different knob, and I never inject local.server.port into production beans because it exists only after the container has started.
