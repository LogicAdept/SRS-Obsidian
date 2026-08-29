<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #SRS

# How does Spring Boot auto-configuration decide which beans to create?

> [!abstract] Short answer
> It never component-scans auto-config. `@EnableAutoConfiguration` loads candidate **`@AutoConfiguration`** class names from **`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`**, drops **exclusions**, then each class and `@Bean` method is a Spring **`@Conditional`**. The usual pair is **`@ConditionalOnClass`** (the library is present) and **`@ConditionalOnMissingBean`** (you did not already define that type). Auto-config is a **`DeferredImportSelector`**, so **user `@Bean` methods run first** and win.

## Candidates, then conditions, then `@Bean` methods

Starters put auto-configuration on the classpath. Boot **3+** does **not** read the old `EnableAutoConfiguration` key in `spring.factories` ([[How does Spring Boot find auto-configuration classes]]). `@SpringBootApplication` includes `@EnableAutoConfiguration`, which imports **`AutoConfigurationImportSelector`**.

```
com.example.acme.autoconfigure.AcmeAutoConfiguration
```

**Listing 1.** One FQCN per line in the **published** jar. `#` comments. A class listed here is still skipped if `exclude` / `spring.autoconfigure.exclude` names it ([[How do you disable a specific auto-configuration class]]).

Each listed type is `@Configuration` (`@AutoConfiguration`). **Class-level** conditions decide whether that configuration is **registered at all**. **Method-level** conditions decide **individual beans**. Typical gates ([[How do ConditionalOn annotations drive auto-configuration]]):

| Condition | Bean is created when |
|---|---|
| `@ConditionalOnClass` | Named types are on the **classpath** (ASM; safe if the class is absent) |
| `@ConditionalOnMissingBean` | No matching bean **already** in the factory (type defaults to the `@Bean` **return type**) |
| `@ConditionalOnProperty` | Environment key is present and not `false` (or `havingValue` matches) |
| `@ConditionalOnWebApplication` | Context is servlet / reactive / any web |

```java
@AutoConfiguration
public class AcmeAutoConfiguration {

	@Configuration(proxyBeanMethods = false)
	@ConditionalOnClass(AcmeClient.class)
	static class AcmeClientConfiguration {

		@Bean
		@ConditionalOnMissingBean
		AcmeClient acmeClient(AcmeProperties properties) {
			return new AcmeClient(properties);
		}
	}
}
```

**Listing 2.** Put `@ConditionalOnClass` on a **nested** `@Configuration` so the JVM does not load `AcmeClient` before the condition. `@ConditionalOnMissingBean` on the factory method is why **your** `AcmeClient` `@Bean` replaces Boot’s. Auto-config is processed **after** user definitions — that order is **not** guaranteed among ordinary application `@Configuration` classes.

`before` / `after` on `@AutoConfiguration` (or `@AutoConfigureBefore`) order **bean definitions**, not “create this instance first.” Conditions can still skip the whole class. The autoconfigure annotation processor writes **`META-INF/spring-autoconfigure-metadata.properties`** so Boot can **eager-filter** some conditions before loading the class ([[How do you create a custom Spring Boot starter]]).

```d2
direction: down
imports: "AutoConfiguration.imports\nacross the classpath" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
excl: "exclude / excludeName" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
cond: "@ConditionalOnClass / Property\n/ WebApplication / …" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
bean: "@Bean + OnMissingBean\nuser beans already present" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

imports -> excl -> cond -> bean
```

**Fig. 1.** Classic example from the reference: **HSQLDB** on the classpath and **no** user `DataSource` → Boot creates an in-memory database; define a `DataSource` and that auto-config **backs off**. Confirm with **`--debug`** / the conditions report ([[How can you debug which auto-configuration classes applied]]). You do **not** re-add `@EnableAutoConfiguration` when you add a dependency. `JdbcTemplate` is **not** created merely because `DataSource.class` exists as a library type — dumps that say “DataSource bean on the classpath” mix **class** and **bean**.

> [!warning] Listing a class is not creating its beans
> `.imports` only names **candidates**. A mismatch on `@ConditionalOnClass` or a user bean of the same type means **zero** beans from that class. `@ConditionalOnWebApplication`, `@ConditionalOnProperty`, and **`OnMissingBean`** can still skip even after you add the JAR. Two `DataSource` beans can fail **`@ConditionalOnSingleCandidate`**. `@ConditionalOnMissingBean` on **your** config does **not** see every other user bean — only definitions processed **so far**.

> [!warning] `OnClass` on a `@Bean` method can still load the type
> The return type is loaded with the method. Isolate class conditions on a nested `@Configuration`. Do **not** component-scan auto-config classes. Putting `@EnableAutoConfiguration` on a second class is the usual duplicate-opt-in. Excluding `DataSourceAutoConfiguration` does not remove Hikari from Maven — it stops **Boot from creating** the DataSource beans.

> [!tip] Interview answer
> Auto-configuration is a deferred import of classes listed in AutoConfiguration.imports. Each class is @Conditional: OnClass for the library, OnMissingBean so my @Bean wins because user configuration is processed first, OnProperty and OnWebApplication for environment. Boot 3 no longer loads those classes from spring.factories. I use the conditions report when the wrong bean appears.
