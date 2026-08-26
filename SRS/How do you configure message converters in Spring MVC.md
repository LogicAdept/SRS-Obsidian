<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# How do you configure message converters in Spring MVC?

> [!abstract] Short answer
> Implement **`WebMvcConfigurer`** and override **`configureMessageConverters`**. As of Spring Framework **7.0**, that method takes **`HttpMessageConverters.ServerBuilder`** — register JSON/XML converters with `withJsonConverter` / `withXmlConverter`. The older **`List<HttpMessageConverter<?>>`** overload (and **`extendMessageConverters`**) is **deprecated for removal**.

## MVC Java config callback

Spring MVC *Message Converters*: customize `HttpMessageConverter` instances by overriding `configureMessageConverters()`. The 7.0 example builds Jackson 3 `JsonMapper` / `XmlMapper` and wraps them in `JacksonJsonHttpMessageConverter` / `JacksonXmlHttpMessageConverter`.

`WebMvcConfigurer` javadoc (7.0): the new `configureMessageConverters(HttpMessageConverters.ServerBuilder)` **configures the converters instance being built**.

```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {

    @Override
    public void configureMessageConverters(HttpMessageConverters.ServerBuilder builder) {
        JsonMapper jsonMapper = JsonMapper.builder()
                .findAndAddModules()
                .enable(SerializationFeature.INDENT_OUTPUT)
                .build();
        builder.withJsonConverter(new JacksonJsonHttpMessageConverter(jsonMapper));
    }
}
```

**Listing 1.** Conceptual Spring Framework 7 MVC config from the Message Converters reference. What converters do at runtime: [[What is HttpMessageConverter in Spring MVC]]. JSON from controllers: [[How do you return JSON from a Spring MVC controller]].

```d2
direction: down
cfg: "WebMvcConfigurer\nconfigureMessageConverters" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
list: "HttpMessageConverter list\n(JSON, XML, …)" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
use: "@RequestBody / @ResponseBody\nRequestMappingHandlerAdapter" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}

cfg -> list -> use
```

**Fig. 1.** Configurer populates converters used for HTTP body read/write, not for HTML views (`ViewResolver`).

### Pre-7.0 `List` API (still in dumps)

Deprecated `configureMessageConverters(List)`: **by default all built-in converters are registered** when Jackson/JAXB/etc. are on the classpath. **Using that method turns off default converter registration** — if you only `add` one converter, you can drop the rest.

Deprecated `extendMessageConverters(List)`: modify the **already configured** list without wiping defaults.

In **Spring Boot**, `WebMvcAutoConfiguration` still adds `HttpMessageConverter` beans and defaults even if you used the empty-list `configure` method — javadoc points Boot apps at **`HttpMessageConverters`** or `extendMessageConverters`. Implement `WebMvcConfigurer` **without** `@EnableWebMvc` if you want to keep Boot’s MVC auto-config.

> [!warning] Old `configureMessageConverters(List)` replaces defaults
> Adding only `MappingJackson2HttpMessageConverter` can remove form, byte-array, and String converters. Prefer the **7.0 builder**, or historically **`extendMessageConverters`**.

> [!warning] `MappingJackson2HttpMessageConverter` is deprecated in 7.0
> Spring 7 JSON path is **`JacksonJsonHttpMessageConverter`** (Jackson 3). Dump listings with Jackson 2 types are the previous generation.

> [!warning] `@EnableWebMvc` disables Boot MVC auto-config
> Full `@EnableWebMvc` means you own converter setup. Boot apps usually customize via `WebMvcConfigurer` only.

> [!tip] Interview answer
> **Override `WebMvcConfigurer.configureMessageConverters`.** In Spring 7 you get a `ServerBuilder` to plug in Jackson JSON/XML converters. On older APIs, `configureMessageConverters(List)` **clears** defaults; `extendMessageConverters` **appends**. Boot may still inject default converter beans unless you take over with `@EnableWebMvc`.
