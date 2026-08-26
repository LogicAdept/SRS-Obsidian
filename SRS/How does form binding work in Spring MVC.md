<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# How does form binding work in Spring MVC?

> [!abstract] Short answer
> Spring maps **request parameters** (form fields and query string), and also URI variables/headers that do not collide, onto a **command object** through **`WebDataBinder`**. A **`@ModelAttribute`** parameter is taken from the model, session (`@SessionAttributes`), a `Converter`, or constructed, then **constructor and property binding** run. Binding is **not** Bean Validation — add **`@Valid` / `@Validated`** and a **`BindingResult`** immediately after the object to handle errors.

## Command object + `WebDataBinder`

Spring MVC `@ModelAttribute` docs: the parameter annotation binds request data onto a model object. Form body fields are Servlet request parameters.

The instance may already be in the model (from a `@ModelAttribute` **method**), in the HTTP session if listed in class-level `@SessionAttributes`, produced by a `Converter<String, T>` when the attribute name matches a path/request value, or **new** via a default or primary constructor whose args match parameter names.

`@ModelAttribute` **methods** on a `@Controller` (or `@ControllerAdvice`) run **before** `@RequestMapping` methods and seed the model. That matches the dump’s “accessor methods first” claim.

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

**Listing 1.** Conceptual bind + validate + PRG from Spring Framework reference. Errors object: [[What is BindingResult in Spring MVC]]. Redirect after success: [[How do you redirect after a form POST in Spring MVC]].

```d2
direction: down
src: "Request params\n(form + query)" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
binder: "WebDataBinder\nconstructor + setters" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
cmd: "Command / form object\nin Model" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
val: "@Valid → BindingResult" {
  width: 260
  height: 60
  style.fill: "#fce4ec"
}

src -> binder -> cmd -> val
```

**Fig. 1.** Binding fills the object; validation is a separate step. Customize conversion with [[What is the InitBinder annotation in Spring MVC]]. JSP/Thymeleaf fields align with the same bean — [[What are Spring form tags]].

Without `@ModelAttribute`, a non-simple parameter that no other resolver claims is still an **implicit** `@ModelAttribute`. GraalVM native images should annotate it explicitly.

Disable further setter/field binding with `@ModelAttribute(binding = false)` (session-stored entities you must not overwrite). Constructor binding still runs to **create** the object.

> [!warning] Mass assignment
> Property binding can set **any** matching setter. Official guidance: use a **web-specific** DTO, **constructor binding only**, or **`allowedFields`** on the binder. Do not bind a JPA entity from the form blindly.

> [!warning] Binding errors vs missing `BindingResult`
> If binding/validation fails and **`BindingResult` is not the next parameter**, Spring raises **`MethodArgumentNotValidException`** (or `HandlerMethodValidationException` when method validation applies).

> [!warning] Exception handlers do not get a populated `Model`
> `@ModelAttribute` javadoc: after an exception, model content is unreliable; `@ExceptionHandler` does not expose a useful `Model` of the failed form.

> [!tip] Interview answer
> **Form fields become request parameters; `WebDataBinder` copies them onto a `@ModelAttribute` command object** (create or reuse from model/session). Then you validate with `@Valid` and inspect `BindingResult`. Binding ≠ validation, and unrestricted setter binding is a security issue — prefer a dedicated form object.
