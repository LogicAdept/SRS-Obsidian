<!--
reps: 0
priority: 0
-->
#Java/Spring/Batch #Java/Spring/Security/FilterChain #SRS

# How do you handle security for a Spring Batch application?

> [!abstract] Short answer
> Spring Batch **does not expose a `/batch/**` HTTP API**. A `Job` bean is a process definition, not an access rule. **HTTP launch** is **your** MVC controller calling **`JobOperator`** — protect **that** path with **`authorizeHttpRequests` + `requestMatchers`** (and **`httpBasic`** or form login). **Command-line** and Boot **`JobLauncherApplicationRunner`** never hit the filter chain: they run **inside the JVM** (or a new process) with **no** servlet request.

## Three launch surfaces, three controls

Spring Batch’s “Running a Job” chapter splits launch into **command line** vs **web container**. Boot adds a third: run a `Job` **on startup**.

| How the job starts | What Spring Batch / Boot actually provides | What Spring Security sees |
| --- | --- | --- |
| **`CommandLineJobOperator`** (scheduler / `java … start jobName`) | New JVM, `main`, `JobOperator` | **Nothing** — no `FilterChainProxy` |
| Boot **`JobLauncherApplicationRunner`** | `ApplicationRunner` launches a context `Job` after startup | **Nothing** — no HTTP call |
| Your **`@Controller`** + **`JobOperator.start`** | Official web example maps **`/jobOperator.html`**, not `/batch/**` | **`AuthorizationFilter`** on **that** mapping |

There is **no** built-in Actuator “run job” endpoint. Metrics may use a `spring.batch` prefix; they do not start or stop jobs.

```java
@Controller
public class JobOperatorController {

	@Autowired
	JobOperator jobOperator;

	@Autowired
	Job job;

	@RequestMapping("/jobOperator.html")
	public void handle() throws Exception {
		this.jobOperator.start(this.job, new JobParameters());
	}
}
```

**Listing 1.** Conceptual controller from the Spring Batch **Running Jobs from within a Web Container** section (current docs use **`JobOperator`**, not a framework `/batch` servlet).

```java
@Bean
SecurityFilterChain batchLaunchChain(HttpSecurity http) throws Exception {
	http
		.authorizeHttpRequests((authorize) -> authorize
			.requestMatchers("/jobOperator.html").authenticated()
			.anyRequest().permitAll())
		.httpBasic(Customizer.withDefaults());
	return http.build();
}
```

**Listing 2.** Current servlet DSL: **`authorizeHttpRequests`** / **`requestMatchers`**. The dump’s **`authorizeRequests()` + `antMatchers("/batch/**")`** is the old matcher API and a **path Spring Batch does not register**.

If Spring Security is on the classpath of a **web** app, Boot already authenticates **every** request by default (form login or HTTP Basic from `Accept`). A custom **`SecurityFilterChain`** replaces that default — so **`anyRequest().permitAll()`** really does leave the rest open. Prefer **`hasRole` / `hasAuthority`** on launch URLs, not only **`authenticated()`**. Optional second line of defense: **`@EnableMethodSecurity`** and **`@PreAuthorize`** on the service that calls **`JobOperator`**.

HTTP launch should be **asynchronous** (`JobOperatorFactoryBean.setTaskExecutor`, e.g. **`SimpleAsyncTaskExecutor`**) so the request is not held for the whole job.

## In-process and CLI jobs bypass HTTP rules

Boot: if a **single** `Job` bean exists, **`JobLauncherApplicationRunner`** executes it on startup. Disable that when launch should go only through a secured controller:

```properties
spring.batch.job.enabled=false
```

**Listing 3.** Stops auto-run. **`spring.batch.job.name`** selects which bean runs when several `Job`s exist and auto-run is still on.

```d2
direction: down
http: "HttpRequest\n/jobOperator.html" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
fc: "SecurityFilterChain\nrequestMatchers" {
  width: 220
  height: 50
  style.fill: "#c8e6c9"
}
op: "JobOperator.start" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}
cli: "CommandLineJobOperator\nor JobLauncherApplicationRunner" {
  width: 260
  height: 55
  style.fill: "#fce4ec"
}

http -> fc
fc -> op
cli -> op: "no filter"
```

**Fig. 1.** Servlet filters wrap **requests**, not **`JobOperator`** itself.

A JAR started by cron with **`CommandLineJobOperator`** is secured by **OS / scheduler identity**, job-repository credentials, and who can reach the box — not by **`/batch/**`**. Same for a `CommandLineRunner` you write that calls **`JobOperator`** locally ([[What is CommandLineRunner and ApplicationRunner]], [[How do you configure HTTP Basic authentication in Spring Security]], [[What is the difference between antMatchers mvcMatchers and requestMatchers]]).

> [!warning] `/batch/**` is not a Spring Batch mapping
> Protect **the `@RequestMapping` you actually declared**. Matching a dump path that nothing serves looks “secure” and still leaves **`/jobOperator.html`** (or your real API) open if your chain ends in **`permitAll`**. Use **`requestMatchers`**, not **`antMatchers`**, on Spring Security 6+.

> [!warning] A secured URL does not authenticate startup or CLI
> **`JobLauncherApplicationRunner.run`** and **`CommandLineJobOperator`** never enter **`FilterChainProxy`**. Leave **`spring.batch.job.enabled`** on, and the job still starts as the process user with **no** HTTP Basic. The `Job` `@Bean` is not an authorization rule ([[What is spring-boot-starter-security]], [[What is Spring Batch]]).

> [!tip] Interview answer
> Spring Batch has no built-in /batch security filter. HTTP launch is your controller plus JobOperator; lock that mapping with authorizeHttpRequests and an authentication mechanism. Command-line and Boot’s JobLauncherApplicationRunner start the same Job without any servlet request, so you disable auto-run if only the web API should launch jobs. The old antMatchers("/batch/**") snippet does not match a framework endpoint.
