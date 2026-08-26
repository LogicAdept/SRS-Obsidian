<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #API/REST #SRS

# What do common Spring Web MVC annotations do?

> [!abstract] Short answer
> They declare **controllers**, **URL/HTTP mappings**, **how arguments bind**, and **how the return value is written**. Core set: **`@Controller` / `@RestController`**, **`@RequestMapping`** (and `@GetMapping` …), **`@PathVariable` / `@RequestParam` / `@RequestBody`**, **`@ResponseBody`**, **`@ExceptionHandler` / `@ControllerAdvice`**. They live in **`org.springframework.web.bind.annotation`**. `@RequestMapping.method` takes **`RequestMethod`**, not a `String`. **`ResponseEntity` is a type**, not an annotation.

## Stereotype, mapping, bind, write, advise

`RequestMappingHandlerMapping` only treats **type-level `@Controller`** as a handler. `@RestController` = `@Controller` + type-level `@ResponseBody` (converters write the body; **not** “always JSON”).

| Annotation | Role |
| --- | --- |
| `@RequestMapping` | Path, HTTP method, params, headers, consumes/produces, (7.0) `version`. Empty `method` → **all** verbs. |
| `@GetMapping` … `@PatchMapping` | Composed mappings for one verb. |
| `@PathVariable` | URI template `{id}`. `required` default **true**. |
| `@RequestParam` | Servlet **parameter map** (query + form + multipart). `required` default **true**; `defaultValue` implies not required. Unnamed `Map`/`MultiValueMap` = **all** params. |
| `@RequestHeader` / `@CookieValue` / `@MatrixVariable` | Header, cookie, path matrix vars. `required` default **true**. |
| `@RequestBody` | Body → object via `HttpMessageConverter` (`Content-Type`). |
| `@ResponseBody` | Return value → body (skips view). |
| `@ModelAttribute` | Command object / model attribute + binding. |
| `@InitBinder` | Per-controller `WebDataBinder`. |
| `@ExceptionHandler` | Handle exceptions from handlers. |
| `@ControllerAdvice` / `@RestControllerAdvice` | Shared `@ExceptionHandler` / `@InitBinder` / `@ModelAttribute`. Rest variant adds `@ResponseBody`. |
| `@ResponseStatus` | HTTP status (and optional `reason`). |
| `@CrossOrigin` | CORS on a type or method. |
| `@SessionAttributes` / `@SessionAttribute` | Type-level conversational model vs **one** session attribute parameter. |

Not MVC: **`@ContextConfiguration`** (tests), **`@Qualifier`** (injection).

```java
@RestController
@RequestMapping("/accounts")
class AccountApi {

    @GetMapping("/{id}")
    Account one(@PathVariable long id) { … }

    @GetMapping
    List<Account> search(@RequestParam String q) { … }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    Account create(@RequestBody Account body) { … }
}
```

**Listing 1.** Conceptual: mapping + path + query + JSON body. Verbs: [[How do you map HTTP methods in Spring MVC]]. Path vs query: [[What is the difference between RequestParam and PathVariable]]. Body directions: [[What is the difference between RequestBody and ResponseBody]]. Status wrapper: [[What is the difference between ResponseBody and ResponseEntity]]. Advice: [[What does the ExceptionHandler annotation do]].

```d2
direction: down
ctrl: "@Controller / @RestController" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
map: "@RequestMapping / @GetMapping" {
  width: 280
  height: 40
  style.fill: "#fff3e0"
}
bind: "@PathVariable @RequestParam @RequestBody" {
  width: 340
  height: 45
  style.fill: "#e8f5e9"
}
out: "@ResponseBody / ResponseEntity" {
  width: 280
  height: 40
  style.fill: "#fce4ec"
}

ctrl -> map
map -> bind
bind -> out
```

**Fig. 1.** Scan finds the type, mapping selects the method, annotations bind inputs, converters or a view write the output.

> [!warning] `method = "GET"` does not compile
> Use **`RequestMethod.GET`** or `@GetMapping`. The package is **`org.springframework.web.bind.annotation`**, not `org.springframework.web.annotation`.

> [!warning] `required` defaults to true
> Missing `@RequestParam` / `@PathVariable` / `@RequestHeader` without `required=false` or `defaultValue` → **400**, not `null`.

> [!warning] `@ResponseBody` is not “JSON only”
> Converters pick a media type (`Accept` / `produces`). HTML `@Controller` methods return **view names** unless `@ResponseBody` is present.

> [!tip] Interview answer
> **`@RestController` + `@GetMapping`/`@PostMapping`**, then **`@PathVariable`**, **`@RequestParam`**, **`@RequestBody`**. `@ResponseBody` writes the return value through converters; **`ResponseEntity`** adds status and headers. Global errors: **`@RestControllerAdvice` + `@ExceptionHandler`**.
