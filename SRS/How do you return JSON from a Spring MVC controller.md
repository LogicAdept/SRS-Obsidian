<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# How do you return JSON from a Spring MVC controller?

> [!abstract] Short answer
> Put **`@ResponseBody`** on the handler (or use **`@RestController`**, which is `@Controller` + type-level `@ResponseBody`) and **return a Java object**. Spring writes it with an **`HttpMessageConverter`** — typically Jackson’s JSON converter for `application/json`. Do **not** return a view name.

## Body writing, not view resolution

Spring MVC *Return Values*: `@ResponseBody` means the return value is converted through `HttpMessageConverter` implementations and written to the response. `ResponseEntity<T>` does the same for body plus status/headers.

`@ResponseBody` javadoc: as of 4.0 it can sit on the **type**; all methods inherit it. `@RestController` javadoc: a convenience meta-annotation of `@Controller` and `@ResponseBody`, so every `@RequestMapping` method gets body semantics.

```java
@RestController
public class AccountController {

    @GetMapping("/accounts/{id}")
    public Account handle(@PathVariable Long id) {
        return accounts.find(id);
    }
}
```

**Listing 1.** Conceptual pattern from Spring’s `@ResponseBody` / `@RestController` docs — POJO in, JSON out when a JSON converter is registered. Shortcut vs repeating `@ResponseBody`: [[What is the difference between Spring RestController and Controller]]. Status and headers: [[What is the difference between ResponseBody and ResponseEntity]].

```d2
direction: right
method: "Handler returns\nAccount POJO" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
conv: "HttpMessageConverter\n(Jackson JSON)" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
body: "HTTP response body\napplication/json" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

method -> conv -> body
```

**Fig. 1.** Converters, not `ViewResolver`, serialize the return value. Register/customize converters in MVC config — [[How do you configure message converters in Spring MVC]], [[What is HttpMessageConverter in Spring MVC]].

As of Spring Framework **7.0**, JSON is written with **`JacksonJsonHttpMessageConverter`** (Jackson 3 `JsonMapper`, media types `application/json` and `application/*+json`). **`MappingJackson2HttpMessageConverter`** (Jackson 2) is deprecated for removal.

A `@Controller` method that returns `String` without `@ResponseBody` is treated as a **view name**, not JSON.

> [!warning] No matching converter → 406 / conversion failure
> JSON only happens if a converter that supports the negotiated media type is registered. Missing Jackson (or a `produces` mismatch) does not silently fall back to a view.

> [!warning] `@RestController` already includes `@ResponseBody`
> Extra `@ResponseBody` on every method is redundant, not a second serialization pass.

> [!warning] `String` return with `@ResponseBody` is a raw body
> It is written as text/JSON string content, not resolved as a template name.

> [!tip] Interview answer
> **Return a POJO from `@RestController` (or `@ResponseBody` on `@Controller`).** Spring picks an `HttpMessageConverter` — Jackson for JSON — and writes the HTTP body. Without that annotation, a `String` is a view name.
