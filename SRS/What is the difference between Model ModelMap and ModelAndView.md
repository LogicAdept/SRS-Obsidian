<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is the difference between `Model`, `ModelMap` and `ModelAndView`?

> [!abstract] Short answer
> **`Model` is the interface** you inject to add view attributes and then **return a view-name `String`**. **`ModelMap` is a `LinkedHashMap<String, Object>`** with chaining `addAttribute` — it does **not** implement `Model`. The object Spring actually injects is usually **`BindingAwareModelMap`** (`ExtendedModelMap` implements `Model`). **`ModelAndView` is a return type** that holds **both** the view (name or `View`) **and** a model map (`addObject`), optionally an HTTP status.

## Attributes vs a return package

`Model` (2.5.1): `addAttribute` (named value may be `null`; unnamed value must not be `null`; empty collections skipped on generated names), `asMap()`, `mergeAttributes`. Handler methods declare `Model`; you do not construct it.

`ModelMap` (2.0): Map holder for UI tools, **not MVC-tied**. A plain `ModelMap` or even `Map<String, ?>` is enough **to return** as a user model. Pair with a `String` view name.

`ModelAndView`: one object for `DispatcherServlet` — view name **or** a `View` instance, plus model. `getModelMap()` never null. `clear()` in an interceptor `postHandle` suppresses rendering. Status is applied **just before** view render (4.3+).

```java
@GetMapping("/pet")
public String show(Model model) {
    model.addAttribute("pet", pet);
    return "petView";
}
```

**Listing 1.** Conceptual: interface + view name. Resolvers: [[What is a ViewResolver in Spring MVC]]. Two-type sibling: [[What is the difference between ModelMap and ModelAndView]]. `put` vs `addAttribute`: [[What is the difference between model put and addAttribute]].

```java
@GetMapping("/pet")
public ModelAndView show() {
    return new ModelAndView("petView", "pet", pet);
}
```

**Listing 2.** Conceptual: same payload as one return value. `addObject` delegates to `ModelMap.addAttribute`.

```d2
direction: down
m: "Model (interface)\naddAttribute → return String" {
  width: 300
  height: 55
  style.fill: "#e3f2fd"
}
mm: "ModelMap\nextends LinkedHashMap" {
  width: 280
  height: 50
  style.fill: "#fff3e0"
}
ex: "ExtendedModelMap\nimplements Model" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
mav: "ModelAndView\nview + ModelMap [+ status]" {
  width: 300
  height: 55
  style.fill: "#fce4ec"
}

mm -> ex
ex -> m
```

**Fig. 1.** Dumps that say “`ModelMap` implements `Model`” skip `ExtendedModelMap`. `ModelAndView` is not in that hierarchy; it **contains** a `ModelMap`.

> [!warning] `ModelMap` ≠ `Model`
> `ModelMap` extends `LinkedHashMap`. **`ExtendedModelMap` implements `Model`.** The injected instance is typically **`BindingAwareModelMap`** (drops a stale `BindingResult` if you `put` over the target).

> [!warning] `@ResponseBody` skips both
> Returning JSON does not use this model/view pair. `ModelAndView` on a `@RestController` method is the wrong tool.

> [!warning] Unnamed `addAttribute` skips empty collections
> Generated-name `addAttribute(Object)` does not add an empty `Collection` (cannot pick a convention name). JSTL should treat missing as `null`.

> [!tip] Interview answer
> **`Model` is how a `@Controller` fills attributes while returning a view name. `ModelMap` is the map implementation; Spring’s injected model is an `ExtendedModelMap`. `ModelAndView` packages view + model (+ optional status) as the method’s return value.** Same data, different packaging.
