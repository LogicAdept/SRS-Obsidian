<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #Java/Annotations #SRS

# What is relaxed binding in Spring Boot?

> [!abstract] Short answer
> **Relaxed binding** lets `@ConfigurationProperties` map an Environment name onto a Java property **without an exact string match**. The same `firstName` field accepts **kebab** `first-name` (recommended in files), **camel** `firstName`, **underscore** `first_name`, and the **env** form `FIRSTNAME` (dots → `_`, dashes **removed**, then uppercase). That is how containers set `SPRING_…` variables. It is **not** fuzzy spelling.

## One Java property, several Environment names

The binder matches **canonical kebab-case** to the JavaBean / constructor name. Official example: `@ConfigurationProperties("my.main-project.person")` with field **`firstName`**.

```java
@ConfigurationProperties("my.main-project.person")
public class MyPersonProperties {

	private String firstName;

	public String getFirstName() {
		return this.firstName;
	}

	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}
}
```

**Listing 1.** The **`prefix`** on the annotation **must** be kebab-case (`my.main-project.person`). These Environment names all bind that field:

| Name | Where |
|---|---|
| `my.main-project.person.first-name` | Files (recommended) |
| `my.main-project.person.firstName` | Files / system properties |
| `my.main-project.person.first_name` | Files / system properties |
| `MY_MAINPROJECT_PERSON_FIRSTNAME` | OS environment |

```properties
# canonical kebab — prefer this in application.properties / YAML
my.main-project.person.first-name=Rod
```

**Listing 2.** Same value as `firstName` / `first_name` in a properties file, or `MY_MAINPROJECT_PERSON_FIRSTNAME` in the environment. Env conversion: **dots → `_`**, **strip `-`**, **uppercase** (`spring.main.log-startup-info` → `SPRING_MAIN_LOGSTARTUPINFO`). Lists: `my.service[0].other` → `MY_SERVICE_0_OTHER`.

```d2
direction: right
names: "first-name · firstName\nfirst_name · FIRSTNAME" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
bind: "Relaxed binder\ncanonical kebab" {
  width: 200
  height: 70
  style.fill: "#fff3e0"
}
field: "Java firstName" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}

names -> bind -> field
```

**Fig. 1.** Files and system properties allow camel / kebab / underscore. **Environment variables** are the uppercase form only (`systemEnvironment` and sources whose name ends with `-systemEnvironment`). Map keys from env are **lowercased** ([[What is Spring Boot property source precedence]]).

`@Value("${…}")` is **not** the same API: `@ConfigurationProperties` does **not** evaluate SpEL. Placeholders should use **kebab** (`${demo.item-price}`) so Boot applies the **same** relaxed lookup (camel + `DEMO_ITEMPRICE`). `${demo.itemPrice}` **misses** `demo.item-price` in the file ([[What is the difference between Value and ConfigurationProperties]]).

> [!warning] Env names drop dashes; they do not spell-check
> `main-project` becomes **`MAINPROJECT`**, not `MAIN_PROJECT`. `mailHost` accepts `mail-host` / `mail_host` / `MAILHOST` — **not** `mail-hst`. A leftover unknown key still keeps the Java default ([[What happens if you misspell a ConfigurationProperties key]]).

> [!warning] `@Value` with camel in the placeholder is a weaker match
> Relaxed rules are specified for **`@ConfigurationProperties`**. `@Value` only gets that Environment lookup if the placeholder is **canonical kebab**. SpEL (`#{…}`) is a `@Value` feature and is **out of scope** for `@ConfigurationProperties`.

> [!tip] Interview answer
> Relaxed binding means a ConfigurationProperties field like firstName also binds first-name, first_name, and the env var with dots turned into underscores and dashes stripped. That is why SPRING_MAIN_LOGSTARTUPINFO sets spring.main.log-startup-info in a container. It is not a spellchecker, and @Value only gets the same lookup if I write the placeholder in kebab-case.
