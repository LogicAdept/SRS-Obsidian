<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS

# What changed in Spring Boot 3?

> [!abstract] Short answer
> **Spring Boot 3.0** (from **2.7**) needs **Java 17+** and **Spring Framework 6.0**. APIs move **`javax.*` → `jakarta.*`** (Jakarta EE **10**: Servlet **6.0**, JPA **3.1**, …). Auto-config registration in **`spring.factories`** (`EnableAutoConfiguration` key) is **gone** — use **`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`**. First-class **GraalVM native** images. **Micrometer Observation** + **tracing** auto-config. Ship **Security 6**, **Hibernate 6.1**, Tomcat **10**. Upgrade **2.7 last patch first**.

## The 2.7 → 3.0 jump

Official path: latest **2.7.x**, optionally **Security 5.8** on that line, then Boot **3**. Deprecated 2.x APIs are **deleted**. `spring-boot-properties-migrator` (runtime, then **remove**) prints renamed keys ([[What is Spring Boot property source precedence]]).

```java
// Boot 2 / Java EE
import javax.servlet.http.HttpServletRequest;
import javax.persistence.Entity;
import javax.validation.Valid;

// Boot 3 / Jakarta EE 10
import jakarta.servlet.http.HttpServletRequest;
import jakarta.persistence.Entity;
import jakarta.validation.Valid;
```

**Listing 1.** Package rename is the breaking compile. Coordinates change too (`jakarta.servlet:jakarta.servlet-api`, not `javax.servlet`). Hibernate artifacts move to **`org.hibernate.orm`**. MySQL driver is **`com.mysql:mysql-connector-j`**.

```text
META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
com.example.AcmeAutoConfiguration
```

**Listing 2.** One FQCN per line. Boot **2.7** accepted this **and** `spring.factories`; **3.0 removed** the `EnableAutoConfiguration` factories key ([[How does Spring Boot find auto-configuration classes]], [[How do you create a custom Spring Boot starter]]). Other `spring.factories` keys stay.

Other 3.0-defining items from the **release notes** / **migration guide**:

- **Native / AOT** — GraalVM 22.3+ native images (portfolio-wide), not a side project.
- **Observability** — auto-config `ObservationRegistry`; Micrometer Tracing (Brave / OTel / Zipkin / Wavefront). Old MVC `*TagsProvider` instrumentation **removed**.
- **Actuator** — JMX expose default is **`health` only** (same as HTTP). `httptrace` → **`httpexchanges`**. `/env` and `/configprops` **mask all values** by default (`show-values`).
- **Web** — Framework **6** trailing-slash match default **`false`** (`/greeting/` → 404). `server.max-http-header-size` → **`server.max-http-request-header-size`**.
- **`@ConstructorBinding`** — not required on a type with **one** constructor; inject beans with **`@Autowired`**. Annotation **package** moved to `…properties.bind`.
- **Batch 5** — **`@EnableBatchProcessing` now turns Boot’s Batch auto-config off**. One job on startup, or set `spring.batch.job.name`.
- **Redis** properties `spring.redis.*` → **`spring.data.redis.*`**. Cassandra `spring.data.cassandra.*` → **`spring.cassandra.*`**.
- **CLI** — `spring run` / `jar` / `grab` **removed** ([[What are the components of a Spring Boot application]]).

Security 6 arrives **with** Boot 3: **`SecurityFilterChain`**, no **`WebSecurityConfigurerAdapter`** (already gone in Security **5.7**; 6 does not bring it back) ([[How do you use form login authentication in Spring Boot]], [[Why might PreAuthorize stop working after a Spring Boot 3 upgrade]]).

```d2
direction: down
b27: "Boot 2.7 + Java 8/11\njavax.*  spring.factories" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
b3: "Boot 3.0 + Java 17\njakarta.*  .imports\nFramework 6 + native" {
  width: 280
  height: 80
  style.fill: "#e8f5e9"
}

b27 -> b3
```

**Fig. 1.** Framework **6** also brings **`ProblemDetail`**. **`RestClient`** is Framework **6.1** / Boot **3.2**, not the 3.0 baseline. Virtual threads are **later** Boot 3.2 + Java 21, not 3.0.

> [!warning] Jetty on 3.0 was Servlet 5
> Migration guide: Jetty did **not** yet support Servlet **6.0**. Early Boot 3 needed `jakarta-servlet.version` **5.0** for Jetty. Do not assume Boot **4** Jetty/`starter-webmvc` facts when answering “what changed in 3.”

> [!warning] Not every `javax` package is Jakarta
> Some `javax.*` APIs stayed (for example parts of XML/activation historically mixed). The ones Boot **depends on** (Servlet, JPA, Bean Validation, Mail, …) are **`jakarta`**. Image **`banner.png`** is ignored; use **`banner.txt`**. Log timestamps default to **ISO-8601** with a `T` and offset.

> [!tip] Interview answer
> Boot 3 is Java 17, Jakarta packages, Spring Framework 6, and Hibernate 6. Auto-config no longer reads EnableAutoConfiguration from spring.factories. You get native images and Micrometer Observation. I upgrade to 2.7 first, then fix javax imports and SecurityFilterChain.
