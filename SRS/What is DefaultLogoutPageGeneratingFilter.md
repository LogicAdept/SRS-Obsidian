<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `DefaultLogoutPageGeneratingFilter`?

> [!abstract] Short answer
> An **`OncePerRequestFilter`** (since 5.1) that **renders the default logout confirmation HTML**. With CSRF **on** (the default), **`GET /logout`** shows that page (CSRF hidden field + POST form). **`POST /logout`** is **`LogoutFilter`**, not this class — it invalidates the session and redirects to **`/login?logout`**. Sibling of **`DefaultLoginPageGeneratingFilter`**. CSRF **off** → **no** confirmation page; GET logs out immediately. A custom **`logoutSuccessUrl`** or SPA **`HttpStatusReturningLogoutSuccessHandler`** never uses this HTML for the **success** step.

## GET confirms; POST logs out

```d2
direction: down
get: "GET /logout\nCSRF enabled?" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
page: "DefaultLogoutPageGeneratingFilter\nHTML + CSRF field" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
post: "LogoutFilter\nPOST /logout" {
  width: 220
  height: 40
  style.fill: "#fff3e0"
}
redir: "LogoutSuccessHandler\n/login?logout" {
  width: 240
  height: 40
  style.fill: "#fce4ec"
}

get -> page: "yes"
get -> post: "CSRF disabled"
page -> post: "form POST"
post -> redir
```

**Fig. 1.** Logout chapter: confirmation is a CSRF convenience, not the logout itself. `LogoutFilter` is **before** `AuthorizationFilter`, so default `/logout` needs **no** `permitAll`. See [[What is CsrfFilter in Spring Security]] and [[What is AuthorizationFilter in Spring Security]].

Architecture default list: `LogoutFilter`, then login page generator, then **this** filter. Hidden CSRF inputs: **`setResolveHiddenInputs`**, same idea as the login generator. See [[What is DefaultLoginPageGeneratingFilter]].

```java
http.logout(Customizer.withDefaults()); // GET /logout → HTML; POST → /login?logout

http.logout((logout) -> logout
        .logoutSuccessUrl("/my/success")
        .permitAll()); // MVC success page — not the generated HTML
```

**Listing 1.** `logout` is on with `@EnableWebSecurity`. Custom success URLs live **after** `LogoutFilter` (DispatcherServlet) and need `permitAll` or `logout.permitAll()`. Prefer **POST `/logout`** with a CSRF token; you do not need GET.

> [!warning] This is not LogoutFilter
> Changing **`logoutSuccessUrl`** or using a **401/204 success handler** skips this page on **success**. **`csrf.disable()`** skips it on **GET** and logs the user out with no confirm — fine for JWT APIs, dangerous if a browser still has a session cookie.

> [!tip] Interview answer
> DefaultLogoutPageGeneratingFilter only paints the GET /logout confirmation form so CSRF can POST. LogoutFilter does the real logout and redirects to /login?logout. Custom success URLs and CSRF-off APIs never show that HTML.
