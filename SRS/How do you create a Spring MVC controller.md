<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# How do you create a Spring MVC controller?

> [!abstract] Short answer
> Annotate a class with **`@Controller`**, register it as a Spring bean (usually via **component scanning**), and map handler methods with **`@RequestMapping`** or HTTP shortcuts such as **`@GetMapping`**. The class does not extend a base type. **`@Controller`** is a **`@Component`** stereotype for the web layer; **`@RestController`** is `@Controller` plus type-level **`@ResponseBody`**.

## Stereotype plus handler methods

Spring MVC’s annotated-controller model: `@Controller` / `@RestController` beans express mappings, input binding, and exception handling with annotations. Methods have flexible signatures; you do not implement a controller interface.

`@Controller` javadoc: it is a specialization of `@Component`, so classpath scanning can auto-detect it. It is typically combined with `@RequestMapping`-style handler methods.

Spring MVC *Declaration* docs: you can also declare the bean explicitly in the servlet `WebApplicationContext`. Auto-detection needs `@ComponentScan` (or XML `<context:component-scan/>`) covering the controller’s package — same mechanism as other stereotypes.

```java
@Controller
public class HelloController {

    @GetMapping("/hello")
    public String handle(Model model) {
        model.addAttribute("message", "Hello World!");
        return "index";
    }
}

@Configuration
@ComponentScan("org.example.web")
class WebConfiguration {
}
```

**Listing 1.** Conceptual annotated controller and scan from Spring Framework MVC reference. `@GetMapping` is a composed `@RequestMapping` for GET — [[How do you map HTTP methods in Spring MVC]].

```d2
direction: down
scan: "@ComponentScan\nfinds @Controller" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
bean: "Controller bean in\nWebApplicationContext" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
map: "@GetMapping / @RequestMapping\nhandler method" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
ds: "DispatcherServlet\ninvokes adapter" {
  width: 260
  height: 70
  style.fill: "#fce4ec"
}

scan -> bean -> map -> ds
```

**Fig. 1.** Scan registers the bean; mappings are metadata the front controller uses at request time — [[What is Spring MVC DispatcherServlet]].

`@RestController` is meta-annotated with `@Controller` and `@ResponseBody`: every method writes the return value to the body instead of resolving a view name. Contrast [[What is the difference between Spring RestController and Controller]].

> [!warning] Annotation without a bean is a no-op
> `@Controller` only works if the class is a Spring bean in the servlet `WebApplicationContext`. A class outside the scan base package never becomes a handler.

> [!warning] Interface-only `@RequestMapping` can disappear under JDK proxies
> As of Spring 6.0, MVC no longer treats a type-level `@RequestMapping` on an interface as enough when the controller is an interface proxy. Put `@Controller` on the interface or use class-based proxying.

> [!warning] `@RequestMapping` on the same element is not stackable
> Multiple `@RequestMapping` (including composed `@GetMapping` + `@RequestMapping`) on the **same** class or method: Spring logs a warning and uses only the first mapping.

> [!tip] Interview answer
> **Stereotype a class with `@Controller`, make it a scanned bean, map methods with `@RequestMapping` or `@GetMapping`.** No base class required. `@Controller` is `@Component` for the web layer; use `@RestController` when every method should write the body instead of a view name.
