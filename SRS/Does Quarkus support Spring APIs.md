<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS

# Does Quarkus support Spring APIs?

> [!abstract] Short answer
> Partially, through dedicated **compatibility extensions**: `quarkus-spring-di` maps Spring's annotations (`@Component`/`@Service`, `@Autowired`, `@Configuration`+`@Bean`, `@Value`), `quarkus-spring-web` maps Spring MVC annotations on controllers, and further guides cover `spring-data-jpa`, `spring-security`, `spring-cache`, `spring-tx`, `spring-scheduled`, `spring-boot-properties`. They are **build-time translators**, not the Spring runtime: annotations are read during augmentation and rewritten onto Quarkus/CDI equivalents — there is no ApplicationContext, no runtime component scanning, and Spring Boot test features are not supported.

## What is actually mapped, and how

With `quarkus-spring-di` on the classpath, a class annotated `@Service` becomes a CDI bean with `@ApplicationScoped` semantics, constructor injection works without `@Autowired` when there is a single constructor, and `@Value("${key}")` bridges onto MicroProfile Config (default values in the `key:default` syntax supported). `@Configuration` classes with `@Bean` producer methods become CDI producers. Everything resolves at build time on the Jandex index — `@ComponentScan` is explicitly unnecessary (annotated discovery over one bean archive), and the container is recorded bytecode ([[What is Jandex in Quarkus]]). `quarkus-spring-web` lets a controller use `@RestController`/`@GetMapping` while executing on the Quarkus REST stack; `spring-data-jpa` supports repositories derived from Spring Data interfaces backed by Hibernate ORM with Panache machinery.

```java
// Spring-annotated bean on Quarkus (quarkus-spring-di) - JDK 21, Quarkus 3.39.2,
// compiled and exercised in the same test run as the CDI beans (mvn test: 6/6 green).
package org.acme.check.infra;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service                                    // -> becomes an @ApplicationScoped CDI bean
public class SpringStyleService {
    @Autowired                              // field injection, resolved at build time
    CachedPriceService prices;

    public int read(String sku) {
        return prices.price(sku);
    }
}
// Injected and called from the same test context as pure-CDI beans; no Spring context
// exists at runtime - the bean instance lives in the ArC container, proxied like any other.
```

**Listing 1.** A Spring-annotated service participating in Quarkus' container. The dependency added to the pom was `io.quarkus:quarkus-spring-di` — a Quarkus extension, not Spring Framework jars.

```d2
direction: left
src: "Source with Spring\nannotations" {
  width: 230
  height: 65
}
aug: "Augmentation (quarkus-spring-di)\nreads @Service/@Autowired/@Value,\nmaps to CDI + MicroProfile Config" {
  width: 340
  height: 80
  style.fill: "#fff3e0"
}
arc: "ArC container\nrecorded bootstrap" {
  width: 240
  height: 65
  style.fill: "#e8f5e9"
}
spring: "Spring Framework runtime\nApplicationContext, scanning, AOP\nNOT PRESENT" {
  width: 300
  height: 75
  style.fill: "#f5f5f5"
}
src -> aug -> arc
aug -x spring: "no dependency"
```

**Fig. 1.** The compatibility layer is a build-time annotation translator; the Spring runtime never ships — which is precisely why the result stays native-image friendly ([[What is a Quarkus extension]]).

## Why the layer exists — and its honest limits

It lowers migration friction: teams can move an application to Quarkus while keeping familiar annotations, then port incrementally. The limits are real: only the documented annotation subset works, Spring-specific features (profiles via `spring.profiles`, `@Conditional*`, AOP aspects, Spring Security filters, Boot's actuator, Spring Boot test slices) do not exist, and mixing subtle Spring semantics with CDI semantics can confuse — CDI scope rules still apply to the resulting beans ([[What bean scopes does Quarkus support]]). The safe interview position: "compatibility extensions translate a stable annotation subset to CDI at build time; they are a migration bridge, not a Spring runtime."

> [!warning] "Quarkus runs Spring" — no, it translates a subset
> The misleading claim is that Quarkus embeds Spring. What actually happens: Quarkus' own extensions parse a fixed set of Spring annotations during augmentation and generate the equivalent CDI/config wiring. Anything outside that set silently does nothing or fails the build. Spring Boot tests (`@SpringBootTest`) have no equivalent here — testing is Quarkus' own `@QuarkusTest` machinery. In an interview, name the bridge and its boundary in the same sentence.

> [!tip] Interview answer
> Yes — selectively, via compatibility extensions: spring-di maps @Service, @Autowired, @Configuration/@Bean and @Value onto CDI and MicroProfile Config; spring-web, spring-data-jpa, spring-security and a few others exist the same way. Crucially they work at build time — annotations are translated to CDI beans on the ArC container, and no Spring runtime, context or scanning ships in the artifact. So it is a migration bridge that also keeps the app native-image friendly, not an embedded Spring.
