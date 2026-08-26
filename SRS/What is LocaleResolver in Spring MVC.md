<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Localization #SRS

# What is `LocaleResolver` in Spring MVC?

> [!abstract] Short answer
> **`DispatcherServlet`’s locale SPI:** a bean named **`localeResolver`** that **`resolveLocale(request)`** (never `null`) and optionally **`setLocale(request, response, locale)`**. Default implementation is **`AcceptHeaderLocaleResolver`**. Controllers and views should read the result through **`RequestContext.getLocale()`**, not by re-parsing headers.

## Resolve, then maybe store

`LocaleResolver` is a special bean type (same table as `HandlerMapping` / `ViewResolver`). If none is declared, the servlet installs **`AcceptHeaderLocaleResolver`**. `setLocale` may throw **`UnsupportedOperationException`** when the strategy cannot change locale (Accept-Language is client-owned; **`FixedLocaleResolver`** is JVM-fixed).

Since Spring 4.0, **`LocaleContextResolver`** extends the contract with a **`LocaleContext`** that can carry a **time zone**. Cookie and session resolvers implement it; the Accept-Language resolver does not. `RequestContext.getTimeZone()` is the app-facing API. Registered `Converter` / `Formatter` beans on the `ConversionService` pick that zone up for date/time formatting.

| Implementation | Where locale lives | `setLocale` |
| --- | --- | --- |
| `AcceptHeaderLocaleResolver` | `Accept-Language` | no |
| `CookieLocaleResolver` | cookie (stateless) | yes |
| `SessionLocaleResolver` | `HttpSession` attribute | yes |
| `FixedLocaleResolver` | configured / JVM default | no |

```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {

    @Bean
    public LocaleResolver localeResolver() {
        CookieLocaleResolver resolver = new CookieLocaleResolver();
        resolver.setDefaultLocale(Locale.ENGLISH);
        resolver.setCookieMaxAge(Duration.ofDays(30));
        return resolver;
    }

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LocaleChangeInterceptor());
    }
}
```

**Listing 1.** Conceptual Framework 7: bean **id/name `localeResolver`** is required. `LocaleChangeInterceptor` default param is **`locale`**, not `lang`. It calls `setLocale` on the resolver in the dispatcher context. Wiring with bundles: [[How do you localize a Spring MVC application]]. Registry: [[How do you register a HandlerInterceptor in Spring MVC]]. Message lookup: [[What is MessageSource in Spring]].

```d2
direction: down
req: "HTTP request" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
ds: "DispatcherServlet\nbean localeResolver" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
lci: "LocaleChangeInterceptor\n?locale=  → setLocale" {
  width: 280
  height: 60
  style.fill: "#fce4ec"
}
impl: "Accept-Language / cookie / session" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
rc: "RequestContext.getLocale()" {
  width: 260
  height: 45
  style.fill: "#f3e5f5"
}

req -> ds
ds -> lci
lci -> impl
impl -> rc
```

**Fig. 1.** Resolve on every request; change only if an interceptor (or controller) calls `setLocale` on a resolver that supports it.

`SessionLocaleResolver` is **not** Spring Session: it reads/writes `HttpSession` attributes and is gone when that session ends. Cookie default **max-age `-1`** is a browser-session cookie. `AcceptHeaderLocaleResolver.setSupportedLocales` matches **language and country**; `"en-GB"` does not match `["en-US"]` unless you also add `"en"`.

> [!warning] Default resolver plus interceptor
> Pairing `LocaleChangeInterceptor` with `AcceptHeaderLocaleResolver` (the servlet default) fails at runtime: `setLocale` is unsupported. Use cookie or session when the user picks a language.

> [!warning] Parameter name is `locale`
> Dumps that wire `paramName = "lang"` are a **custom** choice. The interceptor default is **`"locale"`**. A `?lang=de` URL does nothing unless you `setParamName("lang")`.

> [!warning] Wrong bean name
> A `LocaleResolver` that is not named **`localeResolver`** is ignored; the servlet keeps `AcceptHeaderLocaleResolver`.

> [!tip] Interview answer
> **`LocaleResolver` is how `DispatcherServlet` decides the request `Locale` — default Accept-Language.** Cookie or session resolvers can store a user choice; `LocaleChangeInterceptor` (query param `locale`) calls `setLocale`. Read the result with `RequestContext.getLocale()`, not by parsing headers yourself.
