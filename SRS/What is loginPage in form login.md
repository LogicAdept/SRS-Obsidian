<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/CSRF #SRS

# What is loginPage in form login?

> [!abstract] Short answer
> **`formLogin.loginPage(String)`** is the **GET URL** **`LoginUrlAuthenticationEntryPoint`** redirects to when login is required. If you **omit** it, Spring **generates** a page at **`GET /login`**. If you **set** it, you **render** that URL yourself and the generated page is **off**. Official defaults then **move with that path**: **`POST` the same URL** authenticates, **`?error`** is failure, **`?logout`** is logout success — unless you set **`loginProcessingUrl` / `failureUrl` / logout success** yourself. **`permitAll()`** on form login (or those URLs) is required or the redirect **loops**. The form still needs **`username`**, **`password`**, and a **CSRF** token.

## Redirect target, then a family of defaults

**`FormLoginConfigurer`** (**since 3.2**): no **`loginPage`** → **`DefaultLoginPageGeneratingFilter`** at **`/login`**. Specifying a URL sets **`customLoginPage`**, points the entry point at that path, and **`updateAuthenticationDefaults()`** fills gaps ([[How does form login work internally in Spring Security]], [[What is AuthenticationEntryPoint]], [[What is the default login URL in Spring Security]]):

| If you only pass `loginPage("/authenticate")` | Meaning |
| --- | --- |
| **`GET /authenticate`** | Your form |
| **`POST /authenticate`** | **`UsernamePasswordAuthenticationFilter`** (still **POST-only**) |
| **`GET /authenticate?error`** | **`SimpleUrlAuthenticationFailureHandler`** |
| **`GET /authenticate?logout`** | Logout success, if logout success was still default |

Javadoc: the form **must POST to `loginProcessingUrl`**, with **`usernameParameter` / `passwordParameter`** (defaults **`username` / `password`**) ([[What is UsernamePasswordAuthenticationFilter]], [[How do you create a custom login form in Spring Security]], [[What is AuthenticationFailureHandler]], [[How do you implement logout in Spring Security]]).

**`loginProcessingUrl("/login/process")`** is how you **keep POST off the page URL**. Setting **`loginPage` does not overwrite** a processing URL you already set. **`permitAll()`** authorizes the **page**, the **processing URL**, and the **failure URL**. CSRF stays **on** for cookie sessions; missing token is **403**, not **`?error`** ([[What is CsrfFilter in Spring Security]]).

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.formLogin((form) -> form.loginPage("/login").permitAll());
```

**Listing 1.** You own **`GET /login`**. **`POST /login`** is the processor unless you also set **`loginProcessingUrl`**.

```html
<form th:action="@{/login}" method="post">
	<input type="text" name="username"/>
	<input type="password" name="password"/>
	<button type="submit">Log in</button>
</form>
```

**Listing 2.** Thymeleaf **`th:action`** includes CSRF. Failure is **`param.error`**; logout is **`param.logout`**. Field names must match the configurer.

```d2
direction: down
ep: "LoginUrlAuthenticationEntryPoint\nGET loginPage" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
page: "Your HTML form" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
post: "POST loginProcessingUrl\nUsernamePasswordAuthenticationFilter" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

ep -> page -> post
```

**Fig. 1.** **`loginPage`** is the **view**. **`loginProcessingUrl`** is the **POST** (same path by default).

> [!warning] Redirect loop without `permitAll`
> Unauthenticated **GET `/login`** is itself a secured request → entry point → **`/login`** again. Call **`formLogin((form) -> form.loginPage("/login").permitAll())`** or **`requestMatchers("/login").permitAll()`**.

> [!warning] Processing URL is not frozen at `/login`
> Javadoc: passing **`/authenticate`** moves **POST**, **`?error`**, and **`?logout`** there too. A form whose **`action` is still `/login`** then **never hits the filter**. Set **`loginProcessingUrl`** only when GET and POST **must differ**. CSRF failures are **not** **`?error`**.

> [!tip] Interview answer
> loginPage is the URL the LoginUrlAuthenticationEntryPoint redirects to. If I do not set it, Spring generates GET /login. If I do, I render that page and the auto page is gone. By default POST, ?error, and ?logout follow that same path, so I either post the form there or set loginProcessingUrl. permitAll on the login URLs is required or the browser redirect-loops.
