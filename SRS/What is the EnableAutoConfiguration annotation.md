<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS

# What is the EnableAutoConfiguration annotation?

> [!abstract] Short answer
> **`@EnableAutoConfiguration`** opts a `@Configuration` class into Boot’s auto-configuration: it **`@Import`s `AutoConfigurationImportSelector`** (a **`DeferredImportSelector`**) and **`@AutoConfigurationPackage`**. The selector loads candidate `@AutoConfiguration` classes from the classpath (`.imports` files), then **`@Conditional`** still decides which ones apply. You almost never write it: **`@SpringBootApplication`** is **`@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan`**. Add **one** of those two annotations, on the **primary** configuration class.

## Opt-in, then conditions

Auto-configuration guesses beans from **jar dependencies** and from beans you already defined. Example from the reference: **HSQLDB** on the classpath and **no** `DataSource` you configured → Boot auto-configures an in-memory database. Your own `DataSource` `@Bean` makes that support **back away** (`@ConditionalOnMissingBean`), not because the annotation “turns everything on” ([[How do ConditionalOn annotations drive auto-configuration]]).

```java
// Same as @SpringBootConfiguration @EnableAutoConfiguration @ComponentScan
@SpringBootApplication
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}
}
```

**Listing 1.** Usual form. `@SpringBootApplication` **aliases** `exclude` / `excludeName` onto `@EnableAutoConfiguration`.

```java
@SpringBootConfiguration(proxyBeanMethods = false)
@EnableAutoConfiguration
@Import({ SomeConfiguration.class, AnotherConfiguration.class })
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}
}
```

**Listing 2.** Official split: auto-config **without** component scan. `@Component` types and `@ConfigurationProperties` types are **not** detected; you `@Import` what you need. `@SpringBootConfiguration` is Boot’s `@Configuration` (helps test config detection).

Candidates are **not** component-scanned. The selector reads **`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`** ([[How does Spring Boot find auto-configuration classes]]). Then `exclude` / `excludeName` / `spring.autoconfigure.exclude` drop names ([[How do you disable a specific auto-configuration class]]).

```java
@Configuration(proxyBeanMethods = false)
@EnableAutoConfiguration(exclude = { DataSourceAutoConfiguration.class })
public class MyConfiguration {
}
```

**Listing 3.** Same `exclude` as on `@SpringBootApplication`. Use **`excludeName`** with the FQCN if the class may be absent. Boot 4: `org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration`.

```d2
direction: down
sba: "@SpringBootApplication" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
eac: "@EnableAutoConfiguration\n@Import selector" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
sel: "AutoConfigurationImportSelector\n.imports files" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}
cond: "@Conditional / @ConditionalOn*" {
  width: 260
  height: 50
  style.fill: "#f3e5f5"
}

sba -> eac -> sel -> cond
```

**Fig. 1.** The annotation **enables the mechanism**. Conditions **filter** which classes actually register beans. Confirm with `--debug` / the conditions report ([[How can you debug which auto-configuration classes applied]]).

> [!warning] Enable is not “every auto-config on the classpath ran”
> Listing a starter does not apply every class in that jar. `@ConditionalOnClass`, `@ConditionalOnMissingBean`, web vs non-web, and your exclusions still run. Putting **both** `@SpringBootApplication` and `@EnableAutoConfiguration` on the same app is the documented mistake: **one** annotation only.

> [!warning] Adding `@EnableAutoConfiguration` next to `@SpringBootApplication` does nothing extra
> The composed annotation **already** includes it. Use `@EnableAutoConfiguration` alone when you **do not** want `@ComponentScan` (Listing 2). Auto-config types themselves belong in `.imports`, not on a scanned package.

> [!tip] Interview answer
> @EnableAutoConfiguration is the opt-in that imports AutoConfigurationImportSelector so Boot can load auto-config classes from the classpath and then apply @Conditional. @SpringBootApplication already contains it plus configuration and component scan, so I rarely write EnableAutoConfiguration myself. It does not mean every auto-config class ran — conditions and exclude still decide.
