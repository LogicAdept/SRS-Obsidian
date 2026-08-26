<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS

# What is the difference between `SessionAttributes` and `SessionAttribute`?

> [!abstract] Short answer
> **`@SessionAttributes` is type-level conversational storage:** named (or typed) **model** attributes are copied into the HTTP session for **this controller’s wizard**, then removed when a method calls **`SessionStatus.setComplete()`**. **`@SessionAttribute` is a method-parameter binder** for an **already stored**, usually **global** session value (login user, filter-set object). Plural = “keep my model in session for a conversation.” Singular = “read one existing session attribute.”

## Conversation vs lookup

`@SessionAttributes` (since 2.5) lists **`names` / `value`** and/or **`types`**. On the first request that puts `pet` in the model, Spring **promotes** it to the session and keeps serving it on later requests to that handler. Javadoc: operate on the **model**; session key names may differ. It is **not** for a permanent login object — use `HttpSession.setAttribute` / `WebRequest` for that.

`@SessionAttribute` (since 4.3) binds one session attribute to a parameter. Default **`required = true`**: missing attribute or **no session** fails. `required=false` or `Optional` for absence. It does **not** add or remove attributes; inject `HttpSession` or `WebRequest` for that.

On controller **interfaces** (AOP proxies), put `@SessionAttributes` on the **interface**, not only the implementation.

```java
@Controller
@SessionAttributes("pet")
public class EditPetForm {

    @PostMapping("/pets/{id}")
    public String handle(Pet pet, BindingResult errors, SessionStatus status) {
        if (errors.hasErrors()) {
            return "petForm";
        }
        status.setComplete();
        return "redirect:/pets/{id}";
    }
}
```

**Listing 1.** Conceptual Framework example: conversational `pet` until `setComplete()`. Form object: [[What is a form backing object in Spring MVC]]. One-hop redirect data: [[What is FlashMap in Spring MVC]]. Binding errors: [[What is BindingResult in Spring MVC]].

```java
@GetMapping("/")
public String home(@SessionAttribute User user) {
    return "home";
}
```

**Listing 2.** Conceptual: global session user, not this controller’s `@SessionAttributes` list.

```d2
direction: down
sa: "@SessionAttributes(\"pet\")\ncontroller type" {
  width: 280
  height: 55
  style.fill: "#e3f2fd"
}
model: "model attribute pet" {
  width: 220
  height: 45
  style.fill: "#fff3e0"
}
sess: "HTTP session\n(until setComplete)" {
  width: 240
  height: 50
  style.fill: "#e8f5e9"
}
param: "@SessionAttribute User\nread existing" {
  width: 240
  height: 50
  style.fill: "#fce4ec"
}

sa -> model
model -> sess
param -> sess
```

**Fig. 1.** Plural writes a conversation from the model. Singular only reads. They are not aliases.

> [!warning] Forget `setComplete()`
> Conversational attributes stay in the session after the wizard ends and leak into the next visit. Call **`SessionStatus.setComplete()`** on the success path.

> [!warning] Singular is required by default
> `@SessionAttribute User user` throws if the session has no `user` (or there is no session). Use `required=false` for optional globals.

> [!warning] Not flash, not `HttpSession` DIY
> `@SessionAttributes` is **not** `FlashMap` (one redirect hop) and **not** a substitute for stuffing arbitrary keys with `session.setAttribute`. Permanent objects belong on `HttpSession`; wizard form beans belong on `@SessionAttributes`.

> [!tip] Interview answer
> **`@SessionAttributes` (plural) keeps named model attributes in session for one controller conversation until `SessionStatus.setComplete()`.** **`@SessionAttribute` (singular) injects an existing session value into a method parameter — typically something a filter or login stored.** Mixing the two names is the usual dump mistake.
