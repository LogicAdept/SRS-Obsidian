<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS

# What is Spring Boot?

> [!abstract] Short answer
> Spring Boot is an **opinionated library on Spring**: stand-alone, **production-grade** apps you **`java -jar`** (or still WAR). It is **still Spring** (IoC, MVC, TX). Boot adds **starters**, **auto-configuration**, an **embedded** Tomcat/Jetty/Undertow, and **production** knobs (externalized config, metrics, health). Official goals: **fast start**, **defaults that back off**, **no XML** and **no code generation** (except native image). Typical jobs: an **HTTP API or MVC app**, a **non-web** `main`, and **ops** via Actuator. The value is **less boilerplate wiring**, not a second Framework.

## What Boot adds on top of Spring

Project page **Features** and docs goals are the same list: **stand-alone** `SpringApplication.run` / nested executable JAR; **embedded** server (WAR optional); **opinionated starters**; **auto-configuration** of Spring and third-party libs; **production-ready** metrics, health, and **externalized configuration**; **no XML required**. Auto-configuration is **opt-in** (`@SpringBootApplication` / `@EnableAutoConfiguration`) and **non-invasive**: your `DataSource` `@Bean` makes embedded-DB support **back away** ([[How does Spring Boot auto-configuration decide which beans to create]]). You still write `@RestController`, `@Entity`, `SecurityFilterChain`.

```java
package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@SpringBootApplication
public class MyApplication {

	@RequestMapping("/")
	String home() {
		return "Hello World!";
	}

	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}
}
```

**Listing 1.** Official first app (Boot **4.1**: `spring-boot-starter-webmvc`, not the older `starter-web` name). `@RestController` / `@RequestMapping` are **Spring MVC**. `@SpringBootApplication` is **`@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan`** ([[What is @SpringBootApplication]]). `SpringApplication.run` starts the **IoC container**, which starts **auto-configured Tomcat** ([[What is the SpringApplication class]]). Package as a **nested executable JAR** with the Boot plugin ([[What is an executable JAR in Spring Boot]]).

Starters are **dependency descriptors** with managed versions (`spring-boot-starter-*`), not the auto-config classes themselves. You can add jars **without** a starter; Boot still guesses. Parent POM / Gradle plugin supplies **dependency management** ([[Which common Spring Boot starters do you know]], [[What is spring-boot-starter-parent]], [[Why can you omit library versions in a Spring Boot project]]). Embedded Tomcat/Jetty/Undertow is **optional** (`WebApplicationType.NONE`). Actuator is **optional**. Debug which auto-config ran with **`--debug`**.

```d2
direction: down
fw: "Spring Framework\nIoC, MVC, AOP, TX" {
  width: 280
  height: 60
  style.fill: "#e3f2fd"
}
boot: "Spring Boot\nstarters + auto-config\nembedded server + Actuator" {
  width: 300
  height: 80
  style.fill: "#fff3e0"
}
run: "java -jar  (or WAR)" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}

fw -> boot -> run
```

**Fig. 1.** Boot does not replace Framework ([[What is the difference between Spring Boot and the core Spring Framework]]). Production extras: **metrics**, **health**, **externalized config** ([[What is the role of Actuator in Spring Boot]], [[What is Spring Boot property source precedence]]). Defaults are opinionated; you **override** when they stop fitting. A dump “four major components” list is not official ([[What are the components of a Spring Boot application]]).

> [!warning] Boot is not “DataSource on the classpath means JPA”
> Official example: **HSQLDB** on the classpath and **no** database beans → in-memory `DataSource`. JPA auto-config needs the **JPA stack** (typically `spring-boot-starter-data-jpa`). A starter is an **opinionated classpath**; auto-configuration reads **`.imports`** and conditions. Enable **opts in**; `@ConditionalOn*` still decides ([[How does Spring Boot find auto-configuration classes]]).

> [!warning] Value is not “zero configuration” and not “not Spring”
> Docs: **most** Boot apps need **very little** Spring config — not none. Native AOT **is** codegen; do not quote “absolutely no code generation” without that exception. When something breaks, you still need **Spring Framework** knowledge (bean lifecycle, AOP proxies, Security filter order).

> [!warning] Not “the microservice framework”; the CLI is not the app
> Docs never define Boot as “for microservices only.” A monolith JAR is a first-class use. The **`spring` CLI** (`init` / `encodepassword` / `shell`) bootstraps or helps; it does **not** run the production process. `run` / `jar` / `grab` were **removed in Boot 3**. XML is **not forbidden**; it is **not required**. There is no type named “AutoConfigurator.”

> [!tip] Interview answer
> Spring Boot is still Spring. I add starters, put @SpringBootApplication on main, and SpringApplication.run gives me an executable app with an embedded server and auto-config that backs off when I define my own beans. Actuator and external config are the production extras. I use it for web APIs, workers, and health endpoints. It is a library, not a replacement for the Framework and not only for microservices.
