<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the `RequestHeader` annotation in Spring MVC?

> [!abstract] Short answer
> **`@RequestHeader` binds an HTTP request header to a handler argument** (MVC and WebFlux, since 3.0). A **named** header converts to `String` or another type. On **`Map<String, String>`**, **`MultiValueMap<String, String>`**, or **`HttpHeaders`**, the argument is filled with **every** header. **`required` defaults to `true`**; **`defaultValue` forces `required=false`**. A missing required header raises **`MissingRequestHeaderException`** (since 5.1).

## One header or the whole map

`name` / `value` (alias since 4.2) is the header name. Non-`String` targets go through type conversion. A **comma-separated** header such as `Accept` can bind to `String`, `String[]`, or `List<String>` (and other converted element types).

Unlike `@RequestParam`, a `Map` / `MultiValueMap` / `HttpHeaders` parameter here always means **all headers**, not “convert one named header into a map”.

```java
@GetMapping("/demo")
public void handle(
        @RequestHeader("Accept-Encoding") String encoding,
        @RequestHeader("Keep-Alive") long keepAlive) {
    // ...
}
```

**Listing 1.** Conceptual Framework example: two named headers; `Keep-Alive` converts to `long`. Cookies: [[What is the CookieValue annotation in Spring MVC]]. Query vs path: [[What is the difference between RequestParam and PathVariable]]. Locale from `Accept-Language` is a resolver, not this annotation: [[What is LocaleResolver in Spring MVC]].

```java
@GetMapping("/headers")
public int count(@RequestHeader HttpHeaders headers,
                 @RequestHeader(name = "X-Request-Id", required = false) String requestId) {
    return headers.size();
}
```

**Listing 2.** Conceptual: `HttpHeaders` (or unnamed `Map` / `MultiValueMap`) receives the full header set. `required=false` yields `null` when that one header is absent.

```d2
direction: down
req: "Accept-Encoding: gzip\nKeep-Alive: 300" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
named: "@RequestHeader(\"Keep-Alive\")\nlong keepAlive" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
all: "@RequestHeader HttpHeaders\nevery name → values" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}

req -> named
req -> all
```

**Fig. 1.** Named parameter = one header. `Map` / `MultiValueMap` / `HttpHeaders` = the whole header map.

> [!warning] Required by default
> A missing named header is not a silent `null`. Without `required=false` or `defaultValue`, Spring throws **`MissingRequestHeaderException`**.

> [!warning] `Cookie` is not a header argument
> The `Cookie` request header is still a header, but session/theme cookies belong on **`@CookieValue`**. `@RequestHeader("Cookie")` gives the raw header string, not a parsed `Cookie` object.

> [!warning] Repeated names
> Use `MultiValueMap` or `HttpHeaders` when a header can appear more than once. A plain `Map<String, String>` keeps **one** string per name.

> [!tip] Interview answer
> **`@RequestHeader` injects request headers into the controller: one named header, or all of them on `HttpHeaders` / a map.** Required by default; missing ones fail with `MissingRequestHeaderException`. Comma-separated values can bind to arrays and lists.
