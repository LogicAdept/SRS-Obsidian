<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/SecurityContext #SRS

# How do you get the currently authenticated user in Spring Security?

> [!abstract] Short answer
> On the current thread, call **`SecurityContextHolder.getContext().getAuthentication()`**. **`getName()`** is the username, **`getPrincipal()`** is usually a **`UserDetails`**, and **`getAuthorities()`** are the grants. In a Spring MVC controller, inject **`@AuthenticationPrincipal`** for that principal, **`@CurrentSecurityContext`** for the **`SecurityContext`**, or a servlet **`Principal`** / **`HttpServletRequest#getRemoteUser()`** for the username only. A non-null **`Authentication`** is **not** a logged-in user: the default anonymous filter still plants an **`AnonymousAuthenticationToken`**.

## Holder: any code on that thread

`SecurityContextHolder.getContext()` **never** returns `null`. **`getAuthentication()`** **can** — it is `null` when nothing has been stored. With the default HTTP setup, **`AnonymousAuthenticationFilter`** fills that gap with an **`AnonymousAuthenticationToken`**, so service code often sees a token even for a guest.

```java
SecurityContext context = SecurityContextHolder.getContext();
Authentication authentication = context.getAuthentication();
if (authentication == null) {
	return;
}
String username = authentication.getName();
Object principal = authentication.getPrincipal();
Collection<? extends GrantedAuthority> authorities = authentication.getAuthorities();
```

**Listing 1.** Static lookup. `Authentication` extends `Principal`, so `getName()` is the username. After a username/password login the principal is typically a `UserDetails`; authorities are roles, scopes, or other `GrantedAuthority` values — not “roles” as a separate type.

That call is legal in a filter, a `@Service`, or `@PreAuthorize` support on **the same thread**. The default strategy is **`MODE_THREADLOCAL`**. `FilterChainProxy` clears the holder after the request so a pooled thread does not leak the previous user.

## Controller: inject, do not look up

`@EnableWebSecurity` registers **`AuthenticationPrincipalArgumentResolver`**. The annotation injects **`Authentication.getPrincipal()`** so the MVC method never mentions the holder. **`@CurrentSecurityContext`** injects the **`SecurityContext`** (or a SpEL slice such as `authentication`). A method parameter of type **`java.security.Principal`** or **`Authentication`** is the **servlet** principal (`HttpServletRequest#getRemoteUser()` / `getUserPrincipal()`), which is only **`getName()`** unless you downcast.

```java
@GetMapping("/messages/inbox")
ModelAndView inbox(@AuthenticationPrincipal CustomUser user) {
	return findMessages(user);
}

@GetMapping("/me")
String me(@CurrentSecurityContext SecurityContext context) {
	return context.getAuthentication().getName();
}
```

**Listing 2.** MVC since Spring Security **3.2** (`@AuthenticationPrincipal` on the annotation type since **4.0**). SpEL: `@AuthenticationPrincipal(expression = "customUser")` when `UserDetails` wraps your type. A meta-annotation (`@CurrentUser`) keeps controllers off Security types.

The annotation **does not run** on a `@Service` you call yourself. Wrong principal type → **`null`** unless **`errorOnInvalidType`**. Tests that plant Security’s **`User`** then break a controller that asks for **`CustomUser`**.

```d2
direction: down
holder: "SecurityContextHolder.getContext()\nAuthentication (full token)" {
  width: 340
  height: 70
  style.fill: "#e3f2fd"
}
ann: "@AuthenticationPrincipal\ngetPrincipal() only" {
  width: 340
  height: 70
  style.fill: "#e8f5e9"
}
servlet: "Principal / getRemoteUser()\nusername; null if anonymous" {
  width: 340
  height: 70
  style.fill: "#fff3e0"
}

holder -> ann
holder -> servlet
```

**Fig. 1.** One thread-local `Authentication`; three views. See [[What is the difference between AuthenticationPrincipal and SecurityContextHolder]] and [[What is a principal in Spring Security]].

> [!warning] Anonymous token and the wrong thread
> **`AnonymousAuthenticationFilter`** puts a non-null **`AnonymousAuthenticationToken`** in the holder when no one logged in. Servlet **`getUserPrincipal()`** / **`getRemoteUser()`** stay **`null`**, so an MVC **`Principal`** or **`Authentication`** argument is **`null`** and `instanceof AnonymousAuthenticationToken` is **false**. **`Authentication.isAuthenticated()`** only tells **`AbstractSecurityInterceptor`** not to re-authenticate; it is **not** “this is a logged-in user”. Distinguish a guest with **`AuthenticationTrustResolver.isAnonymous()`** (or **`isAuthenticated(Authentication)`**, which also rejects anonymous, since **6.1.7**) or `instanceof` **`AnonymousAuthenticationToken`** via **`@CurrentSecurityContext`**. **`@Async`** without [[How do you propagate SecurityContext to async threads]] sees an empty holder; MVC **`Callable`** return values **do** copy the context, **`DeferredResult`** does not. See [[What is AnonymousAuthenticationToken]] and [[What is SecurityContextHolder]].

> [!tip] Interview answer
> SecurityContextHolder.getContext().getAuthentication() is the ThreadLocal lookup: getName() for the username, getPrincipal() usually UserDetails, getAuthorities() for grants. In a controller prefer @AuthenticationPrincipal or @CurrentSecurityContext; a servlet Principal is only the username and is null when the user is anonymous. AnonymousAuthenticationFilter still plants a non-null token, so Authentication.isAuthenticated() is not "logged in" — check the token type or AuthenticationTrustResolver. Worker threads do not see that ThreadLocal unless you propagate the context.
