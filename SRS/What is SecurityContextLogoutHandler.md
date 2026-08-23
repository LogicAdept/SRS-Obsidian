<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS

# What is SecurityContextLogoutHandler?

> [!abstract] Short answer
> **SecurityContextLogoutHandler** is a Spring Security **`LogoutHandler`** that performs the core server-side logout cleanup: it clears the **`Authentication`** from the current **`SecurityContext`**, removes the persisted context via **`SecurityContextRepository`**, and (by default) **invalidates the HTTP session**.

## What `logout()` does

The handler implements **`LogoutHandler#logout(HttpServletRequest, HttpServletResponse, Authentication)`**. The `Authentication` parameter is unused; the request and response drive cleanup.

On invocation it:

1. **Clears authentication** from the `SecurityContext` held in `SecurityContextHolder` when `clearAuthentication` is `true` (the default). This avoids concurrent requests still seeing a stale principal on the same thread.
2. **Clears the stored security context** through the configured **`SecurityContextRepository`** (default **`HttpSessionSecurityContextRepository`**).
3. **Invalidates the HTTP session** when `invalidateHttpSession` is `true` (the default) and the session is not `null`.

These three steps are exactly what the reference docs list for default **`POST /logout`** processing — the same handler runs inside **`LogoutFilter`** when you use the `logout` DSL.

```java
SecurityContextLogoutHandler logoutHandler = new SecurityContextLogoutHandler();

@PostMapping("/my/logout")
public String performLogout(Authentication authentication,
        HttpServletRequest request, HttpServletResponse response) {
    logoutHandler.logout(request, response, authentication);
    return "redirect:/home";
}
```

**Listing 1.** Minimum pattern for a custom MVC logout endpoint; without this handler the user may not actually be logged out.

## Defaults and configuration

Both toggles default to **`true`**:

| Property | Default | Effect when `false` |
|---|---|---|
| `invalidateHttpSession` | `true` | Session kept alive; `JSESSIONID` may survive |
| `clearAuthentication` | `true` | Authentication left on the in-memory context |

You can also plug in a custom **`SecurityContextHolderStrategy`** or **`SecurityContextRepository`**.

```d2
direction: right
call: "logout(request,\nresponse, auth)" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
holder: "SecurityContextHolder\nclear Authentication" {
  width: 220
  height: 70
  style.fill: "#fff3e0"
}
repo: "SecurityContextRepository\nclear persisted context" {
  width: 230
  height: 70
  style.fill: "#e8f5e9"
}
session: "HttpSession\ninvalidate (default)" {
  width: 200
  height: 70
  style.fill: "#fce4ec"
}

call -> holder -> repo -> session
```

**Fig. 1.** Default logout path: in-memory context, persisted context, then session invalidation.

> [!warning] Clearing context without invalidating the session
> If you set **`invalidateHttpSession(false)`** but still clear the repository, the browser may keep sending the same **`JSESSIONID`**. A later request can reload authentication from session attributes or other server state unless every persistence layer is cleared. Default **`invalidateHttpSession(true)`** drops the session cookie with the session. See [[What is LogoutFilter]] for the full handler chain (remember-me, CSRF token cleanup, success redirect).

> [!tip] Interview answer
> SecurityContextLogoutHandler is the standard LogoutHandler that wipes the security context from SecurityContextHolder and SecurityContextRepository and invalidates the session by default. LogoutFilter uses it on POST /logout; custom controllers must call it too or the user stays authenticated on the next request.
