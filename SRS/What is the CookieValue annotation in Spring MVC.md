<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the `CookieValue` annotation in Spring MVC?

> [!abstract] Short answer
> **`@CookieValue` binds one HTTP cookie to a handler argument** (since 3.0). The parameter may be a Servlet **`Cookie`** or a **value type** (`String`, `int`, … — conversion applies). **`required` defaults to `true`**. **`defaultValue` forces `required=false`**. A missing required cookie raises **`MissingRequestCookieException`** (since 5.1).

## Cookie header, not query string

Unlike `@RequestParam` (Servlet parameter map) or `@PathVariable` (URI template), this annotation reads the **`Cookie`** request header. `name` / `value` (alias since 4.2) is the cookie name. Official demo: `@CookieValue("JSESSIONID") String cookie`.

There is **no** unnamed-`Map` “all cookies” form on `@CookieValue`. That pattern exists on `@RequestHeader` (`Map` / `MultiValueMap` / `HttpHeaders`).

```java
@GetMapping("/demo")
public void handle(@CookieValue("JSESSIONID") String cookie) {
    // cookie is the JSESSIONID value
}
```

**Listing 1.** Conceptual Framework example: bind one named cookie as `String`. Query vs path: [[What is the difference between RequestParam and PathVariable]]. Headers: [[What is the RequestHeader annotation in Spring MVC]]. Locale cookies are a different SPI: [[What is LocaleResolver in Spring MVC]].

```java
@GetMapping("/prefs")
public String prefs(
        @CookieValue(name = "theme", defaultValue = "light") String theme,
        @CookieValue(name = "sid", required = false) Cookie sessionCookie) {
    return theme;
}
```

**Listing 2.** Conceptual: `defaultValue` makes the cookie optional. `Cookie` (not `String`) exposes name/value/attributes. `required=false` yields `null` when the cookie is absent.

```d2
direction: down
hdr: "Cookie: JSESSIONID=415A…; theme=dark" {
  width: 340
  height: 50
  style.fill: "#e3f2fd"
}
ann: "@CookieValue(\"theme\")" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
arg: "String theme = \"dark\"" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}

hdr -> ann
ann -> arg
```

**Fig. 1.** One annotation, one cookie name. Other cookies on the same header are ignored unless you declare more parameters.

> [!warning] Required by default
> A missing cookie is not a silent `null`. Without `required=false` or `defaultValue`, Spring throws **`MissingRequestCookieException`**. Same default as `@RequestParam` / `@RequestHeader`.

> [!warning] Not a request parameter
> `@RequestParam("JSESSIONID")` does **not** read the session cookie. Query/form keys and cookies are different maps.

> [!warning] No all-cookies `Map`
> `@CookieValue Map<…>` is **not** documented as “every cookie”. Use `@RequestHeader` maps for headers, or `HttpServletRequest.getCookies()` if you need the raw array.

> [!tip] Interview answer
> **`@CookieValue` pulls one cookie off the request into a controller argument — `Cookie` or a converted value.** It is required unless you set `required=false` or `defaultValue`. Missing required cookies fail with `MissingRequestCookieException`, not a null `String`.
