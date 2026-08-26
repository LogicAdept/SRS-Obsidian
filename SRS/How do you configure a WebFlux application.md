<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Annotations #SRS

# How do you configure a WebFlux application?

> [!abstract] Short answer
> In **Spring Boot**, add **`spring-boot-starter-webflux`** and **`@SpringBootApplication`** — auto-config is enough. Extra WebFlux knobs go on a **`WebFluxConfigurer`** **without** **`@EnableWebFlux`**. Use **`server.port`** (and `server.netty.*`) for the embedded server; **`WebServerFactoryCustomizer<NettyReactiveWebServerFactory>`** for Netty-only options. **`@EnableWebFlux`** means you take **complete control** and drop Boot’s WebFlux customizations.

## Boot auto-config vs `@EnableWebFlux`

Spring Boot *Reactive Web Applications*: auto-configuration adds codecs and static resources on top of Spring defaults. To **keep** those features, implement **`WebFluxConfigurer`** and **do not** add `@EnableWebFlux`. To take **complete control**, annotate your own `@Configuration` with **`@EnableWebFlux`**.

Spring Framework *WebFlux Config*: `@EnableWebFlux` registers infrastructure beans (`DelegatingWebFluxConfiguration`). Same Boot warning: `WebFluxConfigurer` without `@EnableWebFlux` preserves Boot customizations.

```java
@SpringBootApplication
public class FluxApp {
    public static void main(String[] args) {
        SpringApplication.run(FluxApp.class, args);
    }
}

@Configuration
public class WebConfig implements WebFluxConfigurer {
    @Override
    public void addFormatters(FormatterRegistry registry) {
        // conversions / formatters — Boot still owns codecs/static unless you @EnableWebFlux
    }
}
```

**Listing 1.** Conceptual Boot app + extra `WebFluxConfigurer`. Full-control annotation: [[What is the EnableWebFlux annotation]].

## Server (Netty by default)

Boot’s WebFlux starter **defaults to Reactor Netty**, port **8080**. Common settings: **`server.port`**, **`server.address`**, error path, plus **`server.netty.*`**. Programmatic: `WebServerFactoryCustomizer<ConfigurableReactiveWebServerFactory>` (for example `setPort`). Netty-specific: `WebServerFactoryCustomizer<NettyReactiveWebServerFactory>` and **`addServerCustomizers`**.

```java
@Component
public class MyNettyWebServerFactoryCustomizer
        implements WebServerFactoryCustomizer<NettyReactiveWebServerFactory> {

    @Override
    public void customize(NettyReactiveWebServerFactory factory) {
        factory.addServerCustomizers(server -> server.idleTimeout(Duration.ofSeconds(20)));
    }
}
```

**Listing 2.** Official Boot pattern for Reactor Netty options (idle timeout). The same `addServerCustomizers` hook is where Netty `ChannelOption`s (for example listen backlog) would go.

```d2
direction: down
boot: "starter-webflux\n@SpringBootApplication" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
cfg: "WebFluxConfigurer\nNO @EnableWebFlux" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
take: "@EnableWebFlux\nreplace Boot WebFlux config" {
  width: 280
  height: 70
  style.fill: "#ffebee"
}

boot -> cfg: "keep auto-config"
boot -> take: "full control"
```

**Fig. 1.** Mixing `@EnableWebFlux` with Boot auto-config is the usual interview trap. Dual MVC+WebFlux classpath: [[Can you use Spring MVC and WebFlux in the same application]].

> [!warning] `@EnableWebFlux` drops Boot WebFlux auto-config
> Codecs, static resources, and other Boot extras are no longer applied the same way. Prefer `WebFluxConfigurer` alone.

> [!warning] `server.port` still applies to Netty
> It is not a Tomcat-only property. Use `server.netty.*` or a `NettyReactiveWebServerFactory` customizer for Netty-only knobs.

> [!warning] Do not map Servlet filters in a WebFlux app
> Mixing blocking Servlet API with non-blocking I/O causes runtime issues — Spring WebFlux *Servers*.

> [!tip] Interview answer
> **Boot: `spring-boot-starter-webflux` + `@SpringBootApplication`.** Customize with `WebFluxConfigurer` **without** `@EnableWebFlux`. Port via `server.port`. Netty extras via `NettyReactiveWebServerFactory` customizers. `@EnableWebFlux` is take-over, not “enable Boot WebFlux.”
