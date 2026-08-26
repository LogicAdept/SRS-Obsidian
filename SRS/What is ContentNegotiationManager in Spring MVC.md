<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is `ContentNegotiationManager` in Spring MVC?

> [!abstract] Short answer
> **`ContentNegotiationManager` is the facade that decides which media types a request asked for.** It delegates to an ordered list of **`ContentNegotiationStrategy`** instances. **`ContentNegotiationManager()` defaults to `HeaderContentNegotiationStrategy` only** (`Accept`). Query-parameter resolution (`?format=`) is **off** until you turn **`favorParameter(true)`** and register **`mediaType` mappings**. Path-extension negotiation is **not** a Framework 7 configurer option.

## Strategies, not a servlet

The manager also implements **`MediaTypeFileExtensionResolver`** (media type → file extensions). `resolveMediaTypes` orders by specificity then `q`. Unparseable `Accept` → **`HttpMediaTypeNotAcceptableException`**. Empty request → `MEDIA_TYPE_ALL_LIST` (`*/*`).

`WebMvcConfigurer.configureContentNegotiation` builds the manager via **`ContentNegotiationConfigurer`**. Framework 7 table:

| Setter | Default | Strategy | On? |
| --- | --- | --- | --- |
| `favorParameter` | `false` | `ParameterContentNegotiationStrategy` | no |
| `ignoreAcceptHeader` | `false` | `HeaderContentNegotiationStrategy` | **yes** |
| `defaultContentType` | unset | `FixedContentNegotiationStrategy` | no |

Parameter name defaults to **`format`**. `mediaType("json", APPLICATION_JSON)` is required for the parameter strategy; those keys are also treated as safe for **RFD** checks. As of 5.0 you can replace the whole list with **`strategies(...)`**.

```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {

    @Override
    public void configureContentNegotiation(ContentNegotiationConfigurer configurer) {
        configurer.mediaType("json", MediaType.APPLICATION_JSON);
        configurer.mediaType("xml", MediaType.APPLICATION_XML);
        configurer.favorParameter(true);
    }
}
```

**Listing 1.** Conceptual Framework 7: register keys, then optionally enable `?format=json`. Config SPI: [[What is WebMvcConfigurer in Spring MVC]]. JSON writing: [[How do you return JSON from a Spring MVC controller]]. Converters: [[What is HttpMessageConverter in Spring MVC]].

```d2
direction: down
req: "HTTP request" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
mgr: "ContentNegotiationManager" {
  width: 260
  height: 45
  style.fill: "#fff3e0"
}
hdr: "HeaderContentNegotiationStrategy\nAccept (default on)" {
  width: 300
  height: 55
  style.fill: "#e8f5e9"
}
param: "ParameterContentNegotiationStrategy\n?format= (default off)" {
  width: 320
  height: 55
  style.fill: "#fce4ec"
}

req -> mgr
mgr -> hdr
mgr -> param
```

**Fig. 1.** Default is the `Accept` header. Path extensions (`/data.json`) are not in this Framework 7 configurer; use a query parameter if you need URL-based selection.

> [!warning] `favorPathExtension` is gone
> Older dumps treat path suffixes as a default (`favorPathExtension=true`). In 5.2.4+ that API was **deprecated and default `false`**; **Framework 7 `ContentNegotiationConfigurer` no longer exposes it**. Prefer `?format=` over `/file.xml`.

> [!warning] Parameter strategy needs mappings
> `favorParameter(true)` without `mediaType(...)` cannot resolve keys. The docs: register mappings or the parameter strategy does not work.

> [!warning] Turning off `Accept`
> `ignoreAcceptHeader(true)` disables the only default strategy. Then you need `favorParameter`, `defaultContentType`, or a custom `strategies` list, or every request looks like “no type requested”.

> [!tip] Interview answer
> **`ContentNegotiationManager` asks a list of strategies what media types the client wants — by default only the `Accept` header.** Turn on `favorParameter` and map `format=json` if you need a URL switch. Path extensions are a retired, RFD-risky approach and are not on the Spring 7 configurer.
