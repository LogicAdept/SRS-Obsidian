<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/FilterChain #Java/Spring/Boot/AutoConfiguration #SRS

# How do you use form login authentication in Spring Boot?

> [!abstract] Short answer
> Add **`spring-boot-starter-security`**. Boot already picks **form login** vs **HTTP Basic** from the **`Accept`** header. To make it explicit, a **`SecurityFilterChain`** calls **`http.formLogin(Customizer.withDefaults())`** — Security then serves a **generated** login page and **`POST /login`**. A custom page is **`formLogin(form -> form.loginPage("/login").permitAll())`**, a **`GET /login`** controller, and an HTML **POST** with fields **`username`**, **`password`**, and a **CSRF** token. Do **not** disable CSRF or log out with **GET**.

## Redirect to a form, POST credentials, then a session

Unauthenticated HTML hits **`ExceptionTranslationFilter`** → **`LoginUrlAuthenticationEntryPoint`** → login page. Submit goes to **`UsernamePasswordAuthenticationFilter`**, which builds a **`UsernamePasswordAuthenticationToken`** and calls the **`AuthenticationManager`**. Success stores the `Authentication` and the default **`AuthenticationSuccessHandler`** sends the browser back to the **saved request**. Failure clears the context and redirects to **`/login?error`**.

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
	http.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated());
	http.formLogin(Customizer.withDefaults());
	return http.build();
}
```

**Listing 1.** Minimal explicit form login. `withDefaults()` is the generated page + **`POST /login`**. In Boot you do **not** register `AbstractSecurityWebApplicationInitializer` — `SecurityAutoConfiguration` already installs the filter ([[What is spring-boot-starter-security]], [[How do you secure a Spring Boot application]]).

```java
http.formLogin((form) -> form.loginPage("/login").permitAll());
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

**Listing 2.** Custom page: you **render** `GET /login`. **`permitAll()`** on the form-login config is required — if `/login` itself needs authentication you get a **redirect loop**. If the dispatcher has a prefix, set **`loginPage`** and **`loginProcessingUrl`** to that prefix (they are matched **literally**).

```html
<form method="post" action="/login">
	<input type="text" name="username"/>
	<input type="password" name="password"/>
	<input type="submit" value="Log in"/>
</form>
```

**Listing 3.** Contract from the Security reference: **POST** `/login`, parameter names **`username`** and **`password`**. Thymeleaf `th:action="@{/login}"` inserts the **CSRF** field. Plain JSP/HTML must add the hidden CSRF input (`_csrf` request attribute). Query **`error`** = bad credentials; **`logout`** = just logged out. Logout is **`POST /logout`** with CSRF — default **`LogoutFilter` ignores GET** ([[When should you use HTTP Basic versus form login]]).

```d2
direction: down
get: "GET /private\nAnonymous" {
  width: 220
  height: 50
  style.fill: "#e3f2fd"
}
entry: "LoginUrlAuthenticationEntryPoint\nGET /login" {
  width: 280
  height: 70
  style.fill: "#fff3e0"
}
post: "POST /login\nUsernamePasswordAuthenticationFilter" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}
ok: "SecurityContext + redirect\nto saved request" {
  width: 260
  height: 70
  style.fill: "#f3e5f5"
}

get -> entry -> post -> ok
```

**Fig. 1.** Form login is a **browser session** flow, not Bearer JWT. Users still come from **`UserDetailsService`** (Boot’s generated **`user`** until you replace it) ([[What is the default username and password in Spring Boot Security]]). Optional DSL: `defaultSuccessUrl`, `failureUrl`, `loginProcessingUrl`.

> [!warning] `csrf().disable()` plus GET `/logout` is the dump’s foot-gun
> CSRF on **login and logout** is **on purpose** (login CSRF = session fixation / “login as attacker”). Missing token → **403**. A custom `SecurityFilterChain` **replaces** Boot’s defaults; `authorizeRequests()` / `antMatchers` / `WebSecurityConfigurerAdapter` will not compile on Boot 3/4 ([[Why was WebSecurityConfigurerAdapter removed]]).

> [!warning] The generated page vanishes when you set `loginPage`
> Once you call **`loginPage("/login")`**, Security **stops** rendering its default form — you must map **GET** and still **POST** to the processing URL. `securityMatcher("/app/**")` that **omits** `/login` yields **404** on the filter’s endpoints.

> [!tip] Interview answer
> In Boot I add starter-security; browsers get form login via content negotiation. I declare a SecurityFilterChain with formLogin. The default is a generated page and POST /login handled by UsernamePasswordAuthenticationFilter. A custom loginPage needs permitAll, a GET controller, username/password fields, and a CSRF token. I never disable CSRF for a browser app and I log out with POST /logout.
