<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is a form backing object in Spring MVC?

> [!abstract] Short answer
> A **form-backing object** (also **command object**) is the Java object Spring **binds HTML form fields onto** — typically a `@ModelAttribute` parameter. It is any POJO; it does **not** implement a Spring interface. The controller puts it in the **model** for the GET form and binds the POST onto the **same type**. JSP form tags default the attribute name to **`command`**.

## Command object = bind target

Spring MVC has used this vocabulary since the classic reference: you can use **any object** as a command or form-backing object. Handler method arguments docs still call a `@ModelAttribute` argument a **command object**. `BindingResult` holds errors **for that command object**.

`@ModelAttribute` javadoc: bind a method parameter to a **named model attribute** exposed to the view — “command objects” for HTML forms.

`FormTag` (`<form:form>`): users place the **form object** in the `ModelAndView`; **`modelAttribute`** names it (default **`"command"`** via `DEFAULT_COMMAND_NAME`). Older `commandName` was the same idea.

```java
@GetMapping("/pets/new")
public String showForm(Model model) {
    model.addAttribute("pet", new Pet()); // form-backing instance
    return "petForm";
}

@PostMapping("/pets/new")
public String submit(@Valid @ModelAttribute("pet") Pet pet, BindingResult result) {
    if (result.hasErrors()) {
        return "petForm";
    }
    return "redirect:/pets";
}
```

**Listing 1.** Conceptual GET expose + POST bind. Binding mechanics: [[How does form binding work in Spring MVC]]. Errors: [[What is BindingResult in Spring MVC]]. Tags: [[What are Spring form tags]].

```d2
direction: down
get: "GET: new Pet()\nin Model as \"pet\"" {
  width: 260
  height: 70
  style.fill: "#e3f2fd"
}
jsp: "form:form modelAttribute=\"pet\"\npath=\"name\"" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
post: "POST: WebDataBinder\n→ same Pet type" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}

get -> jsp -> post
```

**Fig. 1.** One named attribute is the form object on the way out and the bind target on the way in.

A dedicated **`AccountForm`** vs a persistence **`Account`** is a design choice. Current binding docs recommend a **web-specific** type or constructor-only binding so clients cannot set arbitrary entity fields.

> [!warning] Default JSP name is `command`
> If `<form:form>` omits `modelAttribute`, it looks for **`command`**. A controller that puts `"todo"` in the model will not match unless the tag names it.

> [!warning] Not required to be anemic
> Spring never mandated “DTO with no methods.” Older docs even bound **business objects**. Prefer a form DTO **for security**, not because the framework forbids logic.

> [!warning] Same name on GET and POST
> `modelAttribute` / `@ModelAttribute("pet")` must match. A mismatch looks like an empty form or a bind to a **new** default-named object.

> [!tip] Interview answer
> **Form-backing / command object is the POJO that holds submitted fields.** Expose it on GET, bind it with `@ModelAttribute` on POST, inspect `BindingResult`. It is the same idea as a named model attribute — the old name from classic Spring MVC.
