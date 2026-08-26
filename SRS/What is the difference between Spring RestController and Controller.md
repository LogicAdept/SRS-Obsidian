<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the difference between Spring `RestController` and `Controller`?

> [!abstract] Short answer
> **`@RestController` is `@Controller` plus type-level `@ResponseBody`.** Every handler’s return value is written to the **HTTP body** via **`HttpMessageConverter`** (often JSON). **`@Controller`** without `@ResponseBody` treats a **`String` as a view name** and goes through **`ViewResolver`** (HTML templates). Both are **`@Component`** stereotypes and become beans via component scan.

## Composed stereotype vs HTML controller

Spring MVC *Declaration*: `@RestController` is meta-annotated with `@Controller` and `@ResponseBody` so **every method inherits** body-writing semantics instead of view rendering.

`RestController` javadoc: `@RequestMapping` methods assume `@ResponseBody` **by default**. Processed when `RequestMappingHandlerMapping` / `RequestMappingHandlerAdapter` are configured (MVC Java config / Boot).

A `@Controller` method can still return JSON by putting `@ResponseBody` on **that method** (or returning `ResponseEntity`). `@RestController` is the class-wide shortcut.

```java
@Controller
public class PageController {
    @GetMapping("/hello")
    public String hello(Model model) {   // view name
        model.addAttribute("msg", "Hi");
        return "hello";
    }
}

@RestController
public class ApiController {
    @GetMapping("/hello")
    public Map<String, String> hello() { // body via converters
        return Map.of("msg", "Hi");
    }
}
```

**Listing 1.** Conceptual contrast from Spring’s `@ResponseBody` / `@RestController` docs. How JSON is written: [[How do you return JSON from a Spring MVC controller]]. Converters: [[What is HttpMessageConverter in Spring MVC]]. Creating controllers: [[How do you create a Spring MVC controller]].

```d2
direction: down
c: "@Controller\nString → ViewResolver" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
r: "@RestController\n=@Controller+@ResponseBody" {
  width: 320
  height: 80
  style.fill: "#e8f5e9"
}
html: "HTML template" {
  width: 180
  height: 50
  style.fill: "#fff3e0"
}
json: "HTTP body\n(JSON/XML/…)" {
  width: 200
  height: 50
  style.fill: "#fce4ec"
}

c -> html
r -> json
```

**Fig. 1.** Same mapping machinery; different default return-value handling.

Jackson is **typical** when `application/json` is negotiated and a Jackson converter is registered — not hard-wired into `@RestController`. XML or other converters apply the same way.

> [!warning] `@Controller` + `String` is a view, not JSON
> Returning `"{\"a\":1}"` without `@ResponseBody` looks for a **template named that string**.

> [!warning] Mixed HTML + JSON in one class
> Use `@Controller` and mark JSON methods with `@ResponseBody`, or split `@Controller` / `@RestController`. Type-level `@ResponseBody` (`@RestController`) makes **every** method a body writer — including accidental view-name returns.

> [!warning] `@ResponseBody` on `@RestController` methods is redundant
> It does not add a second conversion pass.

> [!tip] Interview answer
> **`@RestController` = `@Controller` + `@ResponseBody` on the type.** REST methods serialize the return value to the body; a plain `@Controller` resolves view names for HTML. Both are scanned beans. JSON happens because of message converters, usually Jackson, not because of the annotation name alone.
