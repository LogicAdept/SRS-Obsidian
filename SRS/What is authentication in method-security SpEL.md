<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Security/Authentication #SRS

# What is authentication in method-security SpEL?

> [!abstract] Short answer
> **`authentication` is the current `Authentication` on the SpEL root** (`SecurityExpressionRoot` / `MethodSecurityExpressionRoot`). It is the same object `SecurityContextHolder` holds for this invocation. **`authentication.name`** is `Principal.getName()` (typically the username). **`principal`** is `Authentication.getPrincipal()` — often a `UserDetails`, sometimes a JWT claims object (`principal.claims['aud']`).

## What the root exposes

When `@EnableMethodSecurity` evaluates `@PreAuthorize`, `@PostAuthorize`, `@PreFilter`, or `@PostFilter`, `MethodSecurityExpressionHandler` builds a `MethodSecurityEvaluationContext` whose root is `MethodSecurityExpressionRoot`. Official fields:

| SpEL | Meaning |
|---|---|
| `authentication` | The `Authentication` for this call |
| `principal` | `authentication.principal` (`getPrincipal()`) |
| `authentication.name` | `getName()` on that `Authentication` (`Principal`) |
| `authentication.authorities` | `getAuthorities()` — never `null` |

Built-in methods that **read** that object: `hasRole` / `hasAuthority`, `isAuthenticated()`, `isAnonymous()`, `isRememberMe()`, `isFullyAuthenticated()`. `permitAll` / `denyAll` do **not** load `Authentication`.

`Authentication` is a `Principal`. After a successful login, providers often put a **`UserDetails`** in `principal`. That is a convention, not a type guarantee — JWT samples use `principal.claims['aud']`.

```java
@PostAuthorize("returnObject.owner == authentication.name")
public Account readAccount(String id) { return load(id); }

@PreAuthorize("#n == authentication.name")
Contact findContactByName(@Param("n") String name);

@PreAuthorize("principal.claims['aud'] == 'my-audience'")
public Resource readResource();

@PreAuthorize("@authz.check(authentication, #root)")
public Resource shareResource();
```

**Listing 1.** Conceptual Security **7.1** — `authentication` in pre/post/filter SpEL. `#n` still needs parameter-name discovery — [[Can PreAuthorize use method parameters]].

```d2
direction: down
ctx: "SecurityContextHolder\nAuthentication" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
root: "MethodSecurityExpressionRoot\nauthentication / principal" {
  width: 280
  height: 55
  style.fill: "#fff3e0"
}
spel: "@PreAuthorize / @PostAuthorize\nauthentication.name" {
  width: 280
  height: 55
  style.fill: "#e8f5e9"
}

ctx -> root -> spel
```

**Fig. 1.** SpEL does not invent a user. It reads the thread’s `Authentication`. See [[What is PreAuthorize]], [[How does method security work in Spring]], [[What is AuthenticationPrincipal]].

> [!warning] Anonymous is an `Authentication`, not `null`
> `AnonymousAuthenticationFilter` puts an `AnonymousAuthenticationToken` in the context when nothing else authenticated (`anonymousUser`, `ROLE_ANONYMOUS`). Servlet `getUserPrincipal()` can still be **null**. In SpEL use **`isAnonymous()`** / **`isAuthenticated()`**, not `authentication == null`. A **direct** service call with an empty `SecurityContext` is the other hole: **`AuthenticationCredentialsNotFoundException`**, not a null `authentication` — [[What is WithAnonymousUser]], [[What exception does a failed method-security check throw]].

> [!tip] Interview answer
> In method-security SpEL, `authentication` is the current `Authentication`. `authentication.name` is the principal name; `principal` is `getPrincipal()`, often `UserDetails` but not always. On the web, anonymous is still an `Authentication` — use `isAuthenticated()` / `isAnonymous()`, not a null check.
