<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #SRS

# What exception does a failed method-security check throw?

> [!abstract] Short answer
> **`AccessDeniedException`** (`org.springframework.security.access`). Since Security **6.3** the default handler (`ThrowingMethodAuthorizationDeniedHandler`) throws **`AuthorizationDeniedException`**, a subclass that carries an `AuthorizationResult`. Catch or assert **`AccessDeniedException`** — it still matches. An empty `SecurityContextHolder` is different: **`AuthenticationCredentialsNotFoundException`** (an `AuthenticationException`).

## When it is thrown

`AuthorizationManagerBeforeMethodInterceptor` (`@PreAuthorize`, `@Secured`, JSR-250) publishes `AuthorizationDeniedEvent` and throws **before** the target runs. `AuthorizationManagerAfterMethodInterceptor` (`@PostAuthorize`) does the same **after** a normal return — the body **already ran** (side effects and writes are done). Official tests use `assertThatExceptionOfType(AccessDeniedException.class)`.

`@HandleAuthorizationDenied` can replace the throw with a masked/default return. That is the exception to “always throws.”

```java
@PreAuthorize("hasRole('ADMIN')")
public Account read(String id) { return load(id); }

@WithMockUser(roles = "WRONG")
@Test
void readWhenWrongRoleThenAccessDenied() {
    assertThatExceptionOfType(AccessDeniedException.class)
            .isThrownBy(() -> this.bankService.read("12345678"));
}
```

**Listing 1.** Conceptual Security **7.1** sample — failed SpEL/role check. `roles = "WRONG"` is not `ROLE_ADMIN`. Import `org.springframework.security.access.AccessDeniedException`, not `java.nio.file.AccessDeniedException`.

```d2
direction: down
pre: "@PreAuthorize deny\nAuthorizationDeniedException\nbody skipped" {
  width: 260
  height: 60
  style.fill: "#ffcdd2"
}
post: "@PostAuthorize deny\nsame exception\nbody already ran" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
http: "ExceptionTranslationFilter\nauthenticated → 403\nanonymous → entry point" {
  width: 280
  height: 70
  style.fill: "#e3f2fd"
}

pre -> http
post -> http
```

**Fig. 1.** The check throws a Java exception. HTTP status exists only if `ExceptionTranslationFilter` sees it.

On the servlet stack, `ExceptionTranslationFilter` wraps the rest of the app (including method security). **Authenticated** `AccessDeniedException` → `AccessDeniedHandler` (typically **403**). **Not authenticated** or any `AuthenticationException` → `AuthenticationEntryPoint` (form login redirect or **401**, not always 401). Anonymous method-security denial is the first branch. No HTTP request: handle `AccessDeniedException` yourself — [[Can method security run without a SecurityFilterChain]], [[How does method security work in Spring]], [[What is ExceptionTranslationFilter in Spring Security]].

> [!warning] `catch (Exception)` hides the 403
> `AccessDeniedException` is a **`RuntimeException`**. A broad `catch (Exception)` around a service call swallows it, so `ExceptionTranslationFilter` never runs and the client never gets 403. Catch `AccessDeniedException` (or let it propagate). Empty `SecurityContext` is `AuthenticationCredentialsNotFoundException`, not `AccessDeniedException`.

> [!tip] Interview answer
> A failed method-security check throws `AccessDeniedException` — in 6.3+ usually the subclass `AuthorizationDeniedException`. `@PreAuthorize` skips the body; `@PostAuthorize` runs it first. On the web, `ExceptionTranslationFilter` maps an authenticated denial to 403 and anonymous/missing auth to the entry point; `catch (Exception)` swallows the exception so you never get that status.
