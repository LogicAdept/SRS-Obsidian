<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the `ResponseStatus` annotation in Spring MVC?

> [!abstract] Short answer
> **`@ResponseStatus` declares the HTTP status (`code` / `value`) and optional `reason` for a handler method, a controller class, or an exception type.** Default `code` is **`INTERNAL_SERVER_ERROR`** — change it. It does **not** override **`ResponseEntity`** or a **`"redirect:"`** view. On an **exception class**, or whenever **`reason` is non-empty**, Spring calls **`HttpServletResponse.sendError`**, which finishes the response and typically yields a **container HTML error page**.

## Method, type, or exception

On a `@RequestMapping` method, the status is applied when that method runs (`setStatus` unless `reason` is set). A class-level annotation is **inherited** by `@RequestMapping` and `@ExceptionHandler` methods in the class and subclasses unless a method declares its own.

On an **exception type**, **`ResponseStatusExceptionResolver`** (enabled by default on `DispatcherServlet`) maps the throw to that status. As of 4.2 it walks **causes**; as of 4.2.2 it honors composed-annotation overrides; as of 5.0 it also handles **`ResponseStatusException`**. `reason` can be a **`MessageSource`** code via `MessageSourceAware`.

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException { }
```

**Listing 1.** Conceptual: an uncaught throw becomes 404 without a local `@ExceptionHandler`. Resolvers: [[What is HandlerExceptionResolver in Spring MVC]]. Handler methods: [[What does the ExceptionHandler annotation do]]. REST bodies: [[What is ProblemDetail in Spring]].

```java
@GetMapping("/gone")
@ResponseStatus(HttpStatus.NO_CONTENT)
public void gone() { }
```

**Listing 2.** Conceptual: method-level status with no body. `void` plus `@ResponseStatus` counts as a fully handled response.

```d2
direction: down
throw: "throw @ResponseStatus exception" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
ehr: "ExceptionHandlerExceptionResolver\n(@ExceptionHandler first)" {
  width: 320
  height: 55
  style.fill: "#fff3e0"
}
rsr: "ResponseStatusExceptionResolver\nsendError(code [, reason])" {
  width: 320
  height: 55
  style.fill: "#e8f5e9"
}

throw -> ehr
ehr -> rsr
```

**Fig. 1.** Default resolver order: if an `@ExceptionHandler` handles the type, the annotation-on-exception path does not run.

> [!warning] `reason` is hostile to REST
> A non-empty `reason` uses **`sendError(int, String)`**. The Servlet container usually writes **HTML**. Prefer **`ResponseEntity`** (or RFC 9457 `ProblemDetail`) and skip `@ResponseStatus` on APIs that must return JSON.

> [!warning] Default is 500
> Forgetting `code` / `value` leaves **`INTERNAL_SERVER_ERROR`**. That is rarely what you meant on a success handler.

> [!warning] Status sources that win
> `@ResponseStatus` does **not** override a `ResponseEntity` status or a `redirect:` view. Put the status on the `ResponseEntity` (or the redirect) instead of stacking annotations.

> [!tip] Interview answer
> **`@ResponseStatus` stamps an HTTP code on a method, a controller type, or an exception class.** Exception mapping is `ResponseStatusExceptionResolver`. A `reason` (or annotation on the exception) goes through `sendError` and a container error page — fine for HTML, a trap for REST. `@ExceptionHandler` runs first if it matches.
