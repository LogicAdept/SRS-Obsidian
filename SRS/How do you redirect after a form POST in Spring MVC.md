<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS

# How do you redirect after a form POST in Spring MVC?

> [!abstract] Short answer
> On success, return a view name with the **`redirect:`** prefix (Post-Redirect-Get) so the browser issues a **new GET** and a refresh does not resubmit the POST. On validation errors, return the **form view name** in the **same request**. Carry a one-hop message with **`RedirectAttributes.addFlashAttribute`**, not the regular model.

## Post-Redirect-Get via `redirect:`

`UrlBasedViewResolver` javadoc: a view name such as `"redirect:myAction"` is **not** resolved as a template. It triggers a redirect — typically after a form workflow finishes. `"forward:myAction"` stays in the **same** request (server-side forward); that is **not** PRG.

Spring MVC *Flash Attributes*: the usual redirect case is **Post-Redirect-Get**. Flash data is stored (typically in the session) for the **next** request, then removed. Controllers should use **`RedirectAttributes`**, not `FlashMap` directly.

`RedirectView` actually sends the redirect: default **HTTP 1.0 compatible** behavior uses **`sendRedirect` (302)**; turning compatibility off sends **303 See Other**, which some HTTP 1.1 clients expect after POST.

```java
@PostMapping("/accounts")
public String handle(Account account, BindingResult result,
        RedirectAttributes redirectAttrs) {
    if (result.hasErrors()) {
        return "accounts/new"; // same POST request — redisplay form
    }
    // persist account ...
    redirectAttrs.addAttribute("id", account.getId())
            .addFlashAttribute("message", "Account created!");
    return "redirect:/accounts/{id}";
}
```

**Listing 1.** Conceptual `RedirectAttributes` example from Spring Framework javadoc. Validation pairing: [[What is BindingResult in Spring MVC]]. Flash storage: [[What is FlashMap in Spring MVC]].

```d2
direction: down
post: "POST /accounts\n(form submit)" {
  width: 240
  height: 60
  style.fill: "#e3f2fd"
}
ok: "redirect:/accounts/{id}\n302/303 + flash" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
get: "GET /accounts/42\nnew request, flash → Model" {
  width: 300
  height: 70
  style.fill: "#fff3e0"
}
err: "return \"accounts/new\"\nsame request" {
  width: 260
  height: 70
  style.fill: "#ffebee"
}

post -> ok -> get
post -> err
```

**Fig. 1.** Success leaves the POST; errors stay on the form view. URI template variables and query params come from `RedirectAttributes.addAttribute`, not from leftover POST model fields unless you expose them.

After the redirect, input `FlashMap` attributes are merged into the **target** controller’s `Model`. `RedirectView` stamps the flash map with the **redirect URL** path/query so a concurrent poll is less likely to steal it.

> [!warning] `redirect:` vs `redirect:/`
> A leading **`/`** is a path from the **host root** unless `RedirectView` is **context-relative**. `"redirect:list-todos"` is relative to the **current request URL**. Wrong slash → 404 after POST.

> [!warning] Regular `Model` does not survive the redirect
> A `RedirectAttributes` model is **empty** unless you return a redirect view / `RedirectView`. Dump `model.clear()` is not the official PRG API — use **`addFlashAttribute`** for messages and **`addAttribute`** for URL/query values.

> [!warning] `forward:` is not PRG
> `forward:` keeps the original POST. Refresh still resubmits. Use it only when you intentionally stay in one request.

> [!tip] Interview answer
> **Successful POST returns `"redirect:/…"` so the next browser request is GET (PRG).** Validation failures return the form view name. Pass a success message with `RedirectAttributes.addFlashAttribute`; `redirect:` is a `UrlBasedViewResolver` prefix, not a logical template name.
