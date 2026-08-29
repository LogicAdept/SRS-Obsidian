<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #SRS

# How do you activate a Spring profile?

> [!abstract] Short answer
> Set **`spring.profiles.active`** to a comma-separated list of names. Put it in **`application.properties`**, as an OS environment variable **`SPRING_PROFILES_ACTIVE`**, as a JVM system property, or as **`--spring.profiles.active=`** on the command line. Later PropertySources **replace** earlier ones, so the CLI switch overrides the file. **`@Profile`** does not activate anything — it only **registers** a `@Component` / `@Configuration` / `@Bean` when that profile is already active.

## Ways to turn a profile on

A profile is a named grouping of beans and configuration ([[What is a Spring profile]]). Boot (and the `Environment`) treat `spring.profiles.active` like any other property: **the highest PropertySource wins** ([[What is Spring Boot property source precedence]]). Among the usual knobs:

| Source | Example | Relative rank |
|---|---|---|
| Config data | `spring.profiles.active=dev` in `application.properties` | Lowest of these |
| OS environment | `SPRING_PROFILES_ACTIVE=dev` (dots → underscores, upper case) | Above config files |
| JVM system property | `-Dspring.profiles.active=dev` | Above env vars |
| Command line | `java -jar app.jar --spring.profiles.active=prod` | Highest of these |

```properties
spring.profiles.active=dev,hsqldb
```

**Listing 1.** Comma-separated active profiles in the **base** `application.properties`. A command-line switch **replaces** this list.

```bash
java -jar app.jar --spring.profiles.active=prod
```

**Listing 2.** CLI form. This **replaces** profiles from `application.properties`; it does not append.

You can also call **`SpringApplication.setAdditionalProfiles(...)`** before `run`, or **`ConfigurableEnvironment.setActiveProfiles(...)`**. Tests use **`@ActiveProfiles`**. If **nothing** is activated, the fallback profile is **`default`** (`spring.profiles.default` / `setDefaultProfiles` to change it; `none` disables the fallback).

`spring.profiles.include` **adds** names instead of replacing `spring.profiles.active`. Included profiles are applied **before** the `active` list. Profile **groups** (`spring.profiles.group.production=proddb,prodmq`) expand one name into several.

```d2
direction: right
src: "application.properties\nSPRING_PROFILES_ACTIVE\n-D / --spring.profiles.active" {
  width: 260
  height: 90
  style.fill: "#e3f2fd"
}
env: "Environment\nactive profiles" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
beans: "@Profile(\"prod\")\nbeans registered" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}
files: "application-prod.*\noverlays base file" {
  width: 200
  height: 70
  style.fill: "#f3e5f5"
}

src -> env
env -> beans
env -> files
```

**Fig. 1.** Activation fills the `Environment`. `@Profile` and `application-{profile}` files **consume** that set ([[How do profile-specific property files work in Spring Boot]]).

Once a profile is active, `@Profile("prod")` (or an expression such as `"p1 & p2"` / `"!p2"`) makes a `@Component`, `@Configuration`, `@ConfigurationProperties`, or `@Bean` method **eligible**. Omit `@Profile` and the component registers regardless of profiles.

> [!warning] `--spring.profiles.active` is not a filename
> The switch **activates** a profile named `prod`. The file `application-prod.properties` is a **separate** overlay that Boot loads **because** `prod` is active. `--spring.profiles.active=application-prod` would look for a profile literally named `application-prod`. Do not put `spring.profiles.active` (or `include` / `default` / `group`) inside `application-{profile}.*` — those keys are valid only in **non-profile-specific** documents.

> [!warning] `active` replaces; `include` appends
> Two `--spring.profiles.active` values are not “merged” with the file: the **highest** source wins and **replaces** the list. Use `spring.profiles.include` (or `setAdditionalProfiles`) when you want **dev plus** extra names. `@Profile` on **overloaded** `@Bean` methods of the same Java name must be consistent — it cannot pick one overload over another.

> [!tip] Interview answer
> I set spring.profiles.active — in application.properties, as SPRING_PROFILES_ACTIVE, or with --spring.profiles.active on the command line, where the highest PropertySource wins so CLI overrides the file. That activates the profile; @Profile only gates which beans register, and application-prod.properties is the overlay file, not the activation switch. If I need to add profiles instead of replacing them I use spring.profiles.include or setAdditionalProfiles, and if none are set Boot falls back to default.
