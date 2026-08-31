<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/CSRF #SRS

# What is the default login URL in Spring Security?

> [!abstract] Short answer
> For **form login**, the default login URL is **`/login`**. **`GET /login`** is the **generated** page (**`DefaultLoginPageGeneratingFilter`**, **`DEFAULT_LOGIN_PAGE_URL`**) when you **`formLogin()`** without **`loginPage(...)`**. **`POST /login`** is **`UsernamePasswordAuthenticationFilter`** (**POST-only**). Failure: **`GET /login?error`**. Logout success: **`GET /login?logout`**. Unauthenticated **HTML** is **redirected** there by **`LoginUrlAuthenticationEntryPoint`**. **HTTP Basic** and **JWT resource server** have **no** login page — they **401**. CSRF is required on the **POST**.

## One path, four jobs

**`FormLoginConfigurer`** (**since 3.2**) javadoc when only **`formLogin()`** is specified:

| URL | Role |
| --- | --- |
| **`GET /login`** | Render form (framework HTML + CSRF hidden field) |
| **`POST /login`** | Authenticate `username` / `password` |
| **`GET /login?error`** | Failed attempt (**`AuthenticationFailureHandler`**) |
| **`GET /login?logout`** | After **`POST /logout`** |

**`AbstractAuthenticationFilterConfigurer`** starts **`loginPage` at `/login`**. Setting **`loginPage("/authenticate")` moves all four** unless you already set **`loginProcessingUrl` / `failureUrl` / logout success** ([[What is loginPage in form login]], [[How does form login work internally in Spring Security]], [[How do you create a custom login form in Spring Security]], [[How do you implement logout in Spring Security]]). Specifying **`loginPage`** **disables** the generated filter — you must **render** that GET yourself and **`permitAll()`** it.

**Basic** sends **`WWW-Authenticate`**, not a redirect to **`/login`**. With **neither** form nor Basic, the default entry point is **`Http403ForbiddenEntryPoint`** (**403**). **`oauth2ResourceServer`** is **Bearer 401**, not **`/login`** ([[What is AuthenticationEntryPoint]], [[How do you configure HTTP Basic authentication in Spring Security]], [[When should you use HTTP Basic versus form login]]). **OAuth2 Login** uses **`/oauth2/authorization/{id}`**, not this URL.

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.formLogin(Customizer.withDefaults());
```

**Listing 1.** Official username/password sample: generated **`GET /login`**, **`POST /login`**, CSRF on.

```http
GET /login
POST /login
GET /login?error
GET /login?logout
```

**Listing 2.** Default form-login family. **`GET /logout`** is the **confirm page**, not this table.

```d2
direction: down
deny: "unauthenticated HTML" {
  width: 220
  height: 50
  style.fill: "#fff3e0"
}
get: "302 → GET /login\nDefaultLoginPageGeneratingFilter" {
  width: 300
  height: 70
  style.fill: "#e3f2fd"
}
post: "POST /login\nUsernamePasswordAuthenticationFilter" {
  width: 300
  height: 70
  style.fill: "#e8f5e9"
}

deny -> get -> post
```

**Fig. 1.** **`/login` GET** is the page. **`/login` POST** is authentication.

> [!warning] `/login` is not universal
> **JWT / Basic** do not redirect here. Calling **`loginPage("/login")`** **turns off** the generated page even though the path is the default — you now **own** the HTML. **`permitAll`** is still required or **GET /login** redirect-loops.

> [!warning] `loginPage` moves POST too
> Javadoc **Impact on other defaults**: **`loginPage("/authenticate")`** makes **POST `/authenticate`**, **`?error`**, and **`?logout`** follow. A form that still **`action="/login"`** misses the filter. Set **`loginProcessingUrl`** only when GET and POST **must differ**. Missing CSRF on POST is **403**, not **`?error`**.

> [!tip] Interview answer
> The default form-login URL is /login: GET shows the generated page, POST authenticates, ?error and ?logout are the failure and logout-success views. Unauthenticated browsers are redirected there; Basic and JWT APIs return 401 instead. If I set loginPage, I supply the HTML and the processing URL follows that path unless I override loginProcessingUrl.
