<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS

# What are the components of a Spring Boot application?

> [!abstract] Short answer
> Official docs **do not** list “four major components.” A Boot **application** is a **Spring app**: **`@SpringBootApplication` + `main`**, **starters** on the classpath, **auto-configuration**, **`Environment`** (`application.properties` / YAML), an **`ApplicationContext`**, and (if web) an **embedded** Tomcat/Jetty/Undertow. **Actuator** is optional production endpoints. **CLI** is a **separate** `spring` tool (`init`, `encodepassword`, `shell`) — **not** part of the running app.

## What you actually ship

Typical layout: `MyApplication` in the **root** package, domain packages underneath, `SpringApplication.run` as the entry ([[What is @SpringBootApplication]], [[What is Spring Boot]]). Build: parent/BOM + **`spring-boot-starter-*`** ([[Which common Spring Boot starters do you know]]). Config: externalized properties ([[What is Spring Boot property source precedence]]). Package: **executable JAR** (or WAR) ([[What is an executable JAR in Spring Boot]]).

```java
package com.example.myapplication;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class MyApplication {

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}
}
```

**Listing 1.** The documented application class. `@SpringBootApplication` = `@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan`. There is **no** type named “AutoConfigurator.”

`SpringApplication.run` (javadoc): **(1)** create an `ApplicationContext` from the classpath (servlet / reactive / none), **(2)** register `CommandLinePropertySource`, **(3)** **refresh** (load singletons), **(4)** run `CommandLineRunner` / `ApplicationRunner` beans. Environment is ready before the context; **`ApplicationReadyEvent`** fires after runners. A web classpath starts the **embedded** server as part of refresh ([[What is the SpringApplication class]], [[How do you create a non-web Spring Boot application]]).

Dump “starters / AutoConfigurator / CLI / Actuator” maps like this:

| Dump name | Official |
| --- | --- |
| Starters | Dependency descriptors (`spring-boot-starter-*`), **not** the running process |
| AutoConfigurator | **Auto-configuration** (`.imports` + `@Conditional`), opt-in, backs off |
| CLI | **`spring` CLI**: Initializr **`init`**, **`encodepassword`**, **`shell`**. **`run` / `jar` / `grab` were removed in Boot 3** |
| Actuator | Optional **production** health/metrics/loggers ([[How do you monitor an application with Spring Boot Actuator]]) |

```d2
direction: down
app: "MyApplication + starters\nproperties + your @Components" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
rt: "SpringApplication\nEnvironment → Context refresh\n(+ embedded server if web)" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
opt: "optional Actuator\nCLI is not in the JAR" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

app -> rt
rt -> opt
```

**Fig. 1.** CLI does **not** “internally use starters to execute the application.” You run `main`, `mvn spring-boot:run` / `gradle bootRun`, or `java -jar`.

> [!warning] CLI is not a fourth runtime piece
> Boot 4 CLI commands are **`init`**, **`encodepassword`**, and **`shell`**. It does not start your context. Putting CLI in the same list as starters and Actuator is a tutorial mnemonic, not the architecture of an application.

> [!warning] Actuator is optional; XML is not required
> A Boot app can be a **non-web** `CommandLineRunner` with no Actuator. Auto-configuration **replaces** typical XML; it does **not** delete `@Bean` / `@Configuration` you write. `BeanFactory` **is** inside `ApplicationContext`, not a sibling container.

> [!tip] Interview answer
> I do not recite four product names. A Boot application is SpringApplication, an Environment, an ApplicationContext from @SpringBootApplication, starters plus auto-config, and an embedded server if it is web. Actuator is production extras. The CLI is a developer tool and no longer has spring run.
