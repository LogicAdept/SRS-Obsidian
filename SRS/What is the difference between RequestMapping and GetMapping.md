<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the difference between `RequestMapping` and `GetMapping`?

> [!abstract] Short answer
> **`@GetMapping` is a composed shortcut for `@RequestMapping(method = RequestMethod.GET)`** (since 4.3). **`@RequestMapping` without `method` matches every HTTP verb.** Prefer `@GetMapping` on **methods**; keep `@RequestMapping` on the **class** for a shared path. Do **not** put both on the **same** method.

## Composed GET vs general mapping

`GetMapping` javadoc: maps HTTP **GET**; it **is** `@RequestMapping(method = RequestMethod.GET)`.

`RequestMapping` javadoc: use it at **class and method** level. For methods, apps usually prefer HTTP-specific variants. Empty `method` **narrows nothing** — GET, POST, PUT, … all match.

Type-level `@RequestMapping("/home")` **combines** with method-level `@GetMapping("/welcome")` → GET `/home/welcome`. Same combination works with `@RequestMapping(method = GET)` on the method.

```java
@RestController
@RequestMapping("/home")          // shared prefix, all methods inherit the path
class HomeController {

    @GetMapping("/welcome")       // GET only
    public String welcome() { return "ok"; }

    @RequestMapping(path = "/legacy", method = RequestMethod.GET) // equivalent GET
    public String legacy() { return "ok"; }
}
```

**Listing 1.** Conceptual class + method mappings from Spring MVC mapping docs. Other verbs: [[How do you map HTTP methods in Spring MVC]]. PUT shortcut: [[What is the difference between RequestMapping and PutMapping]].

```d2
direction: down
rm: "@RequestMapping\noptional method[]" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
gm: "@GetMapping\nmethod = GET only" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
all: "method empty →\nall HTTP verbs" {
  width: 240
  height: 70
  style.fill: "#ffebee"
}

rm -> gm: "composed shortcut"
rm -> all: "if method omitted"
```

**Fig. 1.** `@GetMapping` is not a different mapping engine — it is GET-locked `@RequestMapping`.

> [!warning] Two mapping annotations on one method
> `@GetMapping` **and** `@RequestMapping` on the **same** method: Spring logs a warning and uses **only the first**. The dump listing is **two equivalent styles**, not both at once.

> [!warning] Class-level `@GetMapping` is unusual
> Shortcuts exist for methods. A type-level `@RequestMapping` still supplies the URI prefix for `@GetMapping` methods.

> [!warning] GET mapping is not “safe CRUD”
> `@GetMapping` only restricts the **HTTP method**. Idempotence/safety are HTTP semantics you still have to honor in the handler.

> [!tip] Interview answer
> **`@GetMapping` equals `@RequestMapping(method = GET)`.** Bare `@RequestMapping` accepts every verb — that is the interview trap. Put the path prefix on the class with `@RequestMapping`, and GET handlers with `@GetMapping`.
