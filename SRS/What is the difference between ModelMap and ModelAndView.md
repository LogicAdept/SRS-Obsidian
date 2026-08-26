<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is the difference between `ModelMap` and `ModelAndView`?

> [!abstract] Short answer
> **`ModelMap` is only the attribute map** (`LinkedHashMap<String, Object>` + chaining `addAttribute`). You still **return a view-name `String`** (or a `View`). **`ModelAndView` is the pair**: view (name or `View` instance) **plus** that map (`addObject` → `ModelMap.addAttribute`), optionally an HTTP status. Same data for `DispatcherServlet`; different packaging.

## Map vs map-and-view

`ModelMap` javadoc: generic UI model holder, **not** tied to Servlet MVC. It does **not** implement `Model`. Spring injects **`ExtendedModelMap` / `BindingAwareModelMap`** when you declare `Model` or `ModelMap`. You can also `return` a `ModelMap` or `Map<String, ?>` as the user model with a separate view name.

`ModelAndView` javadoc: holds **model and view in one return value**. View is a **String** for `ViewResolver` or a **`View` object**. `getModelMap()` is never `null`. `setStatus` applies **just before** render. `clear()` in interceptor `postHandle` suppresses rendering.

```java
@GetMapping("/pet")
public String show(ModelMap model) {
    model.addAttribute("pet", pet);
    return "petView";
}
```

**Listing 1.** Conceptual: map argument + `String` view. Three-way: [[What is the difference between Model ModelMap and ModelAndView]]. Resolvers: [[What is a ViewResolver in Spring MVC]]. `put` vs `addAttribute`: [[What is the difference between model put and addAttribute]].

```java
@GetMapping("/pet")
public ModelAndView show() {
    return new ModelAndView("petView", "pet", pet);
}
```

**Listing 2.** Conceptual: one object. Equivalent: `new ModelAndView("petView").addObject("pet", pet)`.

```d2
direction: down
mm: "ModelMap\nattributes only" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
s: "return \"petView\"" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}
mav: "ModelAndView\nview + ModelMap" {
  width: 260
  height: 50
  style.fill: "#e8f5e9"
}
ds: "DispatcherServlet\nViewResolver" {
  width: 240
  height: 45
  style.fill: "#fce4ec"
}

mm -> s
s -> ds
mav -> ds
```

**Fig. 1.** Both paths end at the same servlet. `@ResponseBody` uses neither.

> [!warning] `ModelMap` is not `Model`
> Dumps that call `ModelMap` “the implementation of `Model`” skip **`ExtendedModelMap`**. `ModelMap` is the `LinkedHashMap`; `Model` is the interface on the subclass.

> [!warning] Returning only `ModelMap`
> A method that returns `ModelMap` and **no** view name relies on `RequestToViewNameTranslator` (default: derive a name from the URL). That is easy to miss. Prefer an explicit `String` or `ModelAndView` view.

> [!warning] Status lives on `ModelAndView`
> `ModelMap` has no HTTP status. Need 404 on an HTML view? `new ModelAndView("notFound", HttpStatus.NOT_FOUND)` (or `ResponseEntity` / `@ResponseStatus` on other paths).

> [!tip] Interview answer
> **`ModelMap` is the bag of attributes; you still return a view name. `ModelAndView` is that bag plus the view (and optional status) as the method’s return type.** Spring’s injected `Model` is an `ExtendedModelMap`, not a raw `ModelMap` implementing `Model`.
