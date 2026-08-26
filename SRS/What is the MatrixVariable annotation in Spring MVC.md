<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the `MatrixVariable` annotation in Spring MVC?

> [!abstract] Short answer
> **`@MatrixVariable` binds RFC 3986 path-segment name/value pairs** (`/pets/42;q=11`) into a handler argument (since 3.2). The mapping **must include a `{uriVariable}`** on that segment so matching does not depend on whether the pairs are present. **`required` defaults to `true`**; **`defaultValue` forces `required=false`**. A miss raises **`MissingMatrixVariableException`** (since 5.1).

## Semicolon pairs, not query string

Pairs sit **inside a path segment**, separated by **`;`**. Several values: comma list (`color=red,green`) or repeated names (`color=red;color=green`). They are **not** `@RequestParam` query keys and **not** `{path}` template values.

`pathVar` names the URI template variable whose segment holds the pair when the same matrix name appears on two segments (`q` on `{ownerId}` vs `{petId}`). Unnamed `@MatrixVariable Map` / `MultiValueMap` collects **all** pairs; a **named** `Map` converts **one** matrix variable to a map.

```java
// GET /pets/42;q=11;r=22
@GetMapping("/pets/{petId}")
public void findPet(@PathVariable String petId, @MatrixVariable int q) {
    // petId == "42", q == 11
}
```

**Listing 1.** Conceptual Framework example: `{petId}` **masks** `;q=…` so the mapping still matches. Path vs query: [[What is the difference between RequestParam and PathVariable]]. Headers: [[What is the RequestHeader annotation in Spring MVC]]. Path matching config: [[What is WebMvcConfigurer in Spring MVC]].

```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {

    @Override
    public void configurePathMatch(PathMatchConfigurer configurer) {
        UrlPathHelper helper = new UrlPathHelper();
        helper.setRemoveSemicolonContent(false);
        configurer.setUrlPathHelper(helper);
    }
}
```

**Listing 2.** Conceptual (String/`AntPathMatcher` path): `UrlPathHelper` **defaults to stripping `;…`**, so matrix variables never reach the binder. MVC docs: set **`removeSemicolonContent=false`**. That helper is **deprecated for runtime** in Framework 7; default matching since 6.0 is **`PathPatternParser`** with **`PathContainer.Options.HTTP_PATH`**, which **parses path parameters**. `setPatternParser(null)` falls back to String matching and the strip-default.

```d2
direction: down
url: "/owners/42;q=11/pets/21;q=22" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
mask: "@GetMapping(\"/owners/{ownerId}/pets/{petId}\")" {
  width: 360
  height: 50
  style.fill: "#fff3e0"
}
mv: "@MatrixVariable(pathVar=\"petId\") q → 22" {
  width: 320
  height: 50
  style.fill: "#e8f5e9"
}

url -> mask
mask -> mv
```

**Fig. 1.** Template variables absorb the segment; `pathVar` picks which segment’s `q`.

> [!warning] Mapping without `{…}`
> `/cars/ford;year=2020` against a literal `/cars/ford` does not match. Put **`{make}`** (or similar) on the segment that may carry matrix pairs.

> [!warning] Semicolons stripped by default on the old matcher
> `UrlPathHelper.removeSemicolonContent` defaults to **`true`** (`jsessionid` is always removed). Dumps that only show `@MatrixVariable` without Path Matching leave you with empty/missing variables.

> [!warning] Required by default
> Absent pair → **`MissingMatrixVariableException`**, not a quiet `null`, unless `required=false` or `defaultValue`.

> [!tip] Interview answer
> **`@MatrixVariable` reads `segment;name=value` pairs from the path, not the query string.** The `@GetMapping` path still needs `{id}` so order and presence of those pairs do not break matching. On the AntPathMatcher path you must stop `UrlPathHelper` from stripping semicolons; `pathVar` disambiguates the same name on two segments.
