<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Localization #SRS

# How do you localize a Spring MVC application?

> [!abstract] Short answer
> Wire **three named pieces**: a **`MessageSource`** bean named **`messageSource`** (usually `ResourceBundleMessageSource` over classpath bundles), a **`LocaleResolver`** bean named **`localeResolver`** (default is **`AcceptHeaderLocaleResolver`**), and views or controllers that resolve codes (`<spring:message>` / `getMessage`). To **switch** locale from a query parameter, add **`LocaleChangeInterceptor`** and a resolver that implements **`setLocale`** (cookie or session — **not** the Accept-Language default).

## Bundles, locale, then lookup

`ApplicationContext` **is** a `MessageSource`. On load it looks for a bean named **`messageSource`**. Typical implementation: `ResourceBundleMessageSource` with JDK `ResourceBundle` basenames (`messages.properties`, `messages_fr.properties`, …). Fallback follows JDK rules (`en_GB` → `en` → default). Missing bean → empty `DelegatingMessageSource`.

`DispatcherServlet` looks for **`localeResolver`**. If none, it uses **`AcceptHeaderLocaleResolver`** (`Accept-Language`). On each request it resolves the locale; **`RequestContext.getLocale()`** is the stable API in controllers and views. `LocaleChangeInterceptor` (default param **`locale`**) calls `setLocale` on that resolver.

```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {

    @Bean
    public MessageSource messageSource() {
        ResourceBundleMessageSource source = new ResourceBundleMessageSource();
        source.setBasename("messages");
        source.setDefaultEncoding("UTF-8");
        return source;
    }

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

**Listing 1.** Conceptual MVC i18n wiring (Spring Framework 7). Bean names **`messageSource`** and **`localeResolver`** are required. Interceptor registry: [[How do you register a HandlerInterceptor in Spring MVC]]. SPI: [[What is LocaleResolver in Spring MVC]]. Context API: [[What is MessageSource in Spring]].

```jsp
<%@ taglib prefix="spring" uri="http://www.springframework.org/tags" %>
<spring:message code="welcome" text="Welcome"/>
```

**Listing 2.** Conceptual JSP: `MessageTag` resolves `code` through the current `ApplicationContext` as `MessageSource`, using the request locale. `text` is the fallback if the code is missing.

```d2
direction: down
req: "HTTP request\nAccept-Language / cookie / ?locale=" {
  width: 320
  height: 70
  style.fill: "#e3f2fd"
}
lci: "LocaleChangeInterceptor\nsetLocale on resolver" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
lr: "LocaleResolver\nbean localeResolver" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
ms: "MessageSource\nbean messageSource" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}
out: "spring:message / getMessage" {
  width: 280
  height: 60
  style.fill: "#f3e5f5"
}

req -> lci
lci -> lr
lr -> ms
ms -> out
```

**Fig. 1.** Locale is chosen first; message codes are looked up second. The JSP tag does not invent a separate catalog — it uses the same `messageSource` bean.

Spring Boot auto-configures a `MessageSource` when **`messages.properties`** exists at the classpath root (`spring.messages.basename`, default `messages`). Classic XML/Java still declare the bean by name.

> [!warning] Default resolver cannot switch locale
> `AcceptHeaderLocaleResolver.setLocale` is unsupported: the header is client-controlled. Pairing it with `LocaleChangeInterceptor` fails at runtime. Use `CookieLocaleResolver` or `SessionLocaleResolver` when the user picks a language.

> [!warning] Bean names are not optional
> A `MessageSource` that is not named **`messageSource`** is ignored; the context falls back to an empty delegate. Same for **`localeResolver`**.

> [!warning] Boot needs the default bundle file
> Language-only files (`messages_de.properties`) without **`messages.properties`** skip Boot auto-configuration. `ResourceBundleMessageSource` still defaults to **ISO-8859-1** unless you set encoding (UTF-8 is the usual fix).

> [!warning] Session vs cookie
> `SessionLocaleResolver` stores locale on **`HttpSession`** and loses it when the session ends. It is not Spring Session. Cookie persists across sessions; default max-age **-1** is a browser-session cookie.

> [!tip] Interview answer
> **Put strings in resource bundles behind a `messageSource` bean, resolve the user’s `Locale` with a `localeResolver`, and look up codes in the view or with `MessageSource.getMessage`.** The servlet default is Accept-Language only. To let the user switch language, register `LocaleChangeInterceptor` and a cookie or session resolver — not `AcceptHeaderLocaleResolver`.
