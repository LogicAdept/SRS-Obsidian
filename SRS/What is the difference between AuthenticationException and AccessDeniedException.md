<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/MethodSecurity #SRS

# What is the difference between AuthenticationException and AccessDeniedException?

> [!abstract] Short answer
> **`AuthenticationException`** means the caller is **not successfully authenticated** (missing login, failed credentials, too-weak trust). **`ExceptionTranslationFilter`** sends that to **`AuthenticationEntryPoint`** (form: **login redirect**; Basic: **401**). **`AccessDeniedException`** means **authorization failed**: the principal is known but **not allowed**. For a **fully authenticated** user that is **`AccessDeniedHandler`** (**403**). If the token is **anonymous or remember-me**, the filter **does not** treat it as a final 403 — it wraps **`InsufficientAuthenticationException`** (an **`AuthenticationException`**) and **commences** login instead.

## Who you are versus what you may do

They are **sibling** runtime types, not a parent/child pair. **`AuthenticationException`** is thrown by **`AuthenticationManager` / `AuthenticationProvider`** (and by filters that call them). **`AccessDeniedException`** is thrown by **`AuthorizationFilter`**, method security (**`@PreAuthorize`**, **`@Secured`**), and CSRF (**`InvalidCsrfTokenException`**). **`AuthorizationDeniedException`** (**since 6.3**) **extends `AccessDeniedException`** — still authorization, not authentication ([[What is AuthenticationEntryPoint]], [[What is AccessDeniedHandler]], [[What is ExceptionTranslationFilter in Spring Security]]).

**`ExceptionTranslationFilter`** (via **`AuthenticationTrustResolver`**):

| Thrown | Current `Authentication` | Handler | Typical HTTP |
| --- | --- | --- | --- |
| **`AuthenticationException`** | any / none | **`AuthenticationEntryPoint.commence`** | **302** `/login`, or **401** |
| **`AccessDeniedException`** | **anonymous** or **remember-me** | Wrap **`InsufficientAuthenticationException`**, then **entry point** | Same as unauthenticated |
| **`AccessDeniedException`** | **fully authenticated** (`isFullyAuthenticated`, **since 6.1**) | **`AccessDeniedHandler.handle`** | **403** |

**`isAnonymous`** javadoc is explicit: if the principal is **non-anonymous**, ADE is a **final rejection**; if the token is **merely anonymous**, direct them to **actual authentication**. Remember-me is the same “not fully trusted” bucket (**`InsufficientAuthenticationException`** javadoc). Failed **form POST** never reaches this filter: **`AuthenticationFailureHandler`** (**`/login?error`**) ([[What is AuthenticationFailureHandler]], [[How do you handle authentication exceptions in Spring Security]]).

With **neither** form nor Basic, the default entry point is **`Http403ForbiddenEntryPoint`** — unauthenticated access is **403**, not 401. Status codes **overlap**; the **exception type** still tells you authentication vs authorization.

```java
http
	.authorizeHttpRequests((authorize) -> authorize
		.requestMatchers("/admin/**").hasRole("ADMIN")
		.anyRequest().authenticated())
	.formLogin(Customizer.withDefaults())
	.exceptionHandling((exceptions) -> exceptions
		.accessDeniedPage("/errors/access-denied"));
```

**Listing 1.** Anonymous hit on `/admin` → **login**. Logged-in **`USER`** on `/admin` → **403** / access-denied page. Same URL, two exception types.

```java
@PreAuthorize("hasRole('ADMIN')")
public void deleteAll() { }
```

**Listing 2.** A logged-in caller who fails this check throws **`AccessDeniedException`** (often **`AuthorizationDeniedException`**), **not** **`AuthenticationException`**.

```d2
direction: down
ae: "AuthenticationException" {
  width: 260
  height: 50
  style.fill: "#e3f2fd"
}
ade: "AccessDeniedException" {
  width: 260
  height: 50
  style.fill: "#fff3e0"
}
trust: "anonymous or remember-me?" {
  width: 260
  height: 50
  style.fill: "#fff8e1"
}
ep: "AuthenticationEntryPoint\nlogin / 401" {
  width: 240
  height: 70
  style.fill: "#f3e5f5"
}
adh: "AccessDeniedHandler\n403" {
  width: 220
  height: 70
  style.fill: "#e8f5e9"
}

ae -> ep
ade -> trust
trust -> ep: "yes"
trust -> adh: "no (fully authenticated)"
```

**Fig. 1.** **`AccessDeniedException`** is **not** always 403. Trust level decides.

> [!warning] Anonymous ADE is a login challenge
> **`AnonymousAuthenticationToken`** is **`isAuthenticated() == true`**, so dumps that say “authenticated → 403” are wrong for anonymous and remember-me. **`@PreAuthorize` failure for a real user is ADE / 403**, not a second login. Catching only **`AuthenticationException`** in MVC advice **misses** method-security denials.

> [!warning] Default entry point may already be 403
> Without **`formLogin` / `httpBasic`**, unauthenticated **`AuthenticationException`** handling is **`Http403ForbiddenEntryPoint`**. Seeing **403** does not prove **`AccessDeniedException`**. CSRF invalid tokens are **ADE** handled **directly** by **`CsrfFilter`**, still **403** for a session user ([[What is CsrfFilter in Spring Security]], [[How do you customize the access denied page in Spring Security]]).

> [!tip] Interview answer
> AuthenticationException is “we do not accept who you are” — login challenge or 401. AccessDeniedException is “we know who you are and you may not do this” — 403 for a fully authenticated user. Anonymous and remember-me AccessDeniedException is rewritten to InsufficientAuthenticationException so the entry point runs. Method security failed @PreAuthorize throws AccessDeniedException, not AuthenticationException.
