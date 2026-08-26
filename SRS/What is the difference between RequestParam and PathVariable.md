<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #API/REST #SRS

# What is the difference between `RequestParam` and `PathVariable`?

> [!abstract] Short answer
> **`@PathVariable` binds a URI template segment** (`/users/{id}` → `/users/101`). **`@RequestParam` binds a Servlet request parameter** (query string, and in MVC also form fields / multipart parts): `/users?id=101`. Both default **`required = true`**. Unnamed **`Map<String, String>`** means “all of that source”: all path variables vs all request parameters (`MultiValueMap` if you need repeated query keys).

## Path vs parameter map

`PathVariable` javadoc (since 3.0): bind a method argument to a **URI template variable** on `@RequestMapping` methods. `name` / `required` since 4.3.3. `required=false` is for cases like a `@ModelAttribute` method shared across mappings that **may not** include that variable — not for “optional resource ids” on a `{id}` mapping (the segment is either in the match or the method is not chosen).

`RequestParam` javadoc: MVC “request parameters” are the Servlet **`parameters`** map (query + form + multipart parts). WebFlux `@RequestParam` is **query only**. `required` defaults to **`true`**; `defaultValue` sets `required=false`. There is **no** `defaultValue` on `@PathVariable`.

```java
@GetMapping("/users/{id}")
public User byId(@PathVariable Long id) { … }

@GetMapping("/users")
public List<User> search(@RequestParam("q") String q) { … }
```

**Listing 1.** Conceptual: identity in the path, filter in the query. Repeats: [[Can you pass the same request parameter more than once]]. Forms: [[How does form binding work in Spring MVC]]. JSON body is neither: [[What is the difference between RequestBody and ResponseBody]].

```java
public String allVars(@PathVariable Map<String, String> path,
                      @RequestParam MultiValueMap<String, String> query) { … }
```

**Listing 2.** Conceptual: unnamed `@PathVariable Map` = every `{…}` in the mapping. Unnamed `@RequestParam MultiValueMap` = every request parameter.

```d2
direction: down
url: "/users/101?active=true" {
  width: 280
  height: 50
  style.fill: "#e3f2fd"
}
pv: "@PathVariable\n101" {
  width: 200
  height: 50
  style.fill: "#e8f5e9"
}
rp: "@RequestParam\nactive=true" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}

url -> pv
url -> rp
```

**Fig. 1.** Same HTTP request, two binders. Simple types without annotations still resolve as `@RequestParam` if no other resolver claims them.

REST style: path segments for the **resource**; query params for **filters, sort, pagination**. Spring does not enforce that; it only binds what you annotate.

> [!warning] Both are required by default
> Dumps that say `@RequestParam` is optional by default are **wrong** for current Spring (Framework 7 javadoc: `required` defaults to **`true`**). Same for `@PathVariable`. Use `required=false`, `Optional`, or (params only) `defaultValue`.

> [!warning] `{id}` in the mapping is not a query param
> `/users/101` does not populate `@RequestParam("id")`. `/users?id=101` does not populate `@PathVariable("id")` unless the mapping also has `{id}`.

> [!warning] Named `Map` is not “all keys”
> `@RequestParam("q") Map<…>` converts **one** parameter named `q` **to** a `Map`. All-params / all-path-vars maps omit the name.

> [!tip] Interview answer
> **`@PathVariable` is a `{template}` piece of the URL. `@RequestParam` is `?key=` (and in MVC, form fields too).** Both default to required. Use a `Map` without a name to slurp all path variables or all request parameters.
