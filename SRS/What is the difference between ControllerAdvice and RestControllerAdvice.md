<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the difference between `ControllerAdvice` and `RestControllerAdvice`?

> [!abstract] Short answer
> **`@RestControllerAdvice` is `@ControllerAdvice` plus `@ResponseBody`.** Shared `@ExceptionHandler` / `@InitBinder` / `@ModelAttribute` methods still apply across controllers; with `@RestControllerAdvice` those handler **return values write to the HTTP body** (JSON via converters) instead of being treated as **view names**. By default both advise **all** controllers (`@Controller` and `@RestController`). Narrow with `basePackages`, `assignableTypes`, or `annotations`.

## Global advice, different default returns

`ControllerAdvice` javadoc: a `@Component` specialization whose `@ExceptionHandler`, `@InitBinder`, and `@ModelAttribute` methods are **shared** across `@Controller` classes. Beans are ordered (`Ordered` / `@Order`); for exceptions the **first matching** advice method wins, with root-vs-cause and priority rules.

`RestControllerAdvice` javadoc (since 4.3): shortcut combining `@ControllerAdvice` with `@ResponseBody` — exception handlers **render to the response body**. Same selectors as `@ControllerAdvice`. Default: **any** controller, including `@Controller` and `@RestController`.

```java
@RestControllerAdvice
public class ApiErrors {
    @ExceptionHandler(IllegalArgumentException.class)
    public ProblemDetail badRequest(IllegalArgumentException ex) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.BAD_REQUEST, ex.getMessage());
    }
}

@ControllerAdvice
public class HtmlErrors {
    @ExceptionHandler(IllegalArgumentException.class)
    public String formError(IllegalArgumentException ex, Model model) {
        model.addAttribute("message", ex.getMessage());
        return "error";
    }
}
```

**Listing 1.** Conceptual split: body vs view. Local vs advice: [[What does the ExceptionHandler annotation do]]. RFC 9457: [[What is ProblemDetail in Spring]]. Same `@ResponseBody` idea as [[What is the difference between Spring RestController and Controller]].

```d2
direction: down
ca: "@ControllerAdvice\nshared handlers" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
ra: "@RestControllerAdvice\n=@ControllerAdvice+@ResponseBody" {
  width: 340
  height: 80
  style.fill: "#e8f5e9"
}
view: "String → view name" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
body: "Return → HTTP body" {
  width: 200
  height: 50
  style.fill: "#fce4ec"
}

ca -> view
ra -> body
```

**Fig. 1.** Advice targeting is the same; `@ResponseBody` on the advice type changes how `@ExceptionHandler` returns are written.

Use `@ControllerAdvice` when some handlers return HTML. Use `@RestControllerAdvice` for APIs. A `@ControllerAdvice` method can still add `@ResponseBody` per method.

> [!warning] Default scope is every controller
> `@RestControllerAdvice` without selectors also wraps **`@Controller`** HTML handlers. A `String` return becomes a **body string**, not a template. Narrow with `annotations = RestController.class` (javadoc suggestion) if you only want APIs.

> [!warning] Advice order is not “undefined first bean”
> Declare **`@Order`** on overlapping `@ExceptionHandler` mappings. A cause match on higher-priority advice beats a root match on lower-priority advice.

> [!warning] Selectors are OR’d
> Multiple `basePackages` / `annotations` / `assignableTypes`: a controller matching **any** selector is advised. Runtime checks can get expensive if you pile them on.

> [!tip] Interview answer
> **Both share exception, binder, and model methods across controllers.** `@RestControllerAdvice` adds type-level `@ResponseBody` so those methods serialize to the response body. `@ControllerAdvice` is the one to use when handlers return view names. Filter with `basePackages` or `annotations = RestController.class` so you do not JSON-ify HTML controllers.
