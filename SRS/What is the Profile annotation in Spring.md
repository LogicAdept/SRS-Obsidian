<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Spring/Boot/Properties #Java/Annotations #SRS

# What is the Profile annotation in Spring?

> [!abstract] Short answer
> **`@Profile`** marks a `@Component` / `@Configuration` / `@Bean` (and Boot `@ConfigurationProperties`) as **eligible only when** those **profile names or expressions** are active on the `Environment`. It does **not** activate a profile. It is **`@Conditional`**: `ProfileCondition` calls `Environment.matchesProfiles(...)`. A class **without** `@Profile` registers **regardless** of profiles — that is **not** the `"default"` profile. `"default"` is the Environment fallback when **nothing** is active (`spring.profiles.default`).

## Gate registration, do not turn profiles on

Activate names with `spring.profiles.active` (or CLI / `setActiveProfiles`) ([[How do you activate a Spring profile]]). `@Profile` only **consumes** that set.

```java
@Configuration(proxyBeanMethods = false)
@Profile("production")
public class ProductionConfiguration {

	// ...
}
```

**Listing 1.** Type-level: the class is **not registered or processed** unless `production` is active. Then its **`@Bean` methods and `@Import`s are bypassed** as well. Boot: the same annotation on `@Component` / `@ConfigurationProperties` (if properties are registered via `@EnableConfigurationProperties`, put `@Profile` on **that** `@Configuration` class).

```java
@Configuration
public class AppConfig {

	@Bean("dataSource")
	@Profile("development")
	public DataSource standaloneDataSource() {
		return new EmbeddedDatabaseBuilder()
			.setType(EmbeddedDatabaseType.HSQL)
			.build();
	}

	@Bean("dataSource")
	@Profile("production")
	public DataSource jndiDataSource() throws Exception {
		return (DataSource) new InitialContext()
			.lookup("java:comp/env/jdbc/datasource");
	}
}
```

**Listing 2.** Method-level alternatives: **different Java method names**, same `@Bean` name. `@Profile` on **overloaded** methods (same Java name, different args) must be **consistent** — it cannot pick one overload.

Expressions: `!` NOT, `&` AND, `|` OR. **Do not mix `&` and `|` without parentheses** (`production & (us-east | eu-central)`). Array form `@Profile({"p1", "p2"})` is **OR**. `@Profile({"p1", "!p2"})` registers if `p1` is on **or** `p2` is off. You can meta-annotate (`@Production` → `@Profile("production")`).

```java
@Configuration
@Profile("default")
public class DefaultDataConfig {
	// ...
}
```

**Listing 3.** Beans **tagged** `@Profile("default")` run when **no** profile is active. Activating **any** profile turns `"default"` **off**. Rename the fallback with `spring.profiles.default` / `setDefaultProfiles`. Profile **files** (`application-dev.*`) are a separate overlay ([[How do profile-specific property files work in Spring Boot]]; [[What is a Spring profile]]).

```d2
direction: right
env: "Environment\nactive / default profiles" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
cond: "ProfileCondition\nmatchesProfiles" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
bean: "@Profile component\nregistered or skipped" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

env -> cond -> bean
```

**Fig. 1.** `@Profile` is `@Conditional`. `Condition.matches` reads the annotation and asks the Environment ([[How do ConditionalOn annotations drive auto-configuration]]).

> [!warning] No `@Profile` is not the `"default"` profile
> An unannotated `@Bean` is **always** registered. Dumps that put “no profile ⇒ default profile” confuse that with **`@Profile("default")`** and with `spring.profiles.default`. `@Profile` also does **not** load `application-{profile}.*` by itself.

> [!warning] `@Profile` does not activate anything
> `spring.profiles.active=mysql` (or `--spring.profiles.active`) turns `mysql` on so `@Profile("mysql")` matches. Two names in `@Profile({"postgres", "mysql"})` are **OR**, not activation. XML `profile="…"` on `<beans>` has **no** `&` / `|` expressions (only `!` and nesting).

> [!tip] Interview answer
> @Profile is a @Conditional that registers a component or @Bean only when the Environment has matching active profiles — names or expressions like production & us-east. It does not turn a profile on; spring.profiles.active does that. A class with no @Profile always loads; @Profile("default") is the fallback when nothing is active, and a @Profile on a @Configuration skips that class’s @Bean methods and @Imports.
