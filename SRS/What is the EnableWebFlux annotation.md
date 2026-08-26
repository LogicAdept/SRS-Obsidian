<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Annotations #SRS

# What is the `EnableWebFlux` annotation?

> [!abstract] Short answer
> **`@EnableWebFlux`** (since **5.0**) imports Framework **WebFlux Java config** (`DelegatingWebFluxConfiguration` / `WebFluxConfigurationSupport`): annotated controllers, functional endpoints, codecs, `DispatcherHandler`. In a **plain** Spring app that is how you **turn WebFlux on**. In **Spring Boot**, the **starter already does that** — adding `@EnableWebFlux` means you take **complete control** and **drop Boot’s WebFlux customizations**. Extra knobs: **`WebFluxConfigurer` without `@EnableWebFlux`**.

## What it imports

Javadoc: put it on **one** `@Configuration`. It enables annotated controllers and functional endpoints. **Several** other configs may implement **`WebFluxConfigurer`**. If the configurer API is not enough, **remove** `@EnableWebFlux` and **extend** `WebFluxConfigurationSupport` or **`DelegatingWebFluxConfiguration`** (still detects other `WebFluxConfigurer` beans).

```java
@Configuration
@EnableWebFlux
@ComponentScan
public class MyConfiguration implements WebFluxConfigurer {

    @Override
    public void configureHttpMessageCodecs(ServerCodecConfigurer configurer) {
        configurer.defaultCodecs().jackson2JsonEncoder(new Jackson2JsonEncoder(objectMapper));
        configurer.defaultCodecs().jackson2JsonDecoder(new Jackson2JsonDecoder(objectMapper));
    }
}
```

**Listing 1.** Conceptual Framework javadoc sample — **without Boot**. Boot how-to: [[How do you configure a WebFlux application]].

Spring *WebFlux Config*: `@EnableWebFlux` registers infrastructure beans and adapts to JSON/XML on the classpath. **Boot note in the same chapter:** use `WebFluxConfigurer` **without** `@EnableWebFlux` to **keep Boot WebFlux customizations**.

Boot *Reactive Web Applications*:

- Keep Boot features → `WebFluxConfigurer`, **no** `@EnableWebFlux`.
- **Complete control** → `@Configuration` **with** `@EnableWebFlux`.

```d2
direction: down
plain: "No Boot\n@EnableWebFlux" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
boot: "starter-webflux\nNO @EnableWebFlux" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
cfg: "WebFluxConfigurer\n(optional extras)" {
  width: 240
  height: 60
  style.fill: "#fff3e0"
}
take: "@EnableWebFlux on Boot\nreplaces auto-config" {
  width: 280
  height: 70
  style.fill: "#fce4ec"
}

plain -> cfg
boot -> cfg
boot -> take: "full control"
```

**Fig. 1.** `@EnableWebMvc` has the same Boot trap on the servlet stack. Front controller: [[What is DispatcherHandler in WebFlux]]. MVC+WebFlux classpath: [[Can you use Spring MVC and WebFlux in the same application]].

This annotation does **not** start Netty. Framework does not start servers; Boot’s WebFlux starter does.

> [!warning] Boot: starter is enough
> `@SpringBootApplication` + `spring-boot-starter-webflux` already configures WebFlux. `@EnableWebFlux` is **not** “turn it on”; it is **take over**.

> [!warning] Only one `@EnableWebFlux`
> Javadoc: **one** `@Configuration` may have it. Many `WebFluxConfigurer` classes are fine.

> [!warning] `WebFluxConfigurer` does not require the annotation
> On Boot, **omit** `@EnableWebFlux` so codecs, static resources, and other Boot extras stay. Implementing `WebFluxConfigurer` **and** `@EnableWebFlux` is the **Framework** sample, not the Boot default.

> [!tip] Interview answer
> **`@EnableWebFlux` imports Framework WebFlux Java config (`DelegatingWebFluxConfiguration`).** Without Boot, that is how you enable the stack. **With Boot, do not add it** unless you want to own every WebFlux bean — customize with `WebFluxConfigurer` alone.
