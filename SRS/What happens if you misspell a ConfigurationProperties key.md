<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #Java/Annotations #SRS

# What happens if you misspell a ConfigurationProperties key?

> [!abstract] Short answer
> **Nothing at runtime, by default.** `@ConfigurationProperties` has **`ignoreUnknownFields = true`**: a key that does not match a Java property is **dropped**, and the field keeps its **Java default**. `@Validated` + `@NotNull` fails startup only when the misspelling leaves a **required** field **null**. **`ignoreUnknownFields = false`** fails binding (`UnboundConfigurationPropertiesException`). The configuration processor is **IDE metadata**, not a startup check.

## Unknown keys are not a bind error

The binder maps Environment names onto the Java type (`prefix` + property). Relaxed names are **kebab / camel / underscore / `ENV_VAR`**, not a spellchecker: `first-name` binds to `firstName`; **`mail-hst` does not** bind to `mailHost`.

```java
@ConfigurationProperties("my.service")
public class MyServiceProperties {

	private String remoteAddress = "localhost";

	public String getRemoteAddress() {
		return this.remoteAddress;
	}

	public void setRemoteAddress(String remoteAddress) {
		this.remoteAddress = remoteAddress;
	}
}
```

```properties
my.service.remote-addres=prod.example
```

**Listing 1.** Typo `remote-addres`: with the default **`ignoreUnknownFields`**, the Environment entry is unused and **`remoteAddress` stays `localhost`**. Same outcome for a misspelled Boot key such as `server.prot` instead of `server.port`.

```java
@ConfigurationProperties(prefix = "my.service", ignoreUnknownFields = false)
```

**Listing 2.** Unknown keys **under this prefix** then fail bind (`UnboundConfigurationPropertiesException`). Keys **outside** the prefix are never “unknown fields” of this type. Wrong **type** is a different flag: **`ignoreInvalidFields`** defaults to **`false`** (invalid values fail unless you opt out).

```java
import java.net.InetAddress;

import jakarta.validation.constraints.NotNull;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.validation.annotation.Validated;

@ConfigurationProperties("my.service")
@Validated
public class MyServiceProperties {

	@NotNull
	private InetAddress remoteAddress;

	public InetAddress getRemoteAddress() {
		return this.remoteAddress;
	}

	public void setRemoteAddress(InetAddress remoteAddress) {
		this.remoteAddress = remoteAddress;
	}
}
```

**Listing 3.** Official validation pattern: a misspelling that leaves **`remoteAddress` null** fails startup. A field with a **non-null default** still “succeeds” with that default. Need a JSR-303 implementation on the classpath; cascade nested types with **`@Valid`**.

```d2
direction: right
file: "my.service.remote-addres=…" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
binder: "Binder\nignoreUnknownFields=true" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
bean: "Java field keeps default" {
  width: 200
  height: 50
  style.fill: "#ffebee"
}

file -> binder -> bean
```

**Fig. 1.** The app starts. Prod just never received the value ([[What is Spring Boot property source precedence]]). Metadata from **`spring-boot-configuration-processor`** only helps the **IDE** complete/warn in `application.properties` / YAML ([[What is the difference between Value and ConfigurationProperties]]).

Assert the bound bean in tests if the value is load-bearing. `/actuator/configprops` shows **what bound**, not the leftover typo (and it is **not** HTTP-exposed by default).

> [!warning] Defaults hide typos; `@NotNull` only catches null
> Official samples put defaults on `ip` / `port`. A misspelled key leaves those defaults in place — **`@NotNull` never fires**. `@Validated` is also **not** a global “unknown key” switch. **`ignoreUnknownFields = false`** only sees leftovers **under that prefix**.

> [!warning] Relaxed binding is not fuzzy matching
> `mailHost` accepts `mail-host`, `mail_host`, `mailHost`, and `MAILHOST` in the environment — **not** `mail-hst`. Misspelling the **prefix** (`my.servce`) means **no** property on that type is bound, and those keys are **not** unknown fields of `my.service`. Profile files do not change that rule ([[How do profile-specific property files work in Spring Boot]]).

> [!tip] Interview answer
> By default Boot ignores unknown ConfigurationProperties keys, so a typo keeps the Java default and the app still starts. I fail closed with ignoreUnknownFields false under that prefix, or with @Validated and @NotNull when the field must not stay null. Relaxed binding is not a spellchecker, and the annotation processor only warns in the IDE.
