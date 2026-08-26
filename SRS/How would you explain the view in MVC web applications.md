<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Patterns/Architecture/UI/MVC #SRS

# How would you explain the view in MVC web applications?

> [!abstract] Short answer
> In **Model 2 / MVC**, the **view only renders**. The controller updates the **model** and **selects** the view; the view does not own business rules. In Spring MVC that view is the **`View`** SPI: **`render(model, request, response)`** prepares the model (JSP: request attributes) then hands off to a technology (JSP `RequestDispatcher`, FreeMarker, Thymeleaf, …). Controllers usually return a **logical name** (`String`, `ModelAndView`); a **`ViewResolver`** maps it to a **`View`**. **`@ResponseBody` / `@RestController` skip `View`** and write through **`HttpMessageConverter`**.

## Presentation, not a file path

Java EE Model 2: model = data and operations, view = **how that data is shown**, controller = dispatch and **choose the next view**. Spring’s `View` javadoc: implementations **render content and expose the model**; one view may expose **many** attributes. The interface is **stateless** — treat `View` beans as **thread-safe**. `View.render`’s first step is preparing the request; the second is the actual render (for JSP, include/forward via **`RequestDispatcher`**).

`ViewResolver` maps **names → `View`**. `View` **prepares data**, then the template engine paints HTML. Switching Thymeleaf, Groovy Markup, or JSP is **configuration**, not a controller rewrite. Thymeleaf’s Spring beans (`ThymeleafViewResolver`, …) are owned by the **Thymeleaf** project, not Framework core.

A `@Controller` method may return:

- **`String`** — logical view name + implicit model (`Model` / `@ModelAttribute`)
- **`View`** — a `View` instance, still with the implicit model
- **`ModelAndView`** — name or `View` plus attributes (optional status)
- **`Model` / `Map`** — attributes only; name from **`RequestToViewNameTranslator`**

`redirect:` / `forward:` prefixes on names are **`UrlBasedViewResolver`** instructions, not template files. Resolvers: [[What is a ViewResolver in Spring MVC]]. Model vs `ModelAndView`: [[What is the difference between Model ModelMap and ModelAndView]]. Model 2 vs mixed pages: [[What is the difference between Model 1 and Model 2 architectures]].

```java
@Controller
public class HelloController {

    @GetMapping("/hello")
    public String handle(Model model) {
        model.addAttribute("message", "Hello World!");
        return "index";
    }
}
```

**Listing 1.** Conceptual Framework annotated-controller sample. `"index"` is a **logical name**. A JSP resolver typically turns it into `/WEB-INF/index.jsp` (or a prefix/suffix you set). `@RestController` on this method would write the characters `index` as the **body**.

```d2
direction: down
c: "@Controller\nmodel + logical name" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
vr: "ViewResolver\nname → View" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
v: "View.render\nprepare model, then engine" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
rest: "@ResponseBody\nHttpMessageConverter" {
  width: 260
  height: 50
  style.fill: "#fce4ec"
}

c -> vr -> v
c -> rest
```

**Fig. 1.** HTML goes through `View`. REST bodies do not. Lifecycle: [[How does the Spring MVC request lifecycle work]]. `@Controller` vs `@RestController`: [[What is the difference between Spring RestController and Controller]].

> [!warning] Templates sit inside the app trust boundary
> Framework *View Technologies*: views can see **every bean** in the application context. Do **not** feed Spring template support templates that **outsiders can edit** (SSTI / bean access). Put JSPs under **`WEB-INF`** so clients cannot request the file by URL.

> [!warning] A `String` return is a view name only without `@ResponseBody`
> On `@RestController` (type-level `@ResponseBody`) a `String` is the **payload**. Returning `"users/list"` does not open a template.

> [!warning] The logical name is not the classpath file
> Prefix/suffix live on the resolver (`InternalResourceViewResolver`, Thymeleaf resolver, …). Returning `"/WEB-INF/views/index.jsp"` from the controller couples you to one technology and skips the point of a logical name.

> [!tip] Interview answer
> **The view renders the model; it does not decide business outcomes.** In Spring MVC that is the `View` interface: prepare the model, then a template or JSP paints the response. Controllers return a logical name; `ViewResolver` finds the `View`. REST methods with `@ResponseBody` never enter that path.
