<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/CSRF #SRS

# How do you create a custom login form in Spring Security?

> [!abstract] Short answer
> Set **`formLogin(form -> form.loginPage("/login").permitAll())`**, map **`GET /login`** to your HTML, and **`POST /login`** with fields **`username`**, **`password`**, and a **CSRF** token. Specifying **`loginPage`** **stops** the generated login page — you own rendering. **`permitAll()`** on that config (or on `/login`) is required or unauthenticated users **redirect-loop**. CSRF is **on** for cookie sessions; a missing token is **403**.

## You render GET; the filter authenticates POST

Unauthenticated HTML → **`LoginUrlAuthenticationEntryPoint`** → login page. Submit → **`UsernamePasswordAuthenticationFilter`** (default URL **`/login`**, **POST only**) builds a **`UsernamePasswordAuthenticationToken`** and calls **`AuthenticationManager`**. Failure: **`/login?error`**. Logout success: **`/login?logout`**. Success: saved request ([[What is loginPage in form login]], [[What is the default login URL in Spring Security]], [[How do you use form login authentication in Spring Boot]]).

Once **`loginPage`** is set, Spring Security **does not** generate a form. Provide a controller and a template.

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http
		.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
		.formLogin((form) -> form.loginPage("/login").permitAll());
	return http.build();
}
```

```java
@Controller
class LoginController {
	@GetMapping("/login")
	String login() {
		return "login";
	}
}
```

**Listing 1.** Current DSL (**3.2+**). XML: `<form-login login-page="/login"/>` plus **`permitAll`** on `/login`. Do **not** use **`authorizeRequests()`** / **`.and()`** / **`WebSecurityConfigurerAdapter`** ([[Why was WebSecurityConfigurerAdapter removed]]).

`loginPage` and **`loginProcessingUrl`** are matched **literally**. If the dispatcher is under `/api/*`, set **both** to `/api/login`.

```html
<form method="post" action="/login">
	<input type="text" name="username"/>
	<input type="password" name="password"/>
	<input type="submit" value="Log in"/>
</form>
```

**Listing 2.** Contract for **`UsernamePasswordAuthenticationFilter`**: **POST**, parameter names **`username`** / **`password`** (overridable with **`usernameParameter` / `passwordParameter`**). Thymeleaf **`th:action="@{/login}"`** inserts CSRF. Plain JSP must add a hidden field from the **`_csrf`** request attribute (`parameterName` / `token`). Query **`error`** = bad credentials; **`logout`** = just logged out.

```d2
direction: down
get: "GET /private\nunauthenticated" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
page: "GET /login\nyour controller + HTML" {
  width: 260
  height: 60
  style.fill: "#fff3e0"
}
post: "POST /login\nUsernamePasswordAuthenticationFilter" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
ok: "SecurityContext + redirect\nto saved request" {
  width: 260
  height: 60
  style.fill: "#f3e5f5"
}

get -> page -> post -> ok
```

**Fig. 1.** Custom form is still session form-login, not HTTP Basic or JWT ([[When should you use HTTP Basic versus form login]]). Optional: `defaultSuccessUrl`, `failureUrl`, `loginProcessingUrl`.

> [!warning] Skip `permitAll` and you never see the form
> **`GET /login`** (and the processing URL) must be reachable **without** authentication. **`formLogin(...).permitAll()`** does that. If `/login` itself requires a login, the entry point redirects to `/login` again.

> [!warning] CSRF on login is intentional; missing token is 403
> Spring Security **requires CSRF for login** (forged login / session fixation). Invalid or absent token → **403**, not a polite `?error`. Do **not** disable CSRF to “fix” the form. Setting **`loginPage`** also **removes** the generated page — a `securityMatcher` that **omits** `/login` yields **404** on the filter’s endpoints.

> [!tip] Interview answer
> I keep formLogin but set loginPage to my URL and permitAll so guests can load it. I map GET /login to a template that POSTs username and password to /login with a CSRF token. Thymeleaf’s th:action adds the token; a raw HTML form must include the _csrf hidden field. Once loginPage is set, Security stops generating a default form.
