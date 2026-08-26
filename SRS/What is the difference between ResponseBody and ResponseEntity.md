<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #API/REST #Java/Annotations #SRS

# What is the difference between `ResponseBody` and `ResponseEntity`?

> [!abstract] Short answer
> **`@ResponseBody` writes the return value through `HttpMessageConverter`s and skips view resolution.** Default success status is **200 OK** unless you also set status another way (`@ResponseStatus`, servlet API). **`ResponseEntity<T>` is a return type**: body **plus** **`HttpStatusCode` and `HttpHeaders`**. You do **not** need `@ResponseBody` on a method that returns `ResponseEntity` — `HttpEntity` / `ResponseEntity` are first-class MVC return values. `@RestController` already implies `@ResponseBody` on every method.

## Annotation vs wrapper

`@ResponseBody` (since 3.0; type-level since 4.0) is the “write this object as the body” marker. `@RestController` inherits it.

`ResponseEntity` (since 3.0.2) **extends `HttpEntity`** with a status. Same converters write `getBody()`. Builders: `ok()`, `created(URI)`, `accepted()`, `noContent()`, `badRequest()`, `notFound()`, `unprocessableContent()` (7.0; `unprocessableEntity()` deprecated), `internalServerError()`, `status(...)`. `of(Optional)` / `ofNullable` → 200 with body or **404** if empty/`null`. `of(ProblemDetail)` copies the problem’s status.

```java
@GetMapping("/handle")
public ResponseEntity<String> handle() {
    URI location = URI.create("/resource/1");
    return ResponseEntity.created(location)
            .header("MyResponseHeader", "MyValue")
            .body("Hello World");
}
```

**Listing 1.** Conceptual Framework javadoc: **201 + Location + body**. `created` takes a **`URI`**, not the domain object. Body-only pair: [[What is the difference between RequestBody and ResponseBody]]. `@RestController`: [[What is the difference between Spring RestController and Controller]]. Method-level status without a wrapper: [[What is the ResponseStatus annotation in Spring MVC]].

```java
@GetMapping("/resource")
@ResponseBody
public Resource bodyOnly() {
    return resource;
}
```

**Listing 2.** Conceptual: converters write `Resource`; status stays **200** unless something else changes it. Errors can still be **4xx/5xx** via exception resolvers — not “only 500”.

```d2
direction: down
ret: "controller return value" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
rb: "@ResponseBody\nconverters → body\nstatus default 200" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
re: "ResponseEntity\nstatus + headers + body" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

ret -> rb
ret -> re
```

**Fig. 1.** Same converter pipeline. `ResponseEntity` is how you set status and headers in the return value.

> [!warning] `@ResponseBody` is not “only 200 or 500”
> Dumps that say so are **wrong**. Uncaught exceptions still map through `HandlerExceptionResolver`. `@ResponseStatus` on the method or exception can be 404, 204, 201, … without `ResponseEntity`.

> [!warning] `ResponseEntity.created(resource)` does not compile
> The static factory is **`created(URI location)`**. Then `.body(...)` or `.build()`. HTTP 201 is **`CREATED`**, not a dump label “SUCCESS”.

> [!warning] `@ResponseStatus` loses to `ResponseEntity`
> If you return a `ResponseEntity`, its status **wins**. Do not stack `@ResponseStatus` and expect it to override the entity.

> [!tip] Interview answer
> **`@ResponseBody` means “serialize the return value as the HTTP body.”** **`ResponseEntity` is that body plus status and headers in one object.** Use the entity (or `ProblemDetail`) when the status is not 200; `@RestController` already covers the body-only case.
