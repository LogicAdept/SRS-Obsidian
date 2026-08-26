<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What are Spring form tags?

> [!abstract] Short answer
> The **Spring form tag library** (`form:form`, `form:input`, `form:errors`, …) is a **JSP** tag set that binds HTML controls to a **form object in the model** and renders **`BindingResult`** field/object errors. Declare **`modelAttribute`** (default **`command`**). **`path`** is the property to bind. This is **not** Thymeleaf (`th:object` / `th:field`).

## JSP tags on the command object

`FormTag` (`<form:form>`): renders `<form>` and exposes a **binding path** to nested tags. Put the form object in the model; name it with **`modelAttribute`**. Default attribute name is **`command`**.

`InputTag` (`<form:input>`): HTML `input type="text"` using the **bound value**. **`path`** is required — the property path for data binding. **`cssErrorClass`** applies when that field has errors.

`ErrorsTag` (`<form:errors>`): renders errors in a `<span>` (by default). Three patterns: **`path="field"`** (field errors), **omit `path`** (object errors only), **`path="*"`** (all errors). Renders only when there are errors for that path. Messages come from the bind status / `BindingResult` Spring already placed in the model.

```jsp
<%@ taglib prefix="form" uri="http://www.springframework.org/tags/form" %>
<form:form method="post" modelAttribute="pet">
    <form:input path="name"/>
    <form:errors path="name"/>
    <form:errors path="*"/>
</form:form>
```

**Listing 1.** Conceptual JSP using current `modelAttribute` (not dump `commandName`). Backing bean: [[What is a form backing object in Spring MVC]]. Error bag: [[What is BindingResult in Spring MVC]].

```d2
direction: down
model: "Model attribute\npet + BindingResult" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}
form: "form:form\nmodelAttribute=\"pet\"" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
fields: "form:input path=\"name\"\nform:errors path=\"name\"" {
  width: 280
  height: 70
  style.fill: "#e8f5e9"
}

model -> form -> fields
```

**Fig. 1.** Tags read the same named object the controller bound on POST. Binding: [[How does form binding work in Spring MVC]].

Dump `commandName` is the **legacy** form-object attribute; current `FormTag` API documents **`modelAttribute`**.

HTML views in Thymeleaf use a **different** dialect. Spring form tags apply to **JSP** (and the Spring taglib), not to REST JSON APIs.

> [!warning] Name must match the controller
> `modelAttribute="todo"` requires `model.addAttribute("todo", …)` / `@ModelAttribute("todo")`. Default **`command`** if you omit the name.

> [!warning] `path` is the Java property, not the HTTP parameter nickname
> Nested paths follow the bean graph (`address.city`). A typo binds nothing useful and error tags stay empty.

> [!warning] No `BindingResult` in the model → empty `<form:errors/>`
> If the POST method lacks an adjacent `BindingResult` and throws instead, the form redisplay path never runs.

> [!tip] Interview answer
> **Spring form tags are JSP helpers that bind inputs to a model command object and print `BindingResult` errors.** Use `modelAttribute` (default `command`) and `path` for properties. Thymeleaf is a separate template dialect; REST controllers do not use these tags.
