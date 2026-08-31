<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `DefaultLoginPageGeneratingFilter`?

> [!abstract] Short answer
> The filter that **renders** the auto-generated **HTML login page** at **`/login`** when you use **`formLogin()`** and do **not** set **`loginPage(...)`**. It does **not** redirect anonymous users there. **`AuthorizationFilter`** denies, **`ExceptionTranslationFilter`** + **`LoginUrlAuthenticationEntryPoint`** **redirect**, then this filter **writes HTML**. Namespace: convenience only — **not intended for production**. `loginPage("/my-login")` **turns the generator off**; you must supply the view and `permitAll` that URL.

## Render `/login`, do not start login

```d2
direction: down
deny: "AuthorizationFilter deny\n(anonymous)" {
  width: 240
  height: 50
  style.fill: "#fff3e0"
}
etf: "ExceptionTranslationFilter\nLoginUrlAuthenticationEntryPoint" {
  width: 300
  height: 50
  style.fill: "#e3f2fd"
}
gen: "DefaultLoginPageGeneratingFilter\nGET /login HTML" {
  width: 280
  height: 50
  style.fill: "#e8f5e9"
}
upaf: "UsernamePasswordAuthenticationFilter\nPOST /login" {
  width: 300
  height: 50
  style.fill: "#fce4ec"
}

deny -> etf: "redirect"
etf -> gen
gen -> upaf: "form submit"
```

**Fig. 1.** Javadoc: **only works if a redirect** is used to the login page. Dump mixing this filter with `AuthorizationFilter` as “the redirect” is wrong. See [[How does Spring Security authenticate an HTTP request end to end]] and [[What is ExceptionTranslationFilter in Spring Security]].

`http.formLogin(Customizer.withDefaults())` generates `/login` and `/login?error` on failure. Hidden CSRF fields come from **`setResolveHiddenInputs`**. The same page can show **form login and/or OIDC** (and OTT, SAML2, passkeys when those DSLs are on). It sits **after** `UsernamePasswordAuthenticationFilter` in the default list so **POST `/login`** is not swallowed as HTML. See [[What is AbstractAuthenticationProcessingFilter]] and [[What is CsrfFilter in Spring Security]].

```java
http.formLogin(Customizer.withDefaults()); // DefaultLoginPageGeneratingFilter on

http.formLogin((form) -> form.loginPage("/authentication/login")); // generator off
```

**Listing 1.** `HttpSecurity.formLogin`. Custom `loginPage` needs your own controller/view and a `requestMatchers` **`permitAll`**. See [[How do you disable form login on a SecurityFilterChain]].

> [!warning] REST clients get HTML, not 401
> Form login’s entry point **wins** over Basic’s if both are on. An API call then **302 → `/login` HTML**. Use a JSON/401 entry point (or a separate JWT chain) for APIs. Namespace: do not ship this generated page as the production UI.

> [!tip] Interview answer
> DefaultLoginPageGeneratingFilter only renders the default /login HTML when formLogin has no custom loginPage. The redirect to that URL is LoginUrlAuthenticationEntryPoint after ExceptionTranslationFilter. Custom loginPage disables it. APIs that hit this chain get HTML instead of 401.
