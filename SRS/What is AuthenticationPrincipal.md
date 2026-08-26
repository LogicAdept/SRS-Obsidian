<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Annotations #Java/Spring/Framework/WebMvc #SRS

# What is `AuthenticationPrincipal`?

> [!abstract] Short answer
> **`@AuthenticationPrincipal` is an MVC (and messaging) parameter annotation that injects `Authentication.getPrincipal()`** — typically your `UserDetails` / custom user — without a `SecurityContextHolder` lookup and cast. `AuthenticationPrincipalArgumentResolver` is registered when you use **`@EnableWebSecurity`**. If `Authentication` or the principal is **null**, or the **types do not match**, the argument is **null** unless **`errorOnInvalidType = true`** (then **`ClassCastException`**).

## Resolver, not a filter

Spring Security *MVC Integration*: the resolver reads `SecurityContextHolder`, then `getPrincipal()`. `@EnableWebSecurity` adds it through Security’s `WebMvcConfigurer`. If you extend **`WebMvcConfigurationSupport`** yourself, that auto-config is skipped and you must register the resolver.

`expression` is SpEL with the **principal as root** (`"customUser"`, `"claims['sub']"`, even `"@jpaEntityManager.merge(#this)"`). Meta-annotate your own `@CurrentUser` so controllers do not import Security. For the whole `Authentication` or `SecurityContext`, use **`@CurrentSecurityContext`**, not this annotation.

`java.security.Principal` on a handler is the servlet principal (`Authentication` implements it); `getName()` is the username, not your domain user. Compare: [[What is the difference between Principal and UserDetails]].

```java
@GetMapping("/messages/inbox")
public ModelAndView inbox(@AuthenticationPrincipal CustomUser user) {
    return findMessages(user);
}

@GetMapping("/me")
public CustomUser me(
        @AuthenticationPrincipal(expression = "customUser") CustomUser user) {
    return user;
}
```

**Listing 1.** Conceptual handlers from Spring Security reference. Type-level `@EnableWebSecurity`: [[What is the purpose of EnableWebSecurity]]. Domain user type: [[What is UserDetails and UserDetailsService in Spring Security]].

```d2
direction: down
ctx: "SecurityContextHolder" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
auth: "Authentication" {
  width: 200
  height: 40
  style.fill: "#fff3e0"
}
prin: "getPrincipal()\nUserDetails / custom" {
  width: 240
  height: 55
  style.fill: "#e8f5e9"
}
arg: "@AuthenticationPrincipal param" {
  width: 260
  height: 45
  style.fill: "#fce4ec"
}

ctx -> auth
auth -> prin
prin -> arg
```

**Fig. 1.** Argument resolver copies the principal object into the controller method. It does not run authorization.

> [!warning] Wrong type is silent `null`
> Anonymous principal is often a **`String`**. A `CustomUser` parameter then becomes **null** (`errorOnInvalidType` default **false**). That flag is **not** “fail if unauthenticated” — it only throws on a **type** mismatch.

> [!warning] Controllers only (plus `@MessageMapping`)
> The annotation is a **`HandlerMethodArgumentResolver`**. It does nothing on `@Service` methods. Use method security or pass the user in: [[How does method security work in Spring]].

> [!warning] `@Async` vs MVC `Callable`
> Returning **`Callable`** from a controller **does** copy the `SecurityContext` onto the async thread. **`@Async` services do not.** This annotation still only binds at the **MVC** (or STOMP) call.

> [!tip] Interview answer
> **`@AuthenticationPrincipal` injects `Authentication.getPrincipal()` into a controller argument.** Prefer it over `SecurityContextHolder` in web code. Null if missing or wrong type; `errorOnInvalidType` turns the mismatch into `ClassCastException`. SpEL `expression` unwraps nested user objects.
