<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/Properties #Java/Annotations #Java/Spring/Core/IoC/SpEL #SRS

# What is the difference between Value and ConfigurationProperties?

> [!abstract] Short answer
> **`@Value`** is a **core Spring** injection of **one** expression: `${…}` placeholders or **`#{…}` SpEL**. **`@ConfigurationProperties`** is Boot’s **type-safe binder**: a **prefix** maps a **group** of Environment keys onto one Java type (JavaBean **or** constructor/record), with **relaxed binding**, **metadata**, and optional **`@Validated`**. Official table: `@ConfigurationProperties` has relaxed binding + metadata, **no SpEL**; `@Value` has **limited** relaxed binding, **no** metadata, **yes SpEL**. Prefer `@ConfigurationProperties` for any cohesive set of keys.

## One expression vs one typed prefix

`@Value` is processed by `AutowiredAnnotationBeanPostProcessor`. A typical inject is `${payment.gateway.api-key}` or a SpEL like `#{systemProperties.myProp}`. Related keys scatter across fields and classes; there is **no** Boot metadata and **no** prefix-level Bean Validation.

```java
@Value("${payment.gateway.api-key}")
private String apiKey;
```

**Listing 1.** One Environment key (plus optional `${key:default}`). Use **canonical kebab** in the placeholder or you **miss** the kebab form in the file ([[What is relaxed binding in Spring Boot]]).

```java
@ConfigurationProperties("my.service")
@Validated
public class MyProperties {

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

**Listing 2.** Official validation pattern: JSR-303 on the **type**, plus `@Validated`. Nested types need `@Valid` to cascade. Need a validator on the classpath ([[What happens if you misspell a ConfigurationProperties key]]).

```java
@Configuration(proxyBeanMethods = false)
@EnableConfigurationProperties(MyProperties.class)
public class MyConfiguration {
}
```

**Listing 3.** Register the type (or `@ConfigurationPropertiesScan` on a `@Configuration` / `@SpringBootApplication` class). Constructor binding — including **records** — **cannot** be a regular `@Component` / `@Bean` / `@Import`; it must go through this infrastructure. Compile with **`-parameters`** (Boot parent / Gradle plugin does).

| Feature | `@ConfigurationProperties` | `@Value` |
|---|---|---|
| Relaxed binding | Yes | Limited (kebab placeholder) |
| Metadata (`spring-boot-configuration-processor`) | Yes | No |
| SpEL | No | Yes |

Official comparison. SpEL in a **property file** is **not** evaluated when the Environment is loaded; it **is** evaluated if that string is consumed through `@Value` ([[What is Spring Expression Language]]).

```d2
direction: right
value: "@Value one expression\n${…} or #{…} SpEL" {
  width: 240
  height: 70
  style.fill: "#fff3e0"
}
cp: "@ConfigurationProperties\ntyped prefix group" {
  width: 240
  height: 70
  style.fill: "#e3f2fd"
}
env: "Environment" {
  width: 140
  height: 50
  style.fill: "#e8f5e9"
}

env -> value
env -> cp
```

**Fig. 1.** Same `Environment`; `@Value` is one expression, `@ConfigurationProperties` is a bound type.

JavaBean binding uses setters (or pre-initialized nested objects). A **single parameterized constructor** (or a **record**) selects constructor binding; multiple constructors need `@ConstructorBinding`. Java **field defaults are not in the Environment**: `@Value("${my.service.enabled}")` does **not** see the POJO’s `false` default.

> [!warning] `@Value` is not a config object
> Dumps that `@Value` a whole gateway (`api-key`, `url`, `timeout`) get **no** grouped `@NotBlank` / `@Min`, **no** IDE metadata, and **weaker** relaxed names if the placeholder is camelCase. Boot’s recommendation for **your** keys is a `@ConfigurationProperties` POJO you inject into other beans.

> [!warning] Constructor-bound types are not `@Component`
> Records and constructor binding fail if you register the class as a normal Spring bean. Use `@EnableConfigurationProperties` or `@ConfigurationPropertiesScan`. This cue is Spring **`@Value`**, not Lombok `@Value`.

> [!tip] Interview answer
> @Value injects one placeholder or SpEL expression; it is core Spring and does not validate a group of keys. @ConfigurationProperties binds a prefix into a typed object with relaxed binding, metadata, and optional @Validated. I use ConfigurationProperties for any cohesive config and keep @Value for a single standalone key or actual SpEL.
