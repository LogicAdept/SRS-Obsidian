<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the `InitBinder` annotation in Spring MVC?

> [!abstract] Short answer
> **`@InitBinder`** marks a **`void` controller (or `@ControllerAdvice`) method** that customizes the **`WebDataBinder`** used to populate **command/form arguments**: register **`PropertyEditor`**, **`Converter`**, or **`Formatter`** instances. It supports the same argument types as `@RequestMapping` **except** command objects and **`BindingResult`**. Empty **`value`** → all attributes on that controller; set **`value`** to limit names.

## Per-controller binder setup

Spring MVC `@InitBinder` docs: initialize binders that bind request parameters, convert strings to property types, and format properties when rendering HTML forms. On a `@Controller` the customizations are **local** (or per named model attribute). On **`@ControllerAdvice`** they can apply to **all or a subset** of controllers.

`InitBinder` javadoc: typical arguments are `WebDataBinder` plus `WebRequest` or `Locale`. **Must not return a value.**

```java
@Controller
public class FormController {

    @InitBinder
    public void initBinder(WebDataBinder binder) {
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");
        dateFormat.setLenient(false);
        binder.registerCustomEditor(Date.class, new CustomDateEditor(dateFormat, false));
    }

    @InitBinder("pet")
    public void petBinder(WebDataBinder binder) {
        binder.addCustomFormatter(new DateFormatter("yyyy-MM-dd"));
    }
}
```

**Listing 1.** Conceptual local editors/formatters from Spring Framework reference. Form objects: [[How does form binding work in Spring MVC]]. App-wide converters: [[How do you configure message converters in Spring MVC]] is HTTP bodies — for **form fields** also use `WebMvcConfigurer.addFormatters`. Dates: [[How do you set a default date format in Spring MVC]].

```d2
direction: down
init: "@InitBinder\nvoid method" {
  width: 220
  height: 60
  style.fill: "#e3f2fd"
}
wb: "WebDataBinder" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
cmd: "@ModelAttribute\ncommand object" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

init -> wb -> cmd
```

**Fig. 1.** Binder callbacks run before the handler argument is populated. Security: still set **allowedFields** / prefer constructor binding — `@InitBinder` does not make mass assignment safe by itself.

Alternatively register `Converter` / `Formatter` on a shared **`FormattingConversionService`** via MVC config so every controller shares them.

> [!warning] No form object / `BindingResult` parameters
> Those types are **illegal** on `@InitBinder` methods. Pass `WebDataBinder`, not the `Pet` you are about to bind.

> [!warning] `java.util.Date` vs `java.time`
> `CustomDateEditor` targets **`java.util.Date`**. `LocalDate` usually uses **`@DateTimeFormat`** or a `Formatter<LocalDate>`, not that editor.

> [!warning] Advice scope
> `@InitBinder` on `@ControllerAdvice` is **global** unless the advice itself is narrowed (`assignableTypes`, annotations, …). Easy to change binding for the whole app by accident.

> [!tip] Interview answer
> **`@InitBinder` is a void method that gets `WebDataBinder` before form/command binding.** Register editors or formatters there, or globally via `FormattingConversionService`. It cannot take the command object itself. `@ControllerAdvice` makes the same hook application-wide.
