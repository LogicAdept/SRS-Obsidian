<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS

# What is CommandLineRunner and ApplicationRunner?

> [!abstract] Short answer
> Both are **`@FunctionalInterface`s** for a **bean that runs once** after the context **refresh**, **just before** `SpringApplication.run` returns. **`CommandLineRunner.run(String… args)`** is the raw `main` array. **`ApplicationRunner.run(ApplicationArguments)`** parses **`--option`** vs **non-option** args (`getOptionNames()`, `getOptionValues()`, `getNonOptionArgs()`, `getSourceArgs()`). Order several with **`Ordered` / `@Order`**. Prefer them over **`@PostConstruct`** for “after startup, before traffic.”

## After refresh, before ready

`SpringApplication` javadoc: create context → `CommandLinePropertySource` → **refresh** → **trigger runners**. `SpringApplicationRunListener.started` is **before** runners; **`ready` / `ApplicationReadyEvent`** is **after** all `CommandLineRunner` and `ApplicationRunner` beans ([[What is the SpringApplication class]]). Kubernetes **readiness** stays down while they run ([[How do you implement Kubernetes probes with Spring Boot]]).

```java
@Component
public class MyCommandLineRunner implements CommandLineRunner {

	@Override
	public void run(String... args) {
		// raw main arguments
	}
}
```

**Listing 1.** Official `CommandLineRunner`. Javadoc: if you want parsed options, use **`ApplicationRunner`**. Same contract as a `@Bean` lambda. Typical for **non-web** jobs (`WebApplicationType.NONE`) ([[How do you create a non-web Spring Boot application]]).

```java
@Component
public class MyApplicationRunner implements ApplicationRunner {

	@Override
	public void run(ApplicationArguments args) {
		args.getOptionNames();      // ["foo"] for --foo=bar
		args.getOptionValues("foo"); // ["bar"]; missing option → null
		args.getNonOptionArgs();
		args.getSourceArgs();       // original String[]
	}
}
```

**Listing 2.** `--foo` with no value → empty list; repeated `--foo=` → several values. You can **`@Autowired ApplicationArguments`** on any bean; Boot also maps `--` options into the **`Environment`** (`CommandLinePropertySource`) ([[What is Spring Boot property source precedence]]).

Several runners: implement **`Ordered`** or put **`@Order`** on the bean (lower value runs first). Spring Batch’s **`JobLauncherApplicationRunner`** is an `ApplicationRunner`.

```d2
direction: down
refresh: "context refresh\n(singletons ready)" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
run: "CommandLineRunner +\nApplicationRunner" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
ready: "ApplicationReadyEvent\nreadiness UP" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

refresh -> run -> ready
```

**Fig. 1.** Thrown `Exception` from `run` **fails startup**. This is not `@Scheduled` (repeat) and not a servlet `main` ([[How do you use schedulers in Spring Boot]]).

> [!warning] Not `@PostConstruct`
> Official availability docs: startup work belongs in **runners**, not `@PostConstruct` / `InitializingBean`. Those fire **during** bean creation, possibly **before** other singletons exist. Runners see a **fully refreshed** context.

> [!warning] Raw `String[]` is not parsed options
> `CommandLineRunner` does **not** split `--server.port=9000`. `ApplicationArguments` does. `--spring.profiles.active` is still an **Environment** property, not a special runner API.

> [!tip] Interview answer
> CommandLineRunner and ApplicationRunner are beans SpringApplication calls after refresh and before run returns. CommandLineRunner gets the raw args array; ApplicationRunner gets ApplicationArguments with option names and values. I order them with @Order and I do not put startup I/O in @PostConstruct.
