<!--
reps: 0
priority: 0
-->
#Java/Spring/Core #SRS

# What are the main differences between Spring Framework major versions?

> [!abstract] Short answer
> Interview majors are **generations**, not Java SE history. **3.x** brought **Java `@Configuration` / `@Bean`** into the core container. **4.x** made **Java 8** and **Java EE 6+** first-class (WebSocket, `@Conditional`, Groovy). **5.x** required **JDK 8**, added **WebFlux** / **`WebClient`**, JDK 9 module names, and dropped Portlet/Velocity/`globalSession`. **6.x** requires **Java 17+** and **`jakarta.*` (Jakarta EE 9–10)** plus **AOT / GraalVM native**. **7.x** keeps **JDK 17** (recommend **21/25 LTS**), raises **Jakarta EE 11** (Servlet **6.1**), drops leftover **`javax.annotation` / `javax.inject`**, and steers HTTP clients to **`RestClient`**. Current production line is **7.0.x**.

## Do not confuse Spring with Java language versions

Dump text that lists Java 1.0–14 **is the wrong product**. Spring **integrates** a Java/Jakarta **baseline**; it is not the JDK release train ([[What is the Spring Framework]]).

| Generation | Java / EE baseline | Signature change |
| --- | --- | --- |
| **3.x** | Java 5-era language (annotations, generics) | JavaConfig in **core**: `@Configuration`, `@Bean`, `@Import`, `@DependsOn` |
| **4.x** | Java 8 usable; **Java EE 6+** (4.x docs: Servlet 3 / JPA 2) | WebSocket, `@Conditional`, Groovy; still **`javax.*`** |
| **5.x** | **JDK 8 required** (codebase on Java 8); EE **7** APIs, EE **8** at runtime | **`spring-webflux`**, reactive `WebClient`; `AsyncRestTemplate` deprecated; Portlet / Velocity / JDO / `globalSession` gone ([[What is Spring WebFlux]], [[What is global-session bean scope in Spring]]) |
| **6.x** | **Java 17+**, **Jakarta EE 9–10**, `jakarta.*` | AOT + native images; HTTP interfaces; **`RestClient`** (6.1); trailing-slash match **off**; remoting/EJB helpers removed |
| **7.x** | **JDK 17–25+** (LTS: 17, 21, 25); **Jakarta EE 11–12** | Servlet **6.1** / JPA **3.2** / BV **3.1**; **`javax.annotation` / `javax.inject` unsupported**; `RestTemplate` deprecated toward **`RestClient`**; JSpecify null-safety; API versioning |

```d2
SF5: "5.x  javax.*  JDK 8  WebFlux"
SF6: "6.x  jakarta.*  JDK 17  AOT"
SF7: "7.x  EE 11  Servlet 6.1  RestClient"
SF5 -> SF6: "namespace + Java 17"
SF6 -> SF7: "EE 11, drop javax.inject leftovers"
```

**Fig. 1.** The upgrade that breaks compiles is **5 → 6** (`javax` → `jakarta`). **6 → 7** is a **spec floor** (Servlet 6.1, Tomcat 11 / Jetty 12.1), not another namespace rename.

```java
import jakarta.servlet.http.HttpServletRequest; // 6.x / 7.x
import jakarta.inject.Inject;
import jakarta.annotation.PostConstruct;
```

**Listing 1.** After 6.0, Servlet/JPA/BV live in `jakarta.*`. 6.x still **detected** `javax.inject` / `javax.annotation` on old binaries; **7.0 removes** that compatibility.

## What each jump is *for*

**5.0 (2017 line):** reactive stack beside MVC; Kotlin; JUnit 5 `SpringExtension`; `spring-jcl` logging bridge. OSS **5.3.x** ended **August 2024**.

**6.0:** Java 17 source; GraalVM native / `refreshForAotProcessing`; Tomcat 10+; Hibernate **jakarta** artifacts; HTTP `@HttpExchange` clients. **6.2** was the last 6.x feature branch (OSS through **June 2026**).

**7.0 (production from November 2025):** EE 11 servers; **Undertow** adapters dropped until Servlet 6.1 exists there; `spring-jcl` module removed (Commons Logging 1.3); Jackson **3**; JUnit **6**; `ListenableFuture` gone. `RestClient` / `WebClient` / HTTP interfaces are the HTTP story ([[What is the difference between RestTemplate WebClient and RestClient]]).

Older but still asked: **`@Required`** died on the 5.1 → 6 path; XML **autodetect** autowire is not a 7.x feature.

> [!warning] “Spring 4 = Java 8 in 2016” is a mash-up
> **Spring Framework 4.0** is not “the Java 8 JDK.” 4.x *used* Java 8 features; **5.0 required JDK 8**. Dates on dump slides (3 = 2009, 5 = 2017) are roughly the **.0** years; **4.3 EOL was 31 Dec 2020**, not a feature list.

> [!tip] Interview answer
> 3: Java `@Configuration`. 4: Java 8 / EE 6+ on `javax`. 5: JDK 8 + WebFlux. 6: Java 17 + `jakarta.*` + AOT. 7: EE 11, no `javax.inject`, `RestClient` over `RestTemplate`. Recite **baselines**, not the Java SE changelog.
