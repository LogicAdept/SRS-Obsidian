<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# How do you register a `HandlerInterceptor` in Spring MVC?

> [!abstract] Short answer
> Implement **`WebMvcConfigurer.addInterceptors(InterceptorRegistry)`** and call **`registry.addInterceptor(...)`**. Optionally **`addPathPatterns`** / **`excludePathPatterns`**. XML: `<mvc:interceptors>`. Java config wires interceptors only onto **MVC-managed `HandlerMapping` beans**; XML `MappedInterceptor` beans are detected by **any** `HandlerMapping`.

## Java config registry

Spring MVC *Interceptors*: override `addInterceptors` on a `@Configuration` `WebMvcConfigurer`. `InterceptorRegistry.addInterceptor` returns **`InterceptorRegistration`** so you can limit URL patterns.

`WebMvcConfigurer.addInterceptors` javadoc: interceptors apply to **controller method invocations and resource handler requests**, either all requests or a URL subset.

```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LocaleChangeInterceptor());
        registry.addInterceptor(new UserRoleAuthorizationInterceptor())
                .addPathPatterns("/**")
                .excludePathPatterns("/admin/**");
    }
}
```

**Listing 1.** Pattern from Spring Framework Interceptors reference (not a security recommendation). What the callbacks do: [[What is a HandlerInterceptor in Spring MVC]].

```xml
<mvc:interceptors>
    <bean class="org.springframework.web.servlet.i18n.LocaleChangeInterceptor"/>
    <mvc:interceptor>
        <mvc:mapping path="/**"/>
        <mvc:exclude-mapping path="/admin/**"/>
        <bean class="org.springframework.web.servlet.handler.UserRoleAuthorizationInterceptor"/>
    </mvc:interceptor>
</mvc:interceptors>
```

**Listing 2.** Conceptual XML from the same reference. XML registers **`MappedInterceptor`** beans visible to other frameworks’ `HandlerMapping`s.

```d2
direction: down
cfg: "WebMvcConfigurer\naddInterceptors" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
reg: "InterceptorRegistry\n+ path patterns" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
hm: "HandlerMapping\nexecution chain" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

cfg -> reg -> hm
```

**Fig. 1.** Registration is configuration; the mapping bean builds the interceptor + handler chain at request time.

To share the same interceptors with **non-MVC** `HandlerMapping` beans under Java config: declare **`MappedInterceptor` beans** and **do not** also add them in Java config (or configure both places). You can also set interceptors on a specific `HandlerMapping` bean’s `interceptors` property.

`preHandle` order follows registration order; `postHandle` / `afterCompletion` run **reverse** — [[What is a HandlerInterceptor in Spring MVC]].

> [!warning] Not a security filter chain
> Spring’s interceptor docs: path matching can **diverge** from annotated controllers. Use **Spring Security** (or a Servlet filter) early. `UserRoleAuthorizationInterceptor` in the sample is illustration, not a modern security design.

> [!warning] Java config vs XML visibility
> Java `addInterceptors` does **not** automatically apply to third-party `HandlerMapping` beans. XML `MappedInterceptor` does.

> [!warning] Path pattern style
> Prefer `/**` / `/admin/**` (`PathPattern`) as in current docs. A single `*` is not the same as `/**`.

> [!tip] Interview answer
> **Register with `WebMvcConfigurer.addInterceptors` and `InterceptorRegistry.addInterceptor`.** Add include/exclude path patterns on the registration. Remember Java config only feeds MVC’s own mappings unless you expose `MappedInterceptor` beans. Interceptors are not Spring Security.
