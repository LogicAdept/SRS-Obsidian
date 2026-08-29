<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #SRS

# What is the difference between application.properties and application.yml?

> [!abstract] Short answer
> Both are **config data** for the same `Environment`. **`.properties`** is **flat** `key=value`. **YAML** (`application.yaml` and other YAML variants) is **hierarchical** and is flattened to dotted keys (lists become `servers[0]`). They share locations and relaxed binding. **In the same location, `.properties` wins.** YAML is **not** loaded by **`@PropertySource`**. Prefer **one** format in the app.

## Same Environment, different syntax

`SpringApplication` loads YAML **if SnakeYAML is on the classpath** (`spring-boot-starter` brings it). YAML is flattened before it hits the `Environment`:

```yaml
my:
  servers:
    - "dev.example.com"
    - "another.example.com"
```

```properties
my.servers[0]=dev.example.com
my.servers[1]=another.example.com
```

**Listing 1.** Official flattening. Nested maps become dotted names (`environments.dev.url=…`). That is why YAML is nicer for trees and lists; the binder still sees **flat** properties ([[What is relaxed binding in Spring Boot]]).

Profile files work for **both** formats: `application-prod.yaml` overlays `application.yaml` the same way `application-prod.properties` overlays `application.properties` ([[How do profile-specific property files work in Spring Boot]]).

Multi-document files exist in **both**:

- YAML: a line of **`---`**
- `.properties`: **`#---`** or **`!---`** (exactly three hyphens, no leading space)

Later documents override earlier ones; use `spring.config.activate.on-profile` / `on-cloud-platform` on a document. **`@PropertySource` / `@TestPropertySource` cannot load multi-document files either.**

```d2
direction: right
props: "application.properties\nflat key=value" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
yaml: "application.yaml\nnested maps / lists" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
env: "Environment\nflattened keys" {
  width: 180
  height: 70
  style.fill: "#e8f5e9"
}

props -> env
yaml -> env
```

**Fig. 1.** Same search order as other config data. **Same directory:** `.properties` **beats** YAML. Stick to one format ([[What is Spring Boot property source precedence]]).

Placeholders (`${name:default}`) work in **both**. Map keys with `/` in YAML need **quoted** `[/key]` brackets.

> [!warning] `@PropertySource` is properties-only
> **YAML cannot be loaded** with `@PropertySource` or `@TestPropertySource`. Use a `.properties` file (or `YamlPropertySourceLoader` / `spring.config.import`). Multi-document files have the same restriction. Dump lore that “Boot always reads YAML from `@PropertySource`” is wrong.

> [!warning] Two files in one location is not “merge equally”
> Official: **`.properties` takes precedence** over YAML **in that location**. Indent errors in YAML drop or mis-bind keys; that is not a binder spellcheck ([[What happens if you misspell a ConfigurationProperties key]]). `---` in YAML vs `#---` in properties are easy to copy the wrong way.

> [!tip] Interview answer
> application.properties and application.yaml are the same config data with different syntax: YAML is hierarchical and Boot flattens it to dotted keys and [index] lists. In the same folder, .properties wins, and I should pick one format. @PropertySource still cannot load YAML, which is the usual trap.
