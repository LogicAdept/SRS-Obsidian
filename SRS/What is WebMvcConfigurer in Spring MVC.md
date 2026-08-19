<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`WebMvcConfigurer` is the Java callback API for MVC: interceptors, resource handlers, CORS, message converters, content negotiation, exception resolvers, formatters.

Implement it on a `@Configuration` class (dumps still extend `WebMvcConfigurerAdapter`, which was deprecated).

Typical methods: `addInterceptors`, `addResourceHandlers`, `addCorsMappings`, `configureMessageConverters`, `configureContentNegotiation`.

> [!warning] Unverified traps from the dump
> - WebMvcConfigurerAdapter is deprecated; implement WebMvcConfigurer (Java 8 default methods).
> - @EnableWebMvc + WebMvcConfigurer is classic MVC; Boot prefers a WebMvcConfigurer bean without @EnableWebMvc.
