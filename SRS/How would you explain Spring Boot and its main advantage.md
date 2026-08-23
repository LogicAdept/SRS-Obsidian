<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS

# How would you explain Spring Boot and its main advantage?

> [!abstract] Short answer
> **Spring Boot** is an opinionated layer on Spring that gets you to a **runnable app fast**: **starters** (curated dependencies), **auto-configuration** (beans from the classpath), and an **embedded server** so you ship an executable JAR. The main advantage is **less boilerplate wiring** — Boot guesses sensible defaults, then **gets out of the way** when you override them.

## What Boot adds on top of Spring Framework

| Piece | What you get |
|---|---|
| **Starters** | One dependency (e.g. `spring-boot-starter-data-jpa`) pulls a **supported, consistent** set of libraries — [[Which common Spring Boot starters do you know]] |
| **Auto-configuration** | `@SpringBootApplication` / `@EnableAutoConfiguration` configures beans from jars on the classpath (e.g. in-memory DB if HSQLDB is present) |
| **Embedded server** | Tomcat (default), Jetty, or Undertow inside the process — [[Which embedded containers are supported by Spring Boot]] |
| **Production extras** | Externalized config, Actuator, metrics/health — without hand-rolling XML |

Official goals (paraphrased from Boot’s intro): faster getting-started experience; **opinionated defaults** that you can replace; common non-functional features; **no code generation** and **no required XML**.

## Main advantage in one line

**Starters + auto-config + embedded server → runnable JAR with far less manual Spring wiring.**

```java
@SpringBootApplication
public class BillingApplication {
    public static void main(String[] args) {
        SpringApplication.run(BillingApplication.class, args);
    }
}
```

**Listing 1.** One annotation enables component scan and auto-configuration; `main` starts the embedded container.

Auto-configuration is **non-invasive**: define your own `DataSource` and the embedded-DB auto-config **backs away**. Debug with `--debug` to see which auto-config classes applied.

```d2
direction: right
starter: "Starter on\nclasspath" {
  width: 130
  height: 50
  style.fill: "#e3f2fd"
}
auto: "Auto-configuration" {
  width: 150
  height: 50
  style.fill: "#fff3e0"
}
ctx: "ApplicationContext\n+ embedded server" {
  width: 170
  height: 55
  style.fill: "#e8f5e9"
}
jar: "Executable JAR" {
  width: 130
  height: 45
  style.fill: "#fce4ec"
}

starter -> auto -> ctx -> jar
```

**Fig. 1.** Classpath steers defaults; you override only what must differ.

> [!warning] Defaults hide complexity — they do not remove it
> When something breaks, you still need **Spring Framework** knowledge (bean lifecycle, AOP proxies, Security filter order). Boot reduces **setup**, not the need to understand what it configured — [[Why can you omit library versions in a Spring Boot project]].

> [!tip] Interview answer
> Spring Boot is opinionated Spring: starters, auto-configuration, and an embedded server so you run a JAR quickly. Main advantage — dramatically less boilerplate config while remaining overridable when defaults no longer fit.
