<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/CSRF #SRS

# How does form login work internally in Spring Security?

> [!abstract] Short answer
> Unauthenticated HTML hits **`ExceptionTranslationFilter`**, which **`RequestCache`s** the request and **`LoginUrlAuthenticationEntryPoint`** sends **GET `/login`**. The user **POSTs** `username`, `password`, and a **CSRF** token to **`/login`**. **`UsernamePasswordAuthenticationFilter`** (POST-only) builds **`UsernamePasswordAuthenticationToken.unauthenticated`**, then **`AuthenticationManager` → `ProviderManager` → `DaoAuthenticationProvider`**. Success: session + **`SecurityContext`**, **`FACTOR_PASSWORD`**, then **`SavedRequestAwareAuthenticationSuccessHandler`** (original URL or `/`). Failure never reaches the translation filter: **`AuthenticationFailureHandler`** redirects to **`/login?error`**. This is **cookie-session** login, not a JWT filter.

## Entry point, then POST `/login`, then the manager

`formLogin(Customizer)` registers **`LoginUrlAuthenticationEntryPoint`**, **`UsernamePasswordAuthenticationFilter`**, and (unless **`loginPage`** is set) **`DefaultLoginPageGeneratingFilter`**. Defaults: **GET `/login`** form, **POST `/login`** process, **GET `/login?error`**, **GET `/login?logout`** ([[How do you create a custom login form in Spring Security]], [[What is UsernamePasswordAuthenticationFilter]]).

**Commence (not a failed POST).** Anonymous access to a protected resource → **`AuthorizationFilter`** → **`AccessDeniedException`** → **`ExceptionTranslationFilter`** treats anonymous/remember-me as **start authentication**: save **`HttpSessionRequestCache`**, **`LoginUrlAuthenticationEntryPoint`** redirects to the login page ([[What is ExceptionTranslationFilter in Spring Security]]).

**Submit.** **`CsrfFilter`** runs **before** the login filter. The login filter’s matcher is **`POST /login`** (`postOnly` **true**; other methods → **`AuthenticationServiceException`**). **`attemptAuthentication`**: trim username (null → `""`), password null → `""`, **`UsernamePasswordAuthenticationToken.unauthenticated(username, password)`**, **`WebAuthenticationDetails`** on **`details`**, then **`getAuthenticationManager().authenticate`** ([[What is UsernamePasswordAuthenticationToken]], [[What is AuthenticationManager and AuthenticationProvider in Spring Security]], [[What is DaoAuthenticationProvider]], [[What is CsrfFilter in Spring Security]]).

**Provider.** Typical **`DaoAuthenticationProvider`**: **`UserDetailsService.loadUserByUsername`**, **`PasswordEncoder.matches`**, account-status checks. Success **`Authentication`** includes **`FactorGrantedAuthority.PASSWORD_AUTHORITY`** (**7.0+**).

**After the manager (`AbstractAuthenticationProcessingFilter`).** Success: **`SessionAuthenticationStrategy`** (session fixation), merge authorities if already authenticated, set **`SecurityContextHolder`**, **`SecurityContextRepository.saveContext`** (session by default), **`RememberMeServices.loginSuccess`**, **`InteractiveAuthenticationSuccessEvent`**, **`SavedRequestAwareAuthenticationSuccessHandler`** — saved request, else **`defaultSuccessUrl`** (`/`). Failure: clear context, store the exception for the view, **`RememberMeServices.loginFail`**, **`SimpleUrlAuthenticationFailureHandler`** → **`/login?error`**. That **`AuthenticationException`** is **not** handled by **`ExceptionTranslationFilter`** ([[How do you handle authentication exceptions in Spring Security]], [[What is AuthenticationFailureHandler]]).

```java
UsernamePasswordAuthenticationToken authRequest =
		UsernamePasswordAuthenticationToken.unauthenticated(username, password);
authRequest.setDetails(this.authenticationDetailsSource.buildDetails(request));
return this.getAuthenticationManager().authenticate(authRequest);
```

**Listing 1.** Core of **`UsernamePasswordAuthenticationFilter.attemptAuthentication`**. Parameter names default to **`username`** / **`password`**.

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.formLogin(Customizer.withDefaults());
```

**Listing 2.** That **`Customizer`** is what stands up the filter, entry point, generated login page, and **`/login?error`** failure URL.

```d2
direction: down
deny: "AuthorizationFilter\nanonymous" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
etf: "ExceptionTranslationFilter\nRequestCache + login redirect" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
csrf: "CsrfFilter then\nPOST /login" {
  width: 220
  height: 50
  style.fill: "#fce4ec"
}
upaf: "UsernamePasswordAuthenticationFilter\nunauthenticated token" {
  width: 280
  height: 70
  style.fill: "#fff8e1"
}
am: "AuthenticationManager\nDaoAuthenticationProvider" {
  width: 260
  height: 70
  style.fill: "#e8f5e9"
}
ok: "save SecurityContext\nSavedRequest redirect" {
  width: 240
  height: 70
  style.fill: "#f3e5f5"
}
fail: "AuthenticationFailureHandler\n/login?error" {
  width: 240
  height: 70
  style.fill: "#ffcdd2"
}

deny -> etf -> csrf -> upaf -> am
am -> ok: "success"
am -> fail: "AuthenticationException"
```

**Fig. 1.** Entry point **starts** login. The processing filter **owns** success and failure. The translation filter is idle during **POST `/login`**.

> [!warning] Failed POST is not ExceptionTranslationFilter
> A bad password is **`AuthenticationFailureHandler`**, not **`AuthenticationEntryPoint`**. Confusing those two is how APIs get a **login HTML redirect** on **401** paths. **GET `/login`** is the form; **POST `/login`** is the only default processing method. Missing CSRF is **403** via **`AccessDeniedHandler`**, not **`BadCredentialsException`**.

> [!warning] Not a per-request API filter
> Form login writes a **session cookie**. **`SessionCreationPolicy.STATELESS`** plus **`formLogin`** still runs this filter on **POST `/login`**, but there is **no session** to restore on the next API call — that is bearer/`AuthenticationFilter` territory. Setting **`loginPage`** **stops** the generated form; you then own GET `/login` and **`permitAll`**.

> [!tip] Interview answer
> Unauthenticated browser requests are redirected by LoginUrlAuthenticationEntryPoint; the form POSTs username and password to /login. UsernamePasswordAuthenticationFilter builds an unauthenticated UsernamePasswordAuthenticationToken and AuthenticationManager (usually DaoAuthenticationProvider) verifies UserDetails and the PasswordEncoder. Success saves the SecurityContext in the session and SavedRequestAwareAuthenticationSuccessHandler returns the user to the original URL; failure goes to /login?error through AuthenticationFailureHandler, not ExceptionTranslationFilter.
