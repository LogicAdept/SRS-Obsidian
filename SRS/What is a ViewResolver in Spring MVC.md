<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is a `ViewResolver` in Spring MVC?

> [!abstract] Short answer
> **`ViewResolver` maps a logical view name to a `View`.** The controller returns a name (or `ModelAndView`); the resolver builds the technology-specific renderer (JSP, FreeMarker, …). **`View`** then prepares the model and hands off to that technology. Default when none are declared: **`InternalResourceViewResolver`**. `@ResponseBody` / `@RestController` skip this path and use **`HttpMessageConverter`**.

## Name in, `View` out

`ViewResolver.resolveViewName(String, Locale)` returns a `View` or **`null`** so resolvers can be **chained**. `DispatcherServlet` detects all `ViewResolver` beans by type (`detectAllViewResolvers` defaults to **true**). If none exist, it uses `InternalResourceViewResolver`. The well-known bean name **`viewResolver`** matters only when detection is off.

Spring Framework *View Resolution* table (current): `UrlBasedViewResolver` (prefix/suffix → URL), `InternalResourceViewResolver` (JSP / `InternalResourceView`, `JstlView` if JSTL is present), `FreeMarkerViewResolver`, `BeanNameViewResolver` (view name = bean name), `ContentNegotiatingViewResolver` (delegates; picks by `Accept` / file name / format parameter). Implementations often extend `AbstractCachingViewResolver`.

```java
@Bean
public ViewResolver jsp() {
    return new InternalResourceViewResolver("/WEB-INF/views/", ".jsp");
}
```

**Listing 1.** Conceptual JSP resolver. Constructor prefix/suffix since 4.3. Put JSPs under `WEB-INF` so they are not hit by a raw URL. JSON body path: [[How do you return JSON from a Spring MVC controller]]. `@Controller` vs `@RestController`: [[What is the difference between Spring RestController and Controller]].

```d2
direction: down
ctrl: "Controller\nString view name" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
vr: "ViewResolver chain\norder: low → high" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
view: "View.render\nJSP / FreeMarker / …" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
skip: "@ResponseBody\nHttpMessageConverter" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

ctrl -> vr
vr -> view
ctrl -> skip
```

**Fig. 1.** HTML names go through resolvers; REST bodies do not. Redirect prefix: [[How do you redirect after a form POST in Spring MVC]].

`UrlBasedViewResolver` treats **`redirect:`** as an HTTP redirect and **`forward:`** as `RequestDispatcher.forward()`. `forward:` is not useful with `InternalResourceViewResolver` itself (already a forward).

`ContentNegotiatingViewResolver` does **not** resolve names. It asks other resolvers, then picks the first `View` whose content type matches the negotiated media type. Default order is **`Ordered.HIGHEST_PRECEDENCE`**. `defaultViews` are extra singleton `View`s that ignore the logical name.

> [!warning] JSP resolver must be last
> `InternalResourceViewResolver` cannot cheaply test that a JSP exists, so it **always** returns a `View`. Official rule: put it **last** (`order` **higher** = later in the chain). A `UrlBasedViewResolver` using `InternalResourceView` has the same last-in-chain rule.

> [!warning] `@ResponseBody` never hits this SPI
> Message converters write the HTTP body. `ContentNegotiatingViewResolver` is still **view** negotiation, not Jackson on a `@RestController`.

> [!warning] Velocity is not in Spring 7
> Current Framework lists FreeMarker and JSP, not Velocity. “Jasper” is Tomcat’s JSP compiler, not a `ViewResolver`.

> [!warning] Declaring one resolver replaces the default list
> Adding any `ViewResolver` bean overrides DispatcherServlet’s built-in `InternalResourceViewResolver`. You must then register every resolver you actually need.

> [!tip] Interview answer
> **A `ViewResolver` turns a logical view name into a `View` so controllers stay independent of JSP or FreeMarker.** Chain them by `order`; JSP’s `InternalResourceViewResolver` goes last because it never returns `null`. REST methods with `@ResponseBody` skip view resolution entirely.
