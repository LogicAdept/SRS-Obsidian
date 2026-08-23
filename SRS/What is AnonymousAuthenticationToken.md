<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS

# What is AnonymousAuthenticationToken?

> [!abstract] Short answer
> **AnonymousAuthenticationToken** is Spring Security’s **`Authentication`** implementation for unauthenticated requests. **`AnonymousAuthenticationFilter`** installs one in **`SecurityContextHolder`** when no real authentication exists, with principal **`anonymousUser`** and authority **`ROLE_ANONYMOUS`**.

## How it gets into the context

Three components cooperate:

1. **`AnonymousAuthenticationFilter`** — runs after normal authentication filters; if `SecurityContextHolder` has no `Authentication`, it creates an **`AnonymousAuthenticationToken`** and stores it in the context.
2. **`AnonymousAuthenticationProvider`** — registered in **`ProviderManager`** so anonymous tokens are recognized.
3. **`AnonymousAuthenticationToken`** — holds the anonymous principal and its **`GrantedAuthority`** list.

The filter’s no-arg constructor uses principal **`anonymousUser`** and authority **`ROLE_ANONYMOUS`**. Filter and provider share a **`key`** so only tokens created by the authorized filter are accepted.

```d2
direction: right
req: "Unauthenticated\nHTTP request" {
  width: 190
  height: 70
  style.fill: "#e3f2fd"
}
filter: "AnonymousAuthenticationFilter" {
  width: 230
  height: 70
  style.fill: "#fff3e0"
}
token: "AnonymousAuthenticationToken\nanonymousUser\nROLE_ANONYMOUS" {
  width: 240
  height: 90
  style.fill: "#e8f5e9"
}
ctx: "SecurityContextHolder\n(non-null Authentication)" {
  width: 230
  height: 70
  style.fill: "#fce4ec"
}

req -> filter -> token -> ctx
```

**Fig. 1.** Anonymous authentication guarantees every request carries an `Authentication` object, not `null`.

## The `isAuthenticated()` trap

The token’s constructor calls **`setAuthenticated(true)`**. So **`isAuthenticated()` returns `true`** even though the user is not logged in. That is intentional: authorization rules can reference **`ROLE_ANONYMOUS`**, and components like **`ExceptionTranslationFilter`** can distinguish anonymous from fully authenticated users via **`AuthenticationTrustResolver#isAnonymous`**.

To detect anonymous access in application code, check the token type (or use the trust resolver) — **not** `authentication == null`:

```java
@GetMapping("/")
public String check(@CurrentSecurityContext SecurityContext context) {
    if (context.getAuthentication() instanceof AnonymousAuthenticationToken) {
        return "anonymous";
    }
    return "authenticated";
}
```

**Listing 1.** `@CurrentSecurityContext` reads the security context; a plain `Authentication` MVC parameter resolves via `HttpServletRequest#getPrincipal`, which stays **`null`** for anonymous requests.

> [!warning] Do not treat `isAuthenticated()` as “logged in”
> A request with only an **`AnonymousAuthenticationToken`** reports **`isAuthenticated() == true`** but has no real credentials (`getCredentials()` is an empty string). URL rules like **`hasRole('USER')`** reject it; rules allowing **`ROLE_ANONYMOUS`** accept it. **`ExceptionTranslationFilter`** uses **`AuthenticationTrustResolver`** so anonymous users get redirected to login (via **`AuthenticationEntryPoint`**) instead of a bare 403 when access is denied.

See [[What is the difference between ROLE_USER and ROLE_ANONYMOUS]] and [[What is AnonymousAuthenticationFilter]].

> [!tip] Interview answer
> AnonymousAuthenticationToken is the placeholder Authentication Spring Security puts in the context for guests — principal anonymousUser, authority ROLE_ANONYMOUS. Authentication is never null after the filter runs, but isAuthenticated is true on the token, so detect anonymity with instanceof or AuthenticationTrustResolver, not with a null check.
