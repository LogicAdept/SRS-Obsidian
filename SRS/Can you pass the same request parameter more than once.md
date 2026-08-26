<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #API/REST #Java/Annotations #SRS

# Can you pass the same request parameter more than once?

> [!abstract] Short answer
> **Yes.** HTTP and the Servlet parameter map allow repeated names (`name=a&name=b`). In Spring MVC bind them with **`@RequestParam` on an array or `List`**. A **single `String`** does not collect every occurrence. For **all** parameters at once, use **`@RequestParam MultiValueMap<String, String>`** with **no** parameter name.

## Repeated keys, collection argument

Spring MVC *`@RequestParam`*: “Declaring the argument type as an **array or list** allows for resolving **multiple parameter values for the same parameter name**.” In MVC, “request parameters” are Servlet **`parameters`**: query string **and** form fields (and multipart parts). WebFlux `@RequestParam` is **query only**.

`required` defaults to **`true`**. `defaultValue` forces `required=false`.

```java
@GetMapping("/search")
public String search(@RequestParam("name") List<String> names) {
    return names.toString();
}
```

**Listing 1.** Conceptual: `?name=Ranga&name=Ravi&name=Sathish` binds three strings. `String[]` works the same. Query vs path: [[What is the difference between RequestParam and PathVariable]]. Forms: [[How does form binding work in Spring MVC]].

```java
@PostMapping(path = "/process", consumes = MediaType.APPLICATION_FORM_URLENCODED_VALUE)
public String processForm(@RequestParam MultiValueMap<String, String> params) {
    return params.get("name").toString();
}
```

**Listing 2.** Conceptual Framework example: unnamed `@RequestParam` on `MultiValueMap` receives **every** parameter, including repeats. `Map<String, String>` in the same unnamed form keeps **one** string per key.

```d2
direction: down
q: "name=a&name=b&name=c" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
list: "@RequestParam List / array" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
one: "@RequestParam String" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}

q -> list: "all values"
q -> one: "not a collection"
```

**Fig. 1.** Same Servlet map; the **Java type** decides whether repeats survive. JSON body is **`@RequestBody`**, not request parameters: [[What is the difference between RequestBody and ResponseBody]].

Simple types without `@RequestParam` are still treated as request params (`BeanUtils.isSimpleProperty`) if no other resolver claims them.

> [!warning] `String` is not “all values”
> Use **`List` / array**. A scalar `@RequestParam String name` does not give you the list from the dump’s three `name=` keys.

> [!warning] Unnamed `Map<String, String>` drops extras
> Official unnamed-map support is `Map<String, String>` **or** `MultiValueMap<String, String>`. Only the **multi** map preserves several values per key. A **named** `@RequestParam("q") Map<…>` means convert **that one** parameter’s value **to** a `Map`, not “all query keys”.

> [!warning] MVC vs WebFlux
> Repeats in a **form body** bind in MVC via the Servlet parameter map. In WebFlux the same annotation does **not** read form fields as `@RequestParam`.

> [!tip] Interview answer
> **Yes — repeat the query or form name.** Bind with `@RequestParam List<String>` or `String[]`. `MultiValueMap` without a name captures every parameter. A single `String` is the wrong type for that question.
