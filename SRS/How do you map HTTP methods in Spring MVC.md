<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# How do you map HTTP methods in Spring MVC?

> [!abstract] Short answer
> Set **`@RequestMapping(method = …)`** to `RequestMethod` values (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`, plus `HEAD`, `OPTIONS`, `TRACE`), or use the composed shortcuts **`@GetMapping`**, **`@PostMapping`**, **`@PutMapping`**, **`@DeleteMapping`**, **`@PatchMapping`**. A bare `@RequestMapping` with **empty `method`** matches **all** HTTP methods. Class-level mappings **narrow** method-level ones (shared path and optional method restriction).

## `@RequestMapping` vs HTTP shortcuts

Spring MVC *Mapping Requests*: `@RequestMapping` matches by URL, HTTP method, params, headers, and media types. Put a shared path (and optional method restriction) on the **class**; narrow with method-level annotations.

The HTTP-specific annotations are composed `@RequestMapping` variants. Spring’s docs prefer them on methods because most handlers should bind to **one** verb; keep `@RequestMapping` at type level for the shared prefix.

`@RequestMapping.method` javadoc lists: GET, POST, HEAD, OPTIONS, PUT, PATCH, DELETE, TRACE. Type-level `method` is **inherited** — every handler on that class is restricted unless a more specific mapping applies.

```java
@RestController
@RequestMapping("/persons")
class PersonController {

    @GetMapping("/{id}")
    public Person getPerson(@PathVariable Long id) { /* ... */ }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public void add(@RequestBody Person person) { /* ... */ }

    @RequestMapping(path = "/{id}", method = RequestMethod.PUT)
    public void replace(@PathVariable Long id, @RequestBody Person person) { /* ... */ }
}
```

**Listing 1.** Conceptual type + method mappings from Spring Framework reference. Shortcuts vs raw mapping: [[What is the difference between RequestMapping and GetMapping]], [[What is the difference between RequestMapping and PutMapping]].

```d2
direction: down
cls: "@RequestMapping(\"/persons\")\nclass-level prefix" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
get: "@GetMapping(\"/{id}\")\nGET only" {
  width: 240
  height: 60
  style.fill: "#e8f5e9"
}
post: "@PostMapping\nPOST /persons" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
bare: "@RequestMapping without method\nmatches every HTTP verb" {
  width: 320
  height: 70
  style.fill: "#ffebee"
}

cls -> get
cls -> post
bare
```

**Fig. 1.** Class path combines with method path; omitting `method` is not GET-only. How the servlet picks the handler: [[How does DispatcherServlet choose which handler method to invoke]].

HTTP verb *meanings* (GET read, POST create, PUT replace, PATCH partial, DELETE remove) come from HTTP, not from Spring annotations. Spring only **matches** the request method you declare.

> [!warning] No `method` means every verb
> `@RequestMapping("/home")` on a method accepts GET, POST, PUT, … unless you restrict it. Prefer `@GetMapping` when you mean GET.

> [!warning] Do not stack mapping annotations on one element
> Two `@RequestMapping` (including `@GetMapping` + `@RequestMapping`) on the **same** method or class: a warning is logged and **only the first** mapping is used.

> [!warning] Class-level `method` applies to all handlers
> `@RequestMapping(method = RequestMethod.GET)` on the class makes every method GET-only unless you restructure mappings.

> [!tip] Interview answer
> **Map verbs with `@RequestMapping(method = RequestMethod.…)` or `@GetMapping` / `@PostMapping` / `@PutMapping` / `@PatchMapping` / `@DeleteMapping`.** Class-level `@RequestMapping` is the shared URI prefix. An unrestricted `@RequestMapping` matches all HTTP methods — that is why the shortcuts exist.
