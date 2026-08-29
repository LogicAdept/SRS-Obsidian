<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #SRS

# How do you create a custom Spring Boot starter?

> [!abstract] Short answer
> Split **autoconfigure** ( `@AutoConfiguration` + `@Conditional*` + `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` ) from an **empty starter POM** that depends on that module, the library, and **`spring-boot-starter`**. Name it **`acme-spring-boot-starter`**, never **`spring-boot-…`**. Prefix keys with a namespace you own (`acme`), not `spring` / `server` / `management`. Do **not** component-scan auto-config classes.

## Two jars, one opinion

Official layout for technology “acme”:

| Module | Role |
|---|---|
| **`acme-spring-boot`** | Auto-configuration code, `@ConfigurationProperties`, callbacks |
| **`acme-spring-boot-starter`** | Empty jar: depends on autoconfigure + **acme** + usual extras |

If there are no optional flavors, **one** module named **`acme-spring-boot-starter`** is fine. Keep library dependencies **optional** on the autoconfigure module so apps can depend on it without pulling acme; then conditions **back off**.

```
com.mycorp.libx.autoconfigure.LibXAutoConfiguration
com.mycorp.libx.autoconfigure.LibXWebAutoConfiguration
```

**Listing 1.** In the **published** autoconfigure jar: `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`, one FQCN per line ([[How does Spring Boot find auto-configuration classes]]). Boot 3+ does **not** read the old `EnableAutoConfiguration` key in `spring.factories`.

```java
@AutoConfiguration
@ConditionalOnClass(AcmeClient.class)
@EnableConfigurationProperties(AcmeProperties.class)
public class AcmeAutoConfiguration {

	@Bean
	@ConditionalOnMissingBean
	AcmeClient acmeClient(AcmeProperties properties) {
		return new AcmeClient(properties);
	}
}
```

**Listing 2.** `@AutoConfiguration` is `@Configuration`. Typical pair: **`@ConditionalOnClass`** (library present) and **`@ConditionalOnMissingBean`** (user can override) ([[How do ConditionalOn annotations drive auto-configuration]]). Isolate `OnClass` on a nested `@Configuration` if the `@Bean` return type would otherwise load a missing class. Order with `before` / `after` on `@AutoConfiguration` (bean **definition** order only).

```java
@ConfigurationProperties("acme")
public class AcmeProperties {

	/**
	 * Whether to check the location of acme resources.
	 */
	private boolean checkLocation = true;
	// getters/setters
}
```

**Listing 3.** Unique prefix. Field Javadoc (plain text) feeds **`spring-boot-configuration-processor`**. Records: class-level `@param`. Boolean descriptions start with **Whether** / **Enable**. Add **`spring-boot-autoconfigure-processor`** so `META-INF/spring-autoconfigure-metadata.properties` can **eager-filter** conditions at startup.

The starter POM should depend on autoconfigure, the library, and **`spring-boot-starter`** (directly or via another starter). Do **not** ship unused optional dependencies ([[Which common Spring Boot starters do you know]]).

```d2
direction: down
starter: "acme-spring-boot-starter\n(empty POM)" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
auto: "acme-spring-boot\n@AutoConfiguration" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
imports: "AutoConfiguration.imports" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

starter -> auto -> imports
```

**Fig. 1.** Users add **one** starter dependency. Boot discovers auto-config from the **imports file**, not from the app’s `@ComponentScan`. Test with **`ApplicationContextRunner`** / **`FilteredClassLoader`** (same guide).

> [!warning] Do not scan auto-config, and do not name it `spring-boot-*`
> List classes **only** in `.imports`. Keep them out of a scanned package; do **not** put `@ComponentScan` on the auto-config class (`@Import` instead). A third-party starter named `spring-boot-starter-acme` collides with Boot’s reserved prefix — use **`acme-spring-boot-starter`**. Keys under `spring.*` / `server.*` / `management.*` can break when Boot changes those namespaces ([[What is the difference between Value and ConfigurationProperties]]).

> [!warning] Optional features belong in conditions, not a fat starter
> If acme has flavors, keep autoconfigure separate so another team can write a **different** starter. Putting every optional jar on the starter classpath makes `@ConditionalOnClass` always true. Confirm with the conditions report ([[How can you debug which auto-configuration classes applied]]).

> [!tip] Interview answer
> A custom starter is usually two modules: autoconfigure with @AutoConfiguration, @ConditionalOnClass, @ConditionalOnMissingBean, and AutoConfiguration.imports, plus an empty starter POM that depends on that jar, the library, and spring-boot-starter. I name it acme-spring-boot-starter, prefix properties with acme, and I never component-scan the auto-config classes. On Boot 3 I do not register auto-config in spring.factories.
