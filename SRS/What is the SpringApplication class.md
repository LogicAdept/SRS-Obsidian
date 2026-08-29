<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Core/IoC #SRS

# What is the SpringApplication class?

> [!abstract] Short answer
> **`SpringApplication`** (`org.springframework.boot`) is Boot’s **bootstrap** from `main`: it **creates the right `ApplicationContext`** from the classpath (`WebApplicationType`), registers a **`CommandLinePropertySource`** for `args`, **`refresh()`es** (singletons load), then runs **`CommandLineRunner` / `ApplicationRunner`** beans. Typical call: **`SpringApplication.run(MyApplication.class, args)`**. It is **not** `new AnnotationConfigApplicationContext(...)` — web vs non-web context, banner, failure analyzers, JVM shutdown hook, and `spring.main.*` binding are extra.

## Four documented bootstrap steps

Javadoc order:

1. Create an **appropriate** `ApplicationContext` (servlet / reactive / plain) ([[What ApplicationContext type does Spring Boot create for a web app]]).
2. Register **`CommandLinePropertySource`** so command-line args are Environment properties (`--foo=bar`, inject `ApplicationArguments` or `@Value`).
3. **Refresh** the context (singleton beans, including auto-config because the source is usually `@SpringBootApplication`) ([[What is the EnableAutoConfiguration annotation]]).
4. Invoke **`CommandLineRunner`** beans (and **`ApplicationRunner`** — same moment, just before `run` returns).

```java
@SpringBootApplication
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}
}
```

**Listing 1.** Usual entry. Constructor / `run` **sources** are `@Configuration` (or `@Component`) types; you can also pass a FQCN, an XML/Groovy resource, or a **package name** to scan.

```java
SpringApplication application = new SpringApplication(MyApplication.class);
application.setBannerMode(Banner.Mode.OFF);
application.run(args);
```

**Listing 2.** Instance form when defaults are wrong. Same knobs as properties: `spring.main.banner-mode` (`console` / `log` / `off`), `spring.main.web-application-type`, `spring.main.lazy-initialization`, `spring.main.sources`, `spring.main.log-startup-info=false`. Hierarchy / fluent API: **`SpringApplicationBuilder`** (`parent` / `child`; web beans belong in the **child**; one shared `Environment`).

```java
@Component
public class MyCommandLineRunner implements CommandLineRunner {

	@Override
	public void run(String... args) {
		// after refresh, before run() returns
	}
}
```

**Listing 3.** Startup work goes here (or `ApplicationRunner`), **not** `@PostConstruct`, if it must finish before the app is **ready** for traffic. Several runners: `Ordered` / `@Order`. Exit: JVM **shutdown hook** closes the context; `SpringApplication.exit` plus `ExitCodeGenerator`.

```d2
direction: down
main: "main(args)" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
sa: "SpringApplication.run" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
ctx: "ApplicationContext\n(web type from classpath)" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
run: "CommandLineRunner\nApplicationRunner" {
  width: 200
  height: 70
  style.fill: "#f3e5f5"
}

main -> sa -> ctx -> run
```

**Fig. 1.** Deduce context, bind args, refresh, then runners. Override type with `setWebApplicationType` / `spring.main.web-application-type=none` ([[How do you create a non-web Spring Boot application]]).

Startup failures go through **`FailureAnalyzer`** beans (port in use, and so on). If none match, `--debug` logs the conditions report ([[How can you debug which auto-configuration classes applied]]). Banner: `banner.txt` on the classpath or `spring.banner.location` (`springBootBanner` bean).

> [!warning] `run` is not `new AnnotationConfigApplicationContext`
> A servlet classpath still builds **`AnnotationConfigServletWebServerApplicationContext`** and starts the **embedded** server. Auto-configuration is **not** a hidden `SpringApplication` constructor argument — it runs because the **source class** is `@SpringBootApplication` / `@EnableAutoConfiguration`. `SpringApplication` still adds args, banner, analyzers, and runners on top of a plain Framework refresh.

> [!warning] Runners run before the app is “ready”
> Readiness waits until runners finish. Putting long startup I/O in `@PostConstruct` is the documented miss. `lazy-initialization` is **off** by default: it shortens startup and **hides** misconfigured beans until first use.

> [!tip] Interview answer
> SpringApplication is Boot’s main bootstrap: run(MyApplication.class, args) picks an ApplicationContext from the classpath, exposes command-line args, refreshes, then calls CommandLineRunner and ApplicationRunner. I customize with a SpringApplication instance or spring.main properties. It is more than new AnnotationConfigApplicationContext — web type, banner, failure analyzers, and the shutdown hook are part of that class.
