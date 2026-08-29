<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #Java/Spring/Boot #SRS

# What is the difference between Spring Boot and the core Spring Framework?

> [!abstract] Short answer
> **Spring Framework** is the **IoC/DI platform** (`ApplicationContext`, beans, AOP, MVC, …). **Spring Boot** is **another library on that platform**: opinionated **starters**, **auto-configuration**, an **embedded** server, Actuator, and `java -jar` / WAR packaging so you write **little** Spring config. Boot does **not** replace the container. You can run Framework **without** Boot; a Boot app **always** is a Spring app.

## Same beans, different bootstrap

Framework docs: the container **instantiates, configures, and assembles** beans from metadata — `@Configuration` / `@Component` **or** XML ([[How does a Spring IoC container differ from a web container or EJB container]]). You choose the context type and what sits on the classpath.

Boot docs: **stand-alone, production-grade Spring** you **just run**; opinionated about the platform and third-party libraries; **get out of the way** when you diverge; **no XML required** (native image is the codegen exception). Official using guide: there is **nothing particularly special** about Boot — it is **just another library**. `SpringApplication` still builds an `ApplicationContext` ([[What is Spring Boot]], [[What is the SpringApplication class]]).

```java
ApplicationContext ctx = new AnnotationConfigApplicationContext(AppConfig.class);
```

**Listing 1.** Core Framework: you **construct** the context. XML (`ClassPathXmlApplicationContext`) is **optional**, not mandatory.

```java
@SpringBootApplication
public class MyApplication {
	public static void main(String[] args) {
		SpringApplication.run(MyApplication.class, args);
	}
}
```

**Listing 2.** Boot: `@SpringBootApplication` = `@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan`. Starters pull jars; auto-config **registers beans if conditions match** and **backs off** on `@ConditionalOnMissingBean` ([[How does Spring Boot auto-configuration decide which beans to create]], [[What is @SpringBootApplication]]).

```d2
direction: down
fw: "Spring Framework\nApplicationContext / beans" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
boot: "Spring Boot\nstarters + auto-config + JAR" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
app: "@Service / @RestController\nstill Framework types" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}

fw -> boot
boot -> app
```

**Fig. 1.** Dump “Hibernate SessionFactory vs `@SpringBootConfiguration`” is not the split. ORM setup is **Spring Data / Boot JDBC auto-config**, not “Spring vs Boot.” Dump “Boot cannot skip defaults” is false: **`exclude`**, your own `@Bean`, `spring.autoconfigure.exclude`.

> [!warning] Boot is not a second IoC container
> `@Autowired`, bean scopes, and MVC annotations are **Framework**. Boot **starts** the context and **pre-wires** common infrastructure. Saying “Spring needs XML, Boot uses annotations” is outdated: Framework has been annotation/`@Configuration`-capable for years.

> [!warning] “Undefined future features” is not a criterion
> Official use of Boot is **faster start + production features** (embedded server, metrics, health, externalized config), not “we don’t know the app type.” A well-specified MVC service is a **typical** Boot app.

> [!tip] Interview answer
> Spring Framework is the IoC container and the modules I program against. Spring Boot is a library on top that auto-configures those modules from starters and runs an embedded server as a fat JAR. I can use Framework without Boot. I cannot use Boot without Framework. Auto-config backs off when I define my own beans.
