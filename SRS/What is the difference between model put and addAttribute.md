<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is the difference between `model.put` and `addAttribute`?

> [!abstract] Short answer
> **`addAttribute` is `Model` / `ModelMap`’s API:** it **`put`s** after **`Assert.notNull` on the attribute name**, then **returns `this`** for chaining. **Named values may be `null`.** **`put` is `Map.put`:** no name check, returns the **previous** value, no chaining. Unnamed **`addAttribute(Object)`** generates a key via **`Conventions.getVariableName`**, **rejects a `null` object**, and **skips empty `Collection`s**. Prefer `addAttribute` on `Model`.

## Wrapper, then `put`

`ModelMap.addAttribute(String, Object)` (Framework source): `Assert.notNull(attributeName, "Model attribute name must not be null")`, then `put(attributeName, attributeValue)`, `return this`. Javadoc: value **can be `null`**.

`addAttribute(Object)`: `Assert.notNull(attributeValue)`; if it is an empty `Collection`, return unchanged (no key); else name from `Conventions.getVariableName`. Empty arrays are **not** skipped the same way (they get a generated name).

`Model` exposes `addAttribute`, not `put`. `asMap()` returns the backing map if you insist on `Map` methods. The injected instance is typically **`BindingAwareModelMap`**: **`put` / `putAll`** drop a matching **`BindingResult`** when you replace the target attribute through **Map** operations.

```java
model.addAttribute("attribute1", "value1")
     .addAttribute("attribute2", "value2");

model.put("attribute1", "value1"); // previous value, not this
```

**Listing 1.** Conceptual: chaining needs `addAttribute`. Three types: [[What is the difference between Model ModelMap and ModelAndView]]. Map vs `ModelAndView`: [[What is the difference between ModelMap and ModelAndView]]. Binding keys: [[What is BindingResult in Spring MVC]].

```d2
direction: down
add: "addAttribute(name, value)\nAssert name ≠ null" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
put: "Map.put(name, value)" {
  width: 240
  height: 45
  style.fill: "#fff3e0"
}
map: "LinkedHashMap contents" {
  width: 240
  height: 45
  style.fill: "#e8f5e9"
}

add -> put
put -> map
```

**Fig. 1.** Named `addAttribute` is `put` plus a name assertion and a fluent return. It is not a second store.

> [!warning] The null check is the **name**
> Dumps that say `addAttribute` “null-checks the value” are **wrong** for the two-arg form. **`null` values are stored.** A **`null` name** throws. Unnamed `addAttribute(obj)` forbids a **`null` object**.

> [!warning] `put` on `Model`
> A `Model` parameter has no `put`. Cast/`asMap()`/`ModelMap` does. Mixing `put` over a bound object can strip the **`BindingResult`** on `BindingAwareModelMap`.

> [!warning] Empty collections
> Unnamed `addAttribute(emptyList)` is a no-op. Views should treat a missing attribute like `null` (JSTL already does). Named `addAttribute("items", List.of())` **does** store the empty list.

> [!tip] Interview answer
> **`addAttribute` is the model API: it validates the name, `put`s, and returns the map for chaining.** **`put` is raw `Map`.** Use `addAttribute`; remember unnamed add skips empty collections and rejects a null object.
