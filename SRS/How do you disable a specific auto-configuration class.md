<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot/AutoConfiguration #Java/Annotations #SRS

# How do you disable a specific auto-configuration class?

> [!abstract] Short answer
> Pass the class to **`@SpringBootApplication(exclude = …)`** (or **`excludeName`** with the FQCN if the type is not on the classpath). The same attributes exist on **`@EnableAutoConfiguration`**. You can also set **`spring.autoconfigure.exclude`**. Annotation and property exclusions **stack**. The only **public API** of an auto-config class is its **name** for this purpose.

## Three equivalent knobs

Boot applies auto-configuration from the classpath (starters). If a class you do not want still matches, **exclude** it — classic case: a JDBC starter arrived **transitively** and you do not want Boot’s `DataSource`.

```java
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = { DataSourceAutoConfiguration.class })
public class MyApplication {
}
```

**Listing 1.** `exclude` takes the class literals. Use **`excludeName = "org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration"`** when that class may be absent so the annotation still compiles.

```properties
spring.autoconfigure.exclude=org.springframework.boot.jdbc.autoconfigure.DataSourceAutoConfiguration
```

**Listing 2.** Property form (comma-separated list). You may combine this with the annotation.

If you prefer `@EnableAutoConfiguration` instead of `@SpringBootApplication`, **`exclude`** / **`excludeName`** are on that annotation too. Confirm what actually applied with the conditions report ([[How can you debug which auto-configuration classes applied]]).

```d2
direction: right
want: "Do not want this\nauto-config class" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
knob: "exclude / excludeName\nspring.autoconfigure.exclude" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
skip: "Class not applied\njars still on classpath" {
  width: 220
  height: 70
  style.fill: "#ffebee"
}

want -> knob -> skip
```

**Fig. 1.** Exclusion skips **registration** of that `@AutoConfiguration`. It does not uninstall the starter ([[Which common Spring Boot starters do you know]]).

> [!warning] Exclude does not remove the jars
> `exclude` only stops that auto-configuration class. **Tomcat, JDBC drivers, Hikari** and the rest of the starter stay on the classpath and can still affect **other** conditions ([[How do ConditionalOn annotations drive auto-configuration]]). To drop a stack, remove or replace the **starter**. Also: if you already define a `DataSource` `@Bean`, Boot’s default **backs off** via `@ConditionalOnMissingBean` — you often **do not** need `exclude` for that.

> [!warning] Do not call auto-config internals
> Auto-configuration types are `public`, but **only the class name** is supported API (for exclude). Nested configuration classes and `@Bean` methods are **internal**. Prefer `excludeName` when a direct class reference would fail compilation on a slim classpath.

> [!tip] Interview answer
> I disable one auto-config with @SpringBootApplication(exclude = DataSourceAutoConfiguration.class), or excludeName if the class is not on the classpath, or spring.autoconfigure.exclude. That is how you stop Boot creating a DataSource when JDBC arrived transitively. Exclusion does not remove the starter jars, and if I already provide the bean, OnMissingBean usually backs off without an exclude.
