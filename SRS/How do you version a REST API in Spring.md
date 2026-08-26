<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Spring/Boot #API/REST #SRS

# How do you version a REST API in Spring?

> [!abstract] Short answer
> As of Framework **7.0**, enable **API versioning** on **`WebMvcConfigurer.configureApiVersioning`** (or Boot **`spring.mvc.apiversion.*`**): resolve the version from a **header**, **query param**, **path segment**, or **media-type parameter**. Map handlers with **`@RequestMapping` / `@GetMapping` `version`**: **`"1.2"`** matches that version only; **`"1.2+"`** is a **baseline** (this and later) until a higher mapping takes over. Unknown versions → **`InvalidApiVersionException` (400)**. Missing version → **`MissingApiVersionException` (400)** unless you set a **default** (then version is optional).

## Resolve, then match `version`

Versioning is **off** until you add at least one **`ApiVersionResolver`**. Built-ins: `useRequestHeader`, `useQueryParam`, `usePathSegment(index)`, `useMediaTypeParameter(mediaType, paramName)`, or a custom resolver. Default parser is **`SemanticApiVersionParser`**. Supported versions are **detected from mappings** unless you `detectSupportedVersions(false)` and `addSupportedVersions(...)`.

Path segment: the index is 0 for `"/{version}/..."`, 1 for `"/api/{version}/..."`. The segment **must** be a URI variable. **`usePathSegment` never returns null**, so it does not fall through to other resolvers.

Deprecation: **`StandardApiVersionDeprecationHandler`** can send **Deprecation**, **Sunset**, and **Link** (RFC 9745 / RFC 8594).

Hard-coded `/v1/orders` paths still work as **plain URL prefixes** without this SPI; they are not the same as `version` matching.

```java
@Configuration
public class WebConfiguration implements WebMvcConfigurer {
    @Override
    public void configureApiVersioning(ApiVersionConfigurer configurer) {
        configurer.useRequestHeader("API-Version");
    }
}

@RestController
@RequestMapping("/accounts")
class AccountController {

    @GetMapping(path = "/{id}", version = "1.2+")
    Account v12(@PathVariable long id) { /* compatible shape */ }

    @GetMapping(path = "/{id}", version = "2.0")
    AccountV2 v20(@PathVariable long id) { /* breaking shape */ }
}
```

**Listing 1.** Conceptual Framework 7: one path, two methods. Configurer: [[What is WebMvcConfigurer in Spring MVC]]. Matching: [[How does DispatcherServlet choose which handler method to invoke]]. Mapping surface: [[How do you map HTTP methods in Spring MVC]].

```properties
spring.mvc.apiversion.default=1.0.0
spring.mvc.apiversion.use.header=X-Version
```

**Listing 2.** Boot equivalent. Multiple strategies (header **and** query) should be ordered in **`configureApiVersioning`**, not mixed properties alone.

```d2
direction: down
req: "Request\nheader / query / path / media param" {
  width: 320
  height: 50
  style.fill: "#e3f2fd"
}
cfg: "ApiVersionConfigurer" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
map: "@GetMapping(version = \"1.2+\")" {
  width: 280
  height: 45
  style.fill: "#e8f5e9"
}

req -> cfg
cfg -> map
```

**Fig. 1.** Resolvers extract a version; `RequestMappingInfo` then selects the handler. 400s for missing/unknown versions are MVC exceptions (RFC 9457 if problem details are on): [[What is ProblemDetail in Spring]].

> [!warning] Resolver required
> `@GetMapping(version = "1.2")` does **nothing** until you configure how the request carries a version. Boot: set **`spring.mvc.apiversion.use.*`** or implement the configurer.

> [!warning] Path segment wins exclusively
> `usePathSegment` **cannot yield** to a header resolver. Prefer one strategy, or a custom `ApiVersionResolver`.

> [!warning] `1.2+` is not “forever”
> A later mapping with a **higher fixed version** on the **same path** takes precedence for those requests. That is how you introduce a breaking change without renaming URLs.

> [!tip] Interview answer
> Framework **7**: configure **`configureApiVersioning`** (header is the docs’ example), then **`version = "1.2"`** or **`"1.2+"`** on the mapping. Unknown → 400 `InvalidApiVersionException`. Older apps still prefix `/v1` in the path; that is just URL design, not this SPI.
