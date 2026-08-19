<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Implement `HandlerInterceptor` (or extend the adapter class dumps name) and register it on `WebMvcConfigurer.addInterceptors`:

```java
@Override
public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(new LogInterceptor());
    registry.addInterceptor(new AdminInterceptor())
        .addPathPatterns("/admin/*")
        .excludePathPatterns("/admin/oldLogin");
}
```

You can also attach interceptors to a specific `HandlerMapping`.

> [!warning] Unverified traps from the dump
> - Order of registration is the preHandle order; postHandle and afterCompletion run in reverse.
> - Path patterns on InterceptorRegistry are not a substitute for Spring Security.
