<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# What is `FlashMap` in Spring MVC?

> [!abstract] Short answer
> **`FlashMap` is a `Map` of attributes for the next request**, usually after a **redirect** (Post-Redirect-Get). It is saved (typically in the **HTTP session**), exposed on the matching follow-up request, then **removed**. Annotated controllers use **`RedirectAttributes.addFlashAttribute`**, not `FlashMap` directly. **`FlashMapManager`** (default **`SessionFlashMapManager`**) stores and matches maps. Support is always on; unused flash does **not** create a session.

## Input map, output map, then gone

On every request Spring MVC has an **input** `FlashMap` (from a previous request, if any) and an **output** `FlashMap` (to save for a later one). `RequestContextUtils` exposes both. `FlashMapManager.retrieveAndUpdate` runs at the **start** of each request: match, **remove** the used map, drop **expired** maps. `saveOutputFlashMap` runs only when there is something to save, **before** the redirect commits the response.

After the redirect, input flash attributes are copied onto the **target controller’s `Model`**. You can read them as ordinary model attributes (including `@ModelAttribute("message")`). Default timeout is **180 seconds** (`AbstractFlashMapManager`).

`RedirectAttributes.addAttribute` is **not** flash: those values are formatted as strings for the **redirect URL** (query or URI template). `addFlashAttribute` goes into the output `FlashMap`. A `RedirectAttributes` model is used only if the method returns a redirect view name or `RedirectView`.

```java
@PostMapping("/accounts")
public String handle(Account account, BindingResult result,
        RedirectAttributes redirectAttrs) {
    if (result.hasErrors()) {
        return "accounts/new";
    }
    redirectAttrs.addAttribute("id", account.getId())
            .addFlashAttribute("message", "Account created!");
    return "redirect:/accounts/{id}";
}
```

**Listing 1.** Conceptual Framework example: `id` is a redirect URL variable; `message` is flash. PRG: [[How do you redirect after a form POST in Spring MVC]]. Session-scoped model is a different SPI: [[What is the difference between SessionAttributes and SessionAttribute]]. Special beans: [[What is Spring MVC DispatcherServlet]].

```d2
direction: down
post: "POST handler\naddFlashAttribute" {
  width: 240
  height: 55
  style.fill: "#e3f2fd"
}
out: "output FlashMap\n(session, ~180s)" {
  width: 240
  height: 55
  style.fill: "#fff3e0"
}
get: "GET after redirect\ninput FlashMap → Model" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}
gone: "map removed" {
  width: 180
  height: 40
  style.fill: "#fce4ec"
}

post -> out
out -> get
get -> gone
```

**Fig. 1.** One hop. `RedirectView` stamps the target path and query so the manager can match the intended GET, not a random next request.

> [!warning] The “next” request may not be your GET
> Polling, prefetch, or a static-resource hit can consume the map. Prefer flash **for redirects**; `RedirectView` matching reduces (does not eliminate) that race.

> [!warning] Not `@SessionAttributes`
> Flash is **one matching request**, then deleted. Session attributes stay until the session ends or you clear them.

> [!warning] Empty unless you redirect
> Putting flash on a method that returns a normal view name does not persist it: `RedirectAttributes` is ignored unless the result is a redirect.

> [!tip] Interview answer
> **`FlashMap` carries model data across a redirect, then disappears — the PRG success message.** Controllers call `RedirectAttributes.addFlashAttribute`. Default storage is the HTTP session with a three-minute expiry, and `RedirectView` stamps the target URL so the follow-up GET is the one that receives it.
