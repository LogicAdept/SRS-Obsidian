<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #Java/Spring/Boot #SRS

# What is the `EnableWebMvc` annotation?

> [!abstract] Short answer
> **`@EnableWebMvc` imports Spring MVC’s Java configuration** (`DelegatingWebMvcConfiguration` / `WebMvcConfigurationSupport`): `RequestMappingHandlerMapping`, `RequestMappingHandlerAdapter`, default exception resolvers, message converters, and the rest of the MVC infrastructure. It is the Java equivalent of XML **`<mvc:annotation-driven/>`**. **Exactly one** `@Configuration` class may have it. Customize via **`WebMvcConfigurer`** beans. In **Spring Boot do not use it** unless you want to **replace** Boot’s MVC auto-configuration.

## Import MVC infrastructure

`EnableWebMvc` javadoc (since 3.1): add it to an `@Configuration` class to import `WebMvcConfigurationSupport`. The type actually imported is **`DelegatingWebMvcConfiguration`**, which autowires **all** `WebMvcConfigurer` beans. Multiple configurer classes are allowed; a **second** `@EnableWebMvc` is not.

It does **not** register `DispatcherServlet` and does **not** scan `@Controller`s by itself. Pair with `@ComponentScan` (or explicit `@Bean`s) and a servlet registration (`WebApplicationInitializer` or Boot).

```java
@Configuration
@EnableWebMvc
@ComponentScan(basePackageClasses = MyConfiguration.class)
public class MyConfiguration implements WebMvcConfigurer {

    @Override
    public void addFormatters(FormatterRegistry registry) {
        registry.addConverter(new MyConverter());
    }
}
```

**Listing 1.** Conceptual Framework 7 example (WAR / non-Boot). Callbacks: [[What is WebMvcConfigurer in Spring MVC]]. Servlet: [[What is Spring MVC DispatcherServlet]], [[What is WebApplicationInitializer in Spring MVC]].

Spring Framework *Enable MVC Configuration*: same effect as `<mvc:annotation-driven/>`. As of **7.0** that XML namespace is **deprecated**. If `WebMvcConfigurer` cannot reach a knob, **remove** `@EnableWebMvc` and extend `WebMvcConfigurationSupport` or `DelegatingWebMvcConfiguration` yourself.

```d2
direction: down
ann: "@EnableWebMvc" {
  width: 180
  height: 50
  style.fill: "#e3f2fd"
}
imp: "DelegatingWebMvcConfiguration\nextends WebMvcConfigurationSupport" {
  width: 360
  height: 70
  style.fill: "#fff3e0"
}
beans: "HandlerMapping, HandlerAdapter,\nconverters, exception resolvers" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}

ann -> imp -> beans
```

**Fig. 1.** The annotation is an `@Import`, not a servlet. Boot already provides the equivalent via `WebMvcAutoConfiguration` (`@ConditionalOnMissingBean(WebMvcConfigurationSupport)`).

Spring Boot *Spring Web*: auto-configuration **replaces the need for `@EnableWebMvc` and the two cannot be used together**. Keep Boot MVC extras with a `WebMvcConfigurer` **without** this annotation. Add `@EnableWebMvc` only to take **complete control**.

> [!warning] One `@EnableWebMvc` only
> Official javadoc: only one `@Configuration` class may have it. Extra configurers implement `WebMvcConfigurer`; they must **not** repeat `@EnableWebMvc`.

> [!warning] Boot: this annotation disables `WebMvcAutoConfiguration`
> You lose Boot’s default static resource locations, `WebMvcProperties`, and related customizations. That is the usual production foot-gun.

> [!warning] Controllers still need scanning
> `@EnableWebMvc` wires the **adapter/mapping** beans. Without `@ComponentScan` / `@Bean`, there are no `@Controller`s to map.

> [!tip] Interview answer
> **`@EnableWebMvc` turns on MVC Java config — the same job as `<mvc:annotation-driven/>`.** It imports `DelegatingWebMvcConfiguration`. Use it in a classic WAR with `WebMvcConfigurer`. In Boot, skip it and implement `WebMvcConfigurer` only, or you override Boot’s MVC auto-configuration.
