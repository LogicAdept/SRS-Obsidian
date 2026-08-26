<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Spring/Framework/WebMvc #SRS

# How do you implement exception handling in Spring Boot?

> [!abstract] Short answer
> Use **two layers**. **`@ExceptionHandler`** on a `@Controller` (local) or **`@ControllerAdvice` / `@RestControllerAdvice`** (global) runs **inside** `DispatcherServlet` and can return **`ProblemDetail`**, `ErrorResponse`, or a `ResponseEntity`. Unhandled exceptions fall through to Boot’s **`/error`** mapping (`BasicErrorController`): JSON for APIs, the **whitelabel** HTML page for browsers. Turn on RFC 9457 for built-in MVC exceptions with **`spring.mvc.problemdetails.enabled=true`** (Boot auto-registers a `ResponseEntityExceptionHandler` at **order 0**).

## MVC resolvers first, then `/error`

`DispatcherServlet` asks `HandlerExceptionResolver` beans. `@ExceptionHandler` methods are one resolver. Prefer a **specific** exception type. **`@RestControllerAdvice`** is `@ControllerAdvice` + `@ResponseBody` (Framework **4.3**, not a Boot-only annotation). **`ResponseEntityExceptionHandler`** is a **base class** for advice: it already maps Spring MVC `ErrorResponse` exceptions (validation, media type, 404 resource, …) to a **ProblemDetail** body. Override a `handle*` method or add your own `@ExceptionHandler`.

Boot then registers **`/error`** as the servlet container’s global error page. Machine clients get JSON (`timestamp`, `status`, `error`, `message`, `path` via `ErrorAttributes`). Replace contents with an **`ErrorAttributes`** bean, or replace the controller with **`ErrorController`** / subclass **`BasicErrorController`**. Custom HTML: `public/error/404.html` or `templates/error/5xx.ftlh`. Properties live under **`spring.web.error.*`**.

```java
@RestControllerAdvice
public class ApiErrors {

    @ExceptionHandler(IllegalArgumentException.class)
    public ProblemDetail badArg(IllegalArgumentException ex) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
    }
}
```

**Listing 1.** Conceptual: return RFC 9457 from advice. Annotation mechanics: [[What does the ExceptionHandler annotation do]]. Advice vs body: [[What is the difference between ControllerAdvice and RestControllerAdvice]]. Fields: [[What is ProblemDetail in Spring]]. Validation: [[How does Bean Validation work in Spring Boot]].

```yaml
spring:
  mvc:
    problemdetails:
      enabled: true
```

**Listing 2.** Conceptual Boot property: built-in MVC exceptions as `application/problem+json`. Your advice that **also** extends `ResponseEntityExceptionHandler` can clash with Boot’s order-**0** bean — handle a **specific** type on a **separate** `@ControllerAdvice` ordered **ahead** of 0.

```d2
direction: down
ctrl: "Controller throws" {
  width: 200
  height: 40
  style.fill: "#e3f2fd"
}
eh: "@ExceptionHandler\nController or Advice" {
  width: 260
  height: 55
  style.fill: "#fff3e0"
}
err: "BasicErrorController\n/error" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}

ctrl -> eh
eh -> err: "unhandled"
```

**Fig. 1.** Handled in MVC: client never sees `/error`. Unhandled: container forwards to Boot’s error page.

> [!warning] Catch-all `Exception` + 400
> A global `@ExceptionHandler(Exception.class)` with **`@ResponseStatus(BAD_REQUEST)`** turns **bugs** into 400s and can hide Boot’s `/error` attributes. Match **your** types; leave framework exceptions to `ResponseEntityExceptionHandler` / DefaultHandlerExceptionResolver.

> [!warning] Two `ResponseEntityExceptionHandler` beans
> Boot’s problem-details advice is **order 0**. A second subclass that also handles `ErrorResponse` may never run for built-in types unless your advice is **ordered first**.

> [!warning] `/error` is not `@ExceptionHandler`
> Filters that call **`sendError`**, or exceptions **outside** the servlet mapping, skip controller advice and land on **`ErrorController`**. Customize `ErrorAttributes` / error views for those.

> [!tip] Interview answer
> Local `@ExceptionHandler` on the controller, or global `@RestControllerAdvice` returning `ProblemDetail`. Boot’s `/error` is the **fallback** JSON/HTML page. Enable **`spring.mvc.problemdetails.enabled`** for RFC 9457 on Spring MVC’s own exceptions; `MethodArgumentNotValidException` is one of those.
