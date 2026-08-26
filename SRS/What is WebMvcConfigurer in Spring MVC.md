<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Boot #SRS

# What is `WebMvcConfigurer` in Spring MVC?

> [!abstract] Short answer
> **`WebMvcConfigurer` is the callback SPI to customize MVC Java config** without subclassing `WebMvcConfigurationSupport`. Implement it (Java 8 **default methods**) and override only what you need: interceptors, resources, CORS, formatters, exception resolvers, path matching, and so on. `@EnableWebMvc` **imports** `DelegatingWebMvcConfiguration`, which **autowires every** `WebMvcConfigurer` bean. In **Spring Boot**, register a `WebMvcConfigurer` **without** `@EnableWebMvc` so Boot’s MVC auto-configuration stays on.

## Callbacks, not a servlet

`WebMvcConfigurer` javadoc: `@EnableWebMvc` configuration classes implement this interface to customize the imported defaults. `DelegatingWebMvcConfiguration` (the class `@EnableWebMvc` actually imports) collects **all** `WebMvcConfigurer` beans. Only **one** `@Configuration` may carry `@EnableWebMvc`; many configurer beans are fine.

```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LocaleChangeInterceptor());
    }

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        registry.addResourceHandler("/assets/**")
                .addResourceLocations("classpath:/static/");
    }
}
```

**Listing 1.** Conceptual Boot-style configurer: **no** `@EnableWebMvc`. Interceptor registry: [[How do you register a HandlerInterceptor in Spring MVC]]. Exception chain: [[What is HandlerExceptionResolver in Spring MVC]] (`extendHandlerExceptionResolvers`, not `configure…` unless you take over). Converters: [[How do you configure message converters in Spring MVC]].

Spring Framework *Enable MVC Configuration*: `@EnableWebMvc` ≈ XML `<mvc:annotation-driven/>` (that XML namespace is **deprecated as of 7.0**). Framework and Boot both say: Boot apps should use `WebMvcConfigurer` **without** `@EnableWebMvc`. Boot *Spring Web*: auto-configuration **replaces** `@EnableWebMvc` and **the two cannot be used together**. Adding `@EnableWebMvc` takes **complete control** of MVC (you lose Boot extras: default static locations, `WebMvcProperties`, and so on). `WebMvcAutoConfiguration` is `@ConditionalOnMissingBean(WebMvcConfigurationSupport.class)` — `@EnableWebMvc` provides that bean.

```d2
direction: down
enable: "@EnableWebMvc\nimports DelegatingWebMvcConfiguration" {
  width: 360
  height: 70
  style.fill: "#fff3e0"
}
boot: "Boot WebMvcAutoConfiguration\nno EnableWebMvc" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
cfg: "WebMvcConfigurer beans" {
  width: 260
  height: 55
  style.fill: "#e8f5e9"
}

enable -> cfg
boot -> cfg
```

**Fig. 1.** Same callback interface; Boot supplies the `DelegatingWebMvcConfiguration` equivalent itself. Annotation: [[What is the EnableWebMvc annotation]].

For gaps the configurer does not expose, drop `@EnableWebMvc` and extend **`WebMvcConfigurationSupport`** / **`DelegatingWebMvcConfiguration`** (or Boot’s `WebMvcRegistrations` for swapping mapping/adapter/exception-resolver types while keeping Boot MVC).

> [!warning] Do not extend `WebMvcConfigurerAdapter`
> Deprecated since **5.0**: `WebMvcConfigurer` has default methods. Implement the interface.

> [!warning] `@EnableWebMvc` in Boot turns off auto-config
> Official Boot docs: keep MVC customizations with a `WebMvcConfigurer` **bean**, **without** that annotation. `@EnableWebMvc` is the “I own MVC now” switch.

> [!warning] `configure*` vs `extend*` / `add*`
> `configureHandlerExceptionResolvers` and the old `configureMessageConverters(List)` start from an **empty** list — adding one entry **replaces** framework defaults. Prefer `extendHandlerExceptionResolvers` and Boot-era converter builders.

> [!tip] Interview answer
> **`WebMvcConfigurer` is how you tweak MVC Java config: interceptors, CORS, resources, formatters.** Multiple configurer beans are composed. In a WAR with `@EnableWebMvc` that is required. In Boot, implement `WebMvcConfigurer` and skip `@EnableWebMvc` or you disable Boot’s MVC auto-configuration.
