<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`HttpMessageConverter` converts between HTTP messages and Java objects for given media types (`canRead` / `canWrite`, `read` / `write`).

`@RequestBody` / `@ResponseBody` (and `@RestController`) use these converters. JSON is typically `MappingJackson2HttpMessageConverter`.

You can extend `AbstractHttpMessageConverter` for a custom type.

> [!warning] Unverified traps from the dump
> - View rendering (JSP/Thymeleaf) does not go through HttpMessageConverter; that is ViewResolver.
