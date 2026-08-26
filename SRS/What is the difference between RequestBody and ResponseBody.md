<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the difference between `RequestBody` and `ResponseBody`?

> [!abstract] Short answer
> **`@RequestBody`** binds a **handler parameter** to the **HTTP request body** through an **`HttpMessageConverter`** (typically JSON → object). **`@ResponseBody`** writes the **method return value** to the **HTTP response body** through converters and **skips view resolution**. They are opposite directions on the same converter pipeline. **`@RestController`** applies `@ResponseBody` to **every** method; it does **not** imply `@RequestBody` on parameters.

## In vs out

`RequestBody` javadoc (since 3.0): the request body is passed through an `HttpMessageConverter` according to **`Content-Type`**. Optional **`@Valid`** runs Bean Validation on the argument. **`required`** defaults to **`true`** (empty body → exception); set **`false`** to allow `null` (since 3.2).

`ResponseBody` javadoc: the return value is bound to the **web response body**. As of 4.0 it may sit on the **type** and is inherited — that is what `@RestController` does.

Classic HTML forms use **request parameters** / `@ModelAttribute`, not `@RequestBody`. JSON APIs use `@RequestBody` on POST/PUT/PATCH (and sometimes GET with a body, which HTTP allows but caches dislike).

```java
@PostMapping("/accounts")
@ResponseBody
public Account create(@Valid @RequestBody Account input) {
    return accounts.save(input);
}
```

**Listing 1.** Conceptual pair: converters read the body in and write the return value out. Status/headers: [[What is the difference between ResponseBody and ResponseEntity]]. Class-level shortcut: [[What is the difference between Spring RestController and Controller]]. SPI: [[What is HttpMessageConverter in Spring MVC]].

```d2
direction: right
req: "HTTP request body\nContent-Type" {
  width: 220
  height: 70
  style.fill: "#e3f2fd"
}
in: "@RequestBody\nread()" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
out: "@ResponseBody\nwrite()" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
res: "HTTP response body\nAccept / produces" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}

req -> in
out -> res
```

**Fig. 1.** Same converter list; `@RequestBody` is input, `@ResponseBody` is output. Form objects: [[How does form binding work in Spring MVC]].

> [!warning] `@RestController` is only the output half
> Parameters are still primitives/`@RequestParam`/`@PathVariable` unless you add **`@RequestBody`**. Forgetting it on a JSON POST leaves the body unread.

> [!warning] Forms vs JSON
> `application/x-www-form-urlencoded` is **`@ModelAttribute`** / servlet parameters. `@RequestBody` on a form POST often fails conversion or binds nothing useful.

> [!warning] Not `ResponseEntity`
> `@ResponseBody` does not set status/headers. Use **`ResponseEntity`** (or `@ResponseStatus`) when you need more than the body.

> [!tip] Interview answer
> **`@RequestBody` deserializes the request entity; `@ResponseBody` serializes the return value.** Both use `HttpMessageConverter`. `@RestController` only adds `@ResponseBody` at type level — you still annotate JSON inputs with `@RequestBody`.
