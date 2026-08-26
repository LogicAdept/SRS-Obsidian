<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What does the `ExceptionHandler` annotation do?

> [!abstract] Short answer
> **`@ExceptionHandler` marks a method that handles exceptions thrown from controller handler methods.** Declare it on a `@Controller` (local to that class) or on **`@ControllerAdvice`** (cross-controller). Support is **`HandlerExceptionResolver`** infrastructure on `DispatcherServlet`. Prefer a specific exception type as a method argument; you can also list types on the annotation.

## Local vs advice, then matching

Spring MVC *Exceptions*: `@Controller` and `@ControllerAdvice` may declare `@ExceptionHandler` methods. Matching can be the thrown type or a **nested cause** (as of 5.3, any cause depth). When several methods match, **`ExceptionDepthComparator`** prefers a closer (root) match **within the same class**. Across multiple `@ControllerAdvice` beans, **order** matters: a cause match on a **higher-priority** advice beats a root match on a lower-priority one.

The annotation’s `value` / `exception` narrows types; if empty, types come from the method arguments (javadoc, `exception` since 6.2).

```java
@Controller
public class SimpleController {

    @ExceptionHandler(IOException.class)
    public ResponseEntity<String> handle(IOException ex) {
        return ResponseEntity.internalServerError().body("Could not read file storage");
    }
}
```

**Listing 1.** Conceptual local handler from Spring Framework reference. Global handlers: [[What is the difference between ControllerAdvice and RestControllerAdvice]]. RFC 9457 bodies: [[What is ProblemDetail in Spring]].

```d2
direction: down
ctrl: "Controller method\nthrows IOException" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
res: "HandlerExceptionResolver\n(@ExceptionHandler)" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
out: "ResponseEntity / view /\nProblemDetail" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

ctrl -> res -> out
```

**Fig. 1.** Exception handling is a `DispatcherServlet` resolver step, not a try/catch inside every handler. Related SPI: [[What is HandlerExceptionResolver in Spring MVC]].

Arguments include the exception, `HandlerMethod`, servlet request/response, `WebRequest`, `Locale`, **`Model` (always empty)**, `RedirectAttributes`. Returns include `ResponseEntity`, `@ResponseBody`, view `String`, `ProblemDetail`, `void`.

Same exception type **twice** in one class is allowed when **`produces`** differs (JSON vs HTML via content negotiation, since 6.2). A method may **rethrow** the original exception to skip itself and continue the resolver chain.

You may combine `@ExceptionHandler` with `@ResponseStatus`.

> [!warning] `Model` is supported — and always empty
> Dumps that forbid `Model` are wrong. The provided model is **not** pre-filled with the failed request’s attributes.

> [!warning] Root vs cause argument can surprise you
> A handler declared for `IOException` may receive a **wrapper** `IOException` when the match was a nested cause. Prefer a **specific** exception parameter.

> [!warning] Advice order is not “first bean in the context”
> Do not assume undefined discovery order. Set `@ControllerAdvice` **order** for overlapping mappings.

> [!tip] Interview answer
> **`@ExceptionHandler` is a controller (or `@ControllerAdvice`) method that turns a thrown exception into a response.** Local on the controller, or global on advice. Matching uses the exception type (and nested causes); MVC runs it through `HandlerExceptionResolver`.
