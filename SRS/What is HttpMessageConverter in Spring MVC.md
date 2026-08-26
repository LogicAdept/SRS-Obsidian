<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is `HttpMessageConverter` in Spring MVC?

> [!abstract] Short answer
> **`HttpMessageConverter<T>`** is Spring’s strategy for **reading Java objects from HTTP request bodies** and **writing them to response bodies**, gated by **media type** (`canRead` / `canWrite`, then `read` / `write`). **`@RequestBody`**, **`@ResponseBody`**, **`@RestController`**, and **`ResponseEntity`** use this list. HTML **view names** go through **`ViewResolver`**, not converters.

## Body codec, not a view engine

`HttpMessageConverter` javadoc (since 3.0): convert **from and to HTTP requests and responses**. `canRead(Class, MediaType)` typically consults **`Content-Type`**; `canWrite` consults **`Accept`**. `getSupportedMediaTypes()` lists what the converter advertises.

`RequestMappingHandlerAdapter` walks registered converters until one claims the type + media type. JSON in Spring Framework **7.0** is **`JacksonJsonHttpMessageConverter`** (`application/json`, `application/*+json`). **`MappingJackson2HttpMessageConverter`** (Jackson 2) is **deprecated for removal**. Custom formats usually subclass **`AbstractHttpMessageConverter`**.

```java
public interface HttpMessageConverter<T> {
    boolean canRead(Class<?> clazz, MediaType mediaType);
    boolean canWrite(Class<?> clazz, MediaType mediaType);
    T read(Class<? extends T> clazz, HttpInputMessage inputMessage) throws IOException;
    void write(T t, MediaType contentType, HttpOutputMessage outputMessage) throws IOException;
}
```

**Listing 1.** Conceptual interface from Spring Framework 7.0.9 javadoc (methods abbreviated). Register/replace converters: [[How do you configure message converters in Spring MVC]]. JSON controllers: [[How do you return JSON from a Spring MVC controller]].

```d2
direction: right
body: "@RequestBody\nAccount JSON" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
c: "HttpMessageConverter\ncanRead → read" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
obj: "Account instance" {
  width: 180
  height: 60
  style.fill: "#e8f5e9"
}

body -> c -> obj
```

**Fig. 1.** Converters operate on `HttpInputMessage` / `HttpOutputMessage`, not on JSP/Thymeleaf templates.

Spring MVC *Return Values*: `@ResponseBody` / `ResponseEntity` are converted through `HttpMessageConverter` implementations. A `String` **without** `@ResponseBody` is a **view name**.

> [!warning] Views do not use this SPI
> JSP, Thymeleaf, and `View` objects go through **`ViewResolver`**. Putting Jackson on the classpath does not serialize a form view.

> [!warning] 406 / 415 are converter misses
> No converter for the negotiated type → **`HttpMediaTypeNotAcceptableException`** (write) or **`HttpMediaTypeNotSupportedException`** (read), not a silent fallback to HTML.

> [!warning] Jackson 2 vs 3 class names
> Interview dumps still say `MappingJackson2HttpMessageConverter`. On Spring **7**, prefer **`JacksonJsonHttpMessageConverter`**.

> [!tip] Interview answer
> **`HttpMessageConverter` maps HTTP bodies to objects and back for a media type.** REST annotations pick a converter from the MVC list. HTML templates are `ViewResolver` territory. JSON is a Jackson converter, not `@RestController` magic by itself.
