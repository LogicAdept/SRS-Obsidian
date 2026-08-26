<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #API/REST #SRS

# What is `ProblemDetail` in Spring?

> [!abstract] Short answer
> **`ProblemDetail` is Spring’s RFC 9457 error body** (since Framework **6.0**): **`type`**, **`title`**, **`status`**, **`detail`**, **`instance`**, plus a **`properties`** map for extra fields. Return it (or **`ErrorResponse`**) from `@ExceptionHandler` / `@RequestMapping`. Jackson writes **`application/problem+json`**. Dump “RFC 7807” is the **old** name; Spring documents **9457**. Boot can auto-enable this for MVC exceptions with **`spring.mvc.problemdetails.enabled`**.

## Spec fields, then extras

Factories: `forStatus`, `forStatusAndDetail`. Missing **`type`** is treated as **`about:blank`**. Default **`title`**, if unset, is the **`HttpStatus` reason phrase** for well-known codes. On `@ExceptionHandler`, **`instance`** defaults to the **request path**. Jackson **`ProblemDetailJacksonMixin`** unwraps `properties` as **top-level JSON keys**.

**`ErrorResponse`** is status + headers + a `ProblemDetail` body. Spring MVC exceptions implement it. **`ErrorResponseException`** is a convenient base. **`ResponseEntityExceptionHandler`** (`@ControllerAdvice`) renders built-in web exceptions as problem details. `WebMvcConfigurer.addErrorResponseInterceptors` (6.2+) runs before render.

i18n: codes `problemDetail.type.|title.|` + FQCN; detail `problemDetail.` + FQCN.

```java
@ExceptionHandler(IllegalArgumentException.class)
public ProblemDetail badArg(IllegalArgumentException ex) {
    return ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
}
```

**Listing 1.** Conceptual: status drives HTTP status; body is RFC 9457. Handlers: [[What does the ExceptionHandler annotation do]]. Status-only (often HTML): [[What is the ResponseStatus annotation in Spring MVC]]. Entity wrapper: [[What is the difference between ResponseBody and ResponseEntity]].

```java
return ResponseEntity.of(problemDetail).build();
```

**Listing 2.** Conceptual Framework 6: `ResponseEntity.of(ProblemDetail)` copies the problem’s status. If you have no extra headers, returning `ProblemDetail` alone is enough.

```d2
direction: down
ex: "exception" {
  width: 160
  height: 40
  style.fill: "#e3f2fd"
}
pd: "ProblemDetail\ntype title status detail instance" {
  width: 320
  height: 60
  style.fill: "#fff3e0"
}
json: "application/problem+json" {
  width: 260
  height: 45
  style.fill: "#e8f5e9"
}

ex -> pd
pd -> json
```

**Fig. 1.** Clients decode a stable shape instead of `{error, message}`. `WebClient` / `RestClient` can `getResponseBodyAs(ProblemDetail.class)`.

> [!warning] RFC number
> Interview dumps still say **7807**. Spring **6/7 javadoc is RFC 9457** (7807’s successor). Same field names; cite 9457.

> [!warning] Boot default is off
> `spring.mvc.problemdetails.enabled` autoconfigures `ResponseEntityExceptionHandler` at **order 0**. Custom `@ControllerAdvice` for a built-in exception must be **ordered ahead** of Boot’s handler.

> [!warning] `@ResponseStatus` + `reason`
> That path uses **`sendError`** and a container **HTML** page — not `ProblemDetail`. REST APIs should return `ProblemDetail` / `ErrorResponse`, not a non-empty `@ResponseStatus` reason.

> [!tip] Interview answer
> **`ProblemDetail` is the RFC 9457 JSON error body: type, title, status, detail, instance.** Return it from `@ExceptionHandler`. Spring MVC exceptions already implement `ErrorResponse`. Prefer it over ad-hoc `{message}` maps so clients can parse errors uniformly.
