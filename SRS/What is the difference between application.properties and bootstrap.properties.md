<!--
reps: 0
priority: 0
-->
#Java/Spring/Cloud/Config #Java/Spring/Boot/Properties #SRS

# What is the difference between application.properties and bootstrap.properties?

> [!abstract] Short answer
> **`application.properties` / YAML** are Boot **config data** for the **main** `Environment`. **`bootstrap.properties` / YAML** belong to **Spring Cloud’s bootstrap context** (a **parent** context that runs first) so Config Server URI, `spring.application.name`, and decrypt keys exist **before** the main app starts. Since **Boot 2.4**, Config Client’s **default** is **`spring.config.import=optional:configserver:`** **in `application.properties`** — **no bootstrap file**. Legacy bootstrap needs **`spring-cloud-starter-bootstrap`** (or `spring.cloud.bootstrap.enabled=true` as a **system/env** property).

## Two files, two eras

**Main app (`application.*`).** Boot’s normal search order and profiles ([[What is Spring Boot property source precedence]]; [[What is the difference between application.properties and application.yml]]). This is where **application** settings live.

**Bootstrap (`bootstrap.*`).** Spring Cloud Commons: a **bootstrap `ApplicationContext`** is the **parent** of the main app. It uses basename **`bootstrap`** (`spring.cloud.bootstrap.name`) instead of `application`. Profiles load as `bootstrap-{profile}.*`. Disable the whole process with `spring.cloud.bootstrap.enabled=false`.

```properties
spring.config.import=optional:configserver:
```

**Listing 1.** Current Config Client (default). A bootstrap file is **not** required. Drop `optional:` to fail if the server is down. URI: `spring.cloud.config.uri` or append it on the import (`configserver:` + host); the **import location wins** over `uri`.

```yaml
spring:
  application:
    name: foo
  cloud:
    config:
      uri: ${SPRING_CONFIG_URI}
```

**Listing 2.** Legacy **config-first bootstrap**: Config Server address in **`bootstrap.yml`**. `spring.application.name` must be in **`bootstrap.[properties|yml]`** if it should become the **context ID**. `spring.profiles.active` for remote profile files should be set there too ([[How do you activate a Spring profile]]). Enable bootstrap with **`spring-cloud-starter-bootstrap`** or **`spring.cloud.bootstrap.enabled=true`** as a **system property or environment variable**.

Remote properties loaded in the bootstrap **phase** (the `"bootstrap"` `PropertySource`, e.g. Config Server) have **high** precedence and **are not** overridden by local `application.*` unless the server grants `spring.cloud.config.allowOverride`. The **`bootstrap.yml` file itself** is **low** precedence versus `application.yml` — it is for **defaults** that set up the parent context, not for winning over the main file ([[What is Spring Cloud Config]]).

```d2
direction: down
era: "Boot 2.4+ default" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
imp: "application.properties\nspring.config.import=configserver:" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
legacy: "Legacy Cloud bootstrap" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
boot: "bootstrap.properties\nparent context first" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

era -> imp
legacy -> boot
```

**Fig. 1.** Interview both: **import in `application.*`** today; **`bootstrap.*` + parent context** on older Cloud / when you opt back in.

> [!warning] `bootstrap.yml` does not beat `application.yml`
> Cloud docs: **`applicationConfig` from `bootstrap.yml` is lower** than `application.yml`. What **wins** is the **remote** `"bootstrap"` source. Logging that should apply to **all** events (including bootstrap) belongs in **`bootstrap.[yml|properties]`**, not only in `application.*`.

> [!warning] Putting the Config Server URI only in `application.properties` on a bootstrap stack is too late
> Config-first bootstrap reads **`spring.cloud.config.uri` from bootstrap config**. Current stacks that **do not** enable bootstrap **ignore `bootstrap.properties` unless** you add the bootstrap starter. `spring.cloud.bootstrap.enabled=true` must be a **system/env** property, not a line that only appears after the main context already started.

> [!tip] Interview answer
> application.properties is Boot’s main Environment; bootstrap.properties is Spring Cloud’s parent context so Config Server settings exist before the app context. Since Boot 2.4 the default is spring.config.import=configserver in application.properties and you do not need a bootstrap file. On legacy Cloud you enable bootstrap and put the config URI in bootstrap.yml; that file itself is low precedence, the remote properties are not.
