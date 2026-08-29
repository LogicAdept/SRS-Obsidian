<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #SRS

# What is Spring Boot property source precedence?

> [!abstract] Short answer
> Boot builds one `Environment` from many `PropertySource`s. **Later sources override earlier ones.** The documented list is **lowest → highest**: `setDefaultProperties`, then `@PropertySource`, then **config data** (`application*.properties` / YAML), then `random.*`, **OS env**, **system properties**, **JNDI**, **`SPRING_APPLICATION_JSON`**, **command-line `--`**, then **test** sources, then **Devtools**. That is why `--server.port` and `SERVER_PORT` beat packaged YAML without a rebuild.

## Later in the list wins

Official rule: *later property sources override earlier ones*. Interview cheat-sheets often print that list **upside down**.

Highest → lowest (each row loses to the row above):

| | Source |
|---|---|
| Tests / Devtools | Devtools `$HOME/.config/spring-boot` (when active), then `@TestPropertySource`, `@DynamicPropertySource`, `@SpringBootTest` `properties` |
| CLI / JSON | Command-line `--key=value`, then `SPRING_APPLICATION_JSON` / `spring.application.json` |
| Container | JNDI `java:comp/env`, then **system properties**, then **OS environment** |
| Random | `RandomValuePropertySource` (`random.*` only) |
| Files | **Config data** (see below) |
| Lowest | `@PropertySource` on `@Configuration`, then `SpringApplication.setDefaultProperties` |

Java field defaults on a `@ConfigurationProperties` type are **not** a `PropertySource`. They apply only if **nothing** bound the field ([[What is relaxed binding in Spring Boot]]).

**Config data** (the `application.*` slot) has its **own** later-wins order:

1. Packaged `application.properties` / YAML
2. Packaged `application-{profile}.*`
3. **Outside** the jar: `application.*`
4. **Outside** the jar: `application-{profile}.*`

Profile files **overlay** the base file at that location; they do not wipe the rest of the `Environment` ([[How do profile-specific property files work in Spring Boot]]; [[How do you activate a Spring profile]]).

```bash
java -jar app.jar --name="Spring"
```

**Listing 1.** Command-line options (`--`, as in `--server.port=9000`) become Environment properties and **always beat file-based sources**. Disable with `SpringApplication.setAddCommandLineProperties(false)`.

```
$ SPRING_APPLICATION_JSON='{"my":{"name":"test"}}' java -jar myapp.jar
```

**Listing 2.** JSON block → `my.name=test`. Same JSON via `-Dspring.application.json=…` or `--spring.application.json=…`. A JSON **`null`** does **not** override a lower source.

Search locations for files (later overrides earlier): classpath root → classpath `/config` → current directory → `./config/` → `./config/*/`. Same directory: **`.properties` beats YAML**. `spring.config.location` **replaces** those defaults; `spring.config.additional-location` **adds** higher locations. Those three name/location properties must themselves come from env / system / CLI — they are read **before** files load.

```d2
direction: right
files: "application*.yml / .properties\npackaged then external" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
os: "OS env then\nsystem properties" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
cli: "--args and\nSPRING_APPLICATION_JSON" {
  width: 200
  height: 70
  style.fill: "#e8f5e9"
}

files -> os -> cli
```

**Fig. 1.** Twelve-factor idea: one artifact; env and CLI override packaged defaults ([[How do you change the port of the embedded server]]). Diagnose with Actuator **`env`** / **`configprops`** (not HTTP-exposed by default).

> [!warning] `@PropertySource` is weaker than `application.properties`
> It is **below** config data, and it is registered only at **context refresh** — too late for `logging.*` and `spring.main.*`. Dump lists that put `@PropertySource` **above** YAML are wrong. OS env is **not** the same slot as `SPRING_APPLICATION_JSON` (JSON wins). Tests and Devtools (`$HOME/.config/spring-boot`) sit **above** CLI.

> [!warning] “Profile YAML beats application.yml” is only the file slot
> `application-prod` beats `application` **among config data**. `SERVER_PORT` / `--server.port` still win. Several active profiles: **last** profile’s file wins at that location group. `@PropertySource` cannot be the place you set `spring.profiles.active` if you need it before refresh.

> [!tip] Interview answer
> Boot’s Environment is last-wins: later PropertySources override earlier ones, so command-line and SPRING_APPLICATION_JSON beat system properties and env, which beat application files. Inside files, external and profile-specific overlay the packaged application.yml. @PropertySource is below those files and too late for logging and spring.main, and Java field defaults are not even a PropertySource.
