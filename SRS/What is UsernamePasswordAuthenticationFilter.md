<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Security/Authentication #SRS

# What is `UsernamePasswordAuthenticationFilter`?

> [!abstract] Short answer
> The **form-login** filter (`http.formLogin()`). It extends [[What is AbstractAuthenticationProcessingFilter]], runs on **`POST /login`** by default (`postOnly` **true**), reads form fields **`username`** and **`password`**, builds a **`UsernamePasswordAuthenticationToken`**, and calls **`AuthenticationManager`**. It is **not** [[What is BasicAuthenticationFilter]] (header, every request) and **not** the GET login **page** ([[What is DefaultLoginPageGeneratingFilter]]). Architecture TRACE: after [[What is LogoutFilter]], before Basic. Custom JWT filters typically **`addFilterBefore(..., UsernamePasswordAuthenticationFilter.class)`**.

## Form POST, then `AuthenticationManager`

```d2
direction: down
post: "POST /login\nusername + password" {
  width: 240
  height: 50
}
upaf: "UsernamePasswordAuthenticationFilter" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
am: "AuthenticationManager" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}

post -> upaf
upaf -> am: "attemptAuthentication"
```

**Fig. 1.** Called `AuthenticationProcessingFilter` before Spring Security **3.0**. Parameter names default to `username` / `password` (`SPRING_SECURITY_FORM_*_KEY`). Other requests skip this filter. See [[What is DaoAuthenticationProvider]], [[What is CsrfFilter in Spring Security]] (CSRF still applies to this POST), and [[What is FilterOrderRegistration]].

Success **redirects** (saved request or `/`); it does **not** continue like Basic. Failure goes to `/login?error` unless you set a failure handler.

```java
http.formLogin(Customizer.withDefaults());

http.addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class);
```

**Listing 1.** First line installs this filter. Second is the documented custom-filter landmark — the class is **always** in the order table even if form login is off. See [[How do you disable form login on a SecurityFilterChain]], [[How do you implement a custom security filter in Spring Security]], and [[What is the difference between addFilterBefore addFilterAfter and addFilterAt]].

> [!warning] Do not landmark on Basic in a form-login app
> `addFilterBefore(f, BasicAuthenticationFilter.class)` lands **after** this filter (login pages and Bearer sit in between). In a UI-only chain Basic may not even be present. Use **`UsernamePasswordAuthenticationFilter.class`** (or Logout) so a token filter still runs in the authentication phase — see [[Why must a JWT filter run before AnonymousAuthenticationFilter]].

> [!tip] Interview answer
> UsernamePasswordAuthenticationFilter is the form-login filter: POST /login, username and password parameters, UsernamePasswordAuthenticationToken, AuthenticationManager. http.formLogin adds it. It is the usual addFilterBefore landmark for a custom JWT filter. It is not BasicAuthenticationFilter and not the generated GET /login page.
