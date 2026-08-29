<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Embedded #SRS

# How do you create a non-web Spring Boot application?

> [!abstract] Short answer
> Do **not** put a web starter (servlet API / WebFlux server) on the classpath, **or** force **`WebApplicationType.NONE`**: `spring.main.web-application-type=none` or `SpringApplication.setWebApplicationType(WebApplicationType.NONE)`. Boot then uses a plain **`AnnotationConfigApplicationContext`** and **does not start** an embedded server. Put work in a **`CommandLineRunner`** / **`ApplicationRunner`** `@Bean`. `NONE` does **not** delete `spring-boot-starter-web` from the POM.

## How Boot decides, and how you override it

`SpringApplication` picks a context from the classpath:

1. Spring MVC present → servlet web context (embedded Tomcat/Jetty/Undertow).
2. Else Spring WebFlux present → reactive web context (Netty by default).
3. Else → **`AnnotationConfigApplicationContext`** (no web server).

The enum is **`NONE`**, **`SERVLET`**, **`REACTIVE`**. `deduce()` reads the classpath; `setWebApplicationType` / `spring.main.web-application-type` overrides it (`none` is the documented property value). If the property is unset, type is **auto-detected**.

```properties
spring.main.web-application-type=none
```

**Listing 1.** Same flag in YAML: `spring.main.web-application-type: none`. Use this when web jars **must** stay on the classpath (shared codebase) but this process must not bind a port.

```java
@SpringBootApplication
public class WorkerApplication {

	public static void main(String[] args) {
		SpringApplication app = new SpringApplication(WorkerApplication.class);
		app.setWebApplicationType(WebApplicationType.NONE);
		app.run(args);
	}

	@Bean
	CommandLineRunner runJob() {
		return args -> {
			// CLI / batch / consumer work
		};
	}
}
```

**Listing 2.** Java API plus a `CommandLineRunner` — `run` executes just before `SpringApplication.run` returns, after the context is up ([[What is the SpringApplication class]]).

The first, cleaner fix is still **leave servlet/reactive server dependencies off** the classpath so deduction already yields `NONE`. `NONE` in tests is common so `@SpringBootTest` does not start a container.

```d2
direction: right
cp: "Classpath\nMVC? WebFlux? neither?" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
type: "WebApplicationType\nNONE / SERVLET / REACTIVE" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
ctx: "AnnotationConfigApplicationContext\nno embedded server" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}

cp -> type -> ctx
```

**Fig. 1.** Deduce, then optionally override. `NONE` means **not a web app** — no embedded server ([[Which embedded containers are supported by Spring Boot]]).

> [!warning] `none` is not `server.port=-1`
> **`server.port=-1`** still builds a **`WebApplicationContext`** and only turns **HTTP endpoints off**. **`NONE`** skips the web server **and** the web context type. Setting `none` does **not** remove `spring-boot-starter-web` (or Tomcat) from Maven/Gradle; those jars stay, they just are not used as a server. Excluding a web auto-configuration class is **not** the documented way to make a non-web app.

> [!warning] MVC plus WebFlux still looks like a servlet app
> If both stacks are on the classpath, deduction picks **MVC / `SERVLET`**, not `NONE`. A worker that transitively pulled `starter-web` will still start an embedded server until you set **`none`**. `CommandLineRunner` / `ApplicationRunner` run **just before** `SpringApplication.run` returns — that is the documented place for “do the job” in a non-web process.

> [!tip] Interview answer
> I either omit web starters so Boot deduces a non-web AnnotationConfigApplicationContext, or I set spring.main.web-application-type=none / setWebApplicationType(NONE) when web jars are unavoidable. NONE, SERVLET, and REACTIVE are the three types; NONE means no embedded server. Business logic goes in a CommandLineRunner. That is not the same as server.port=-1, which still creates a web context.
