<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #API/REST #Java/Annotations #SRS

# What is the difference between `RequestMapping` and `PutMapping`?

> [!abstract] Short answer
> **`@PutMapping` is a composed shortcut for `@RequestMapping(method = RequestMethod.PUT)`** (since 4.3). **`@RequestMapping` with an empty `method` matches all HTTP verbs**, including PUT, GET, POST. Prefer `@PutMapping` on **methods**; use class-level `@RequestMapping` for a shared URI prefix. Do **not** stack both annotations on the same method.

## PUT-only composed mapping

`PutMapping` javadoc: maps HTTP **PUT**; it **is** `@RequestMapping(method = RequestMethod.PUT)`. Same note as other shortcuts: another `@RequestMapping` (including `@GetMapping` / `@PostMapping`) on the **same method** logs a warning and **only the first** mapping is used.

`RequestMapping.method` javadoc: PUT is one of the verbs you can list. Type-level `method` is inherited by all handlers on that class.

Spring does **not** implement HTTP PUT replace-vs-PATCH semantics for you — the annotation only **matches** the request method. Resource replace vs partial update is your handler (and HTTP) design.

```java
@RestController
@RequestMapping("/persons")
class PersonController {

    @PutMapping("/{id}")
    public void replace(@PathVariable Long id, @RequestBody Person person) { /* ... */ }

    @RequestMapping(path = "/{id}", method = RequestMethod.PUT) // equivalent
    public void replaceExplicit(@PathVariable Long id, @RequestBody Person person) { /* ... */ }
}
```

**Listing 1.** Conceptual PUT mapping from Spring MVC mapping docs. GET shortcut: [[What is the difference between RequestMapping and GetMapping]]. Verb list: [[How do you map HTTP methods in Spring MVC]].

```d2
direction: down
rm: "@RequestMapping\nmethod optional" {
  width: 260
  height: 70
  style.fill: "#fff3e0"
}
pm: "@PutMapping\nmethod = PUT only" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

rm -> pm: "composed shortcut"
```

**Fig. 1.** Same mapping infrastructure; `@PutMapping` locks the verb.

> [!warning] Unrestricted `@RequestMapping` accepts PUT and everything else
> A method mapped only as `@RequestMapping("/x")` is not “REST PUT”. Clients can GET/POST it too unless you set `method` or use `@PutMapping`.

> [!warning] Same-element stacking
> `@PutMapping` + `@RequestMapping` on one method is invalid in practice — first mapping wins.

> [!warning] PUT ≠ PATCH
> `@PatchMapping` is the PATCH shortcut. Using PUT for partial updates is an API design choice, not what `@PutMapping` encodes.

> [!tip] Interview answer
> **`@PutMapping` equals `@RequestMapping(method = PUT)`.** Bare `@RequestMapping` matches every HTTP method. Put the collection path on the class; put PUT on the method with `@PutMapping`. The annotation selects the verb; it does not define replace-vs-merge.
