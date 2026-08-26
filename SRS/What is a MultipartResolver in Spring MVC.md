<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Boot #SRS

# What is a `MultipartResolver` in Spring MVC?

> [!abstract] Short answer
> **`MultipartResolver` is the `DispatcherServlet` SPI that parses RFC 1867 multipart requests** and wraps them as **`MultipartHttpServletRequest`**, so controllers can read **`MultipartFile`**. There is **no default** on a plain `DispatcherServlet`: you must register a bean named **`multipartResolver`**. Framework 7’s implementation is **`StandardServletMultipartResolver`** (Servlet **`Part`** API). **Spring Boot** turns it on by default (`spring.servlet.multipart.enabled=true`) and sets size limits on the servlet, not on the resolver bean.

## Parse, wrap, then clean up

`isMultipart` typically looks for `multipart/form-data` (or any `multipart/` unless **strict Servlet compliance**). `resolveMultipart` wraps the request; `cleanupMultipart` drops temp storage. Size/location limits are **servlet `multipart-config` / `MultipartConfigElement`**, not resolver properties. Parse failures throw **`MultipartException`**.

Controllers rarely inject the resolver. Use `@RequestParam MultipartFile`, `@RequestPart`, or cast to `MultipartHttpServletRequest`. `MultipartFilter` exists for apps **without** Spring MVC, delegating to a root-context `multipartResolver`.

```java
@Override
protected void customizeRegistration(ServletRegistration.Dynamic registration) {
    registration.setMultipartConfig(new MultipartConfigElement("/tmp"));
}
```

**Listing 1.** Conceptual Framework example: classic MVC must mark the servlet for Part parsing, then expose bean **`multipartResolver`**. Boot: [[How do you implement file upload and download in Spring Boot]]. Parameters: [[What is the difference between RequestParam and PathVariable]]. Special beans: [[What is Spring MVC DispatcherServlet]].

```properties
spring.servlet.multipart.enabled=true
spring.servlet.multipart.max-file-size=1MB
spring.servlet.multipart.max-request-size=10MB
spring.servlet.multipart.file-size-threshold=0B
```

**Listing 2.** Boot 3.5 defaults (appendix). `location` is empty unless you set it. `resolve-lazily` defaults **false** (fail at wrap time). `strict-servlet-compliance` defaults **false** (Tomcat may wrap non-form `multipart/` types; Jetty may not).

```d2
direction: down
req: "multipart/form-data POST" {
  width: 240
  height: 45
  style.fill: "#e3f2fd"
}
ds: "DispatcherServlet\nbean multipartResolver" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
wrap: "MultipartHttpServletRequest\nMultipartFile parts" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}

req -> ds
ds -> wrap
```

**Fig. 1.** No bean (and no Boot auto-config) → the request is not wrapped; `MultipartFile` arguments do not bind.

> [!warning] Bean name is `multipartResolver`
> Any other id is ignored. Classic XML/Java MVC without that bean does **not** parse uploads.

> [!warning] Limits live on the servlet
> Setting sizes only on a Spring bean does nothing for `StandardServletMultipartResolver`. Use `MultipartConfigElement` or Boot’s `spring.servlet.multipart.max-*-size`.

> [!warning] Commons FileUpload resolver is gone
> Spring 6+ dropped `CommonsMultipartResolver`. The remaining type is **`StandardServletMultipartResolver`**. Where files land on disk is **your** storage code, not this SPI.

> [!tip] Interview answer
> **`MultipartResolver` is how `DispatcherServlet` turns a multipart POST into `MultipartFile`.** Register it as **`multipartResolver`**; Boot does that for you and caps sizes via `spring.servlet.multipart.*`. Max size is servlet multipart config, not a property on the resolver itself.
