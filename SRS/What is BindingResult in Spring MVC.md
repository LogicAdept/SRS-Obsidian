<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is `BindingResult` in Spring MVC?

> [!abstract] Short answer
> **`BindingResult`** (`org.springframework.validation`) is the **error holder** for a **`WebDataBinder`** / command object: type-mismatch bind failures **and** `Validator` / Bean Validation errors. Declare it **immediately after** the `@ModelAttribute` (often `@Valid`) parameter, then `hasErrors()` and redisplay the form. Omit it and Spring raises **`MethodArgumentNotValidException`** instead of entering your method.

## Result of binding, then validation

`BindingResult` extends **`Errors`**: register field/object errors, then expose a **model map** with the target object under its name and the result under **`MODEL_KEY_PREFIX` + objectName** — what Spring form tags (`<form:errors/>`) read.

Spring MVC `@ModelAttribute` docs: add `BindingResult` **next to** the `@ModelAttribute` to handle bind/validation errors in the controller. `@Valid` or `@Validated` runs constraints **after** binding; errors land on the same `BindingResult`.

```java
@PostMapping("/owners/{ownerId}/pets/{petId}/edit")
public String processSubmit(@Valid @ModelAttribute("pet") Pet pet,
        BindingResult result) {
    if (result.hasErrors()) {
        return "petForm";
    }
    // persist ...
    return "redirect:/owners/{ownerId}";
}
```

**Listing 1.** Conceptual adjacent-parameter pattern from Spring Framework reference. How the object was filled: [[How does form binding work in Spring MVC]]. Constraint annotations: [[How does Bean Validation work in Spring Boot]].

```d2
direction: down
bind: "WebDataBinder\nbind request → Pet" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
br: "BindingResult\n(Errors)" {
  width: 220
  height: 60
  style.fill: "#fff3e0"
}
valid: "@Valid / Validator" {
  width: 220
  height: 60
  style.fill: "#fce4ec"
}
view: "Form view +\nMODEL_KEY_PREFIX+name" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

bind -> br
br -> valid
valid -> view
```

**Fig. 1.** One result object collects bind failures and constraint violations. Form tags: [[What are Spring form tags]].

`getSuppressedFields()` lists values that targeted **disallowed** properties (allowedFields / disallowedFields on the binder).

> [!warning] Must be the next parameter
> `BindingResult` has to sit **immediately after** the corresponding command object. A `Model` (or anything else) **between** them is invalid. After `BindingResult`, other arguments (`Model`, `RedirectAttributes`) are fine.

> [!warning] No `BindingResult` → exception, not a 200 form
> Missing adjacent `BindingResult` yields **`MethodArgumentNotValidException`** (or **`HandlerMethodValidationException`** when other parameters use constraint annotations). Handle those globally or always declare `BindingResult` on form POSTs.

> [!warning] `getModel()` is a fresh Map
> Each call builds a new map. Mutating it and calling `getModel()` again does not accumulate — rely on Spring putting the result in the request model for the form view.

> [!tip] Interview answer
> **`BindingResult` is the bind-and-validate error bag for a form object.** Put it right after `@ModelAttribute` / `@Valid`. `hasErrors()` → return the form view; success → redirect. Leave it out and the method never runs — you get an exception instead.
