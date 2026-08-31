<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/Authentication #Java/Spring/Security/CSRF #SRS

# When should you use HTTP Basic versus form login?

> [!abstract] Short answer
> Use **form login** for **browser apps** that need a **login page**, a **session cookie**, **logout**, and **RequestCache** replay after **302** to **`/login`**. Use **HTTP Basic** for **clients that can send `Authorization: Basic` on every request** (curl, simple APIs, machines). Both present a **username/password** to the same **`DaoAuthenticationProvider`**. Basic is **401 + `WWW-Authenticate`**, **Base64 not encryption** (TLS), and by default **does not store** the `SecurityContext` in the session. Delegate interactive login to an IdP with **`oauth2Login`**, not Basic. You **may** enable **both** on one chain.

## Same password check, different presentation

| | Form login | HTTP Basic |
| --- | --- | --- |
| Client | Browser HTML | HTTP client / script |
| Challenge | **302** **`GET /login`** | **401** + **`WWW-Authenticate: Basic`** |
| Credentials | **POST `/login`** `username` / `password` + **CSRF** | **`Authorization: Basic`** each request (RFC **7617**) |
| Session | **Saved** by default | Filter **does not save** context (resend header) |
| Saved request | **`HttpSessionRequestCache`** | **`NullRequestCache`** |
| Logout | **`POST /logout`** (CSRF) | Stop sending the header (browser dialog is sticky) |
| UX | Your form | Native **browser dialog** |

Form: **`LoginUrlAuthenticationEntryPoint`** + **`UsernamePasswordAuthenticationFilter`**. Basic: **`BasicAuthenticationEntryPoint`** + **`BasicAuthenticationFilter`**. Users still come from **`UserDetailsService`** ([[How does form login work internally in Spring Security]], [[How do you configure HTTP Basic authentication in Spring Security]], [[What is AuthenticationEntryPoint]], [[What is the default login URL in Spring Security]]).

**Choose form** when you render HTML, need **`permitAll` login/logout pages**, CSRF on cookie sessions, and **`SavedRequest`** after login ([[How do you create a custom login form in Spring Security]], [[What is CsrfFilter in Spring Security]], [[How do you implement logout in Spring Security]]).

**Choose Basic** when there is **no page** to host a form: internal APIs, probes, `curl`. Do **not** pick Basic to “skip CSRF” on a browser SPA — the password rides **every** request and the dialog **cannot** be styled. Prefer **Bearer JWT / OAuth2** for public APIs ([[What authentication mechanisms does Spring Security support]], [[What is the difference between HTTP 401 and 403 in Spring Security]]).

**Both:** **`formLogin()` + `httpBasic()`** is supported. Entry points are registered with **`defaultAuthenticationEntryPointFor`**. A browser still **redirects to `/login`**; a client that sends **`Authorization: Basic`** is authenticated by the Basic filter. **`X-Requested-With: XMLHttpRequest`** suppresses Basic’s **`WWW-Authenticate`** so the native dialog stays down.

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.formLogin(Customizer.withDefaults());
```

**Listing 1.** Server-rendered app: session, CSRF, generated **`/login`**.

```java
http
	.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
	.httpBasic(Customizer.withDefaults());
```

**Listing 2.** Header-per-request API. Add **`formLogin`** on the same chain only if browsers also hit it.

```d2
direction: down
html: "browser HTML" {
  width: 200
  height: 50
  style.fill: "#e3f2fd"
}
api: "curl / machine API" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
form: "formLogin\n302 / session / CSRF" {
  width: 240
  height: 70
  style.fill: "#e8f5e9"
}
basic: "httpBasic\n401 / Authorization header" {
  width: 260
  height: 70
  style.fill: "#f3e5f5"
}

html -> form
api -> basic
```

**Fig. 1.** Pick by **client**, not by password store. Both can use the same **`UserDetailsService`**.

> [!warning] Basic in a browser is a dialog plus a password on every request
> Base64 is reversible. **TLS is mandatory.** If you also keep a **session cookie**, **CSRF still applies** to cookie-authenticated POSTs. Basic’s default **stateless** context does **not** mean **`csrf.disable()`** is required — disable CSRF only for true non-browser APIs you have designed that way.

> [!warning] Boot’s default is Basic until you add a chain
> A custom **`SecurityFilterChain`** **turns Boot’s default Basic off**. Adding only **`formLogin`** does **not** keep Basic. Adding only **`httpBasic`** does **not** give you **`/login`**. **OAuth2 Login** is for **delegated** IdP sign-in; **resource-server JWT** is for **Bearer** APIs — neither is a third “password header.”

> [!tip] Interview answer
> Form login is for browsers: redirect to a login page, session cookie, CSRF, logout. HTTP Basic is for clients that send Authorization: Basic on every request — 401 plus WWW-Authenticate, no form, password Base64-encoded so TLS is required. I use the same UserDetailsService for both. I do not put Basic on a user-facing website, and I use OAuth2 or JWT when I am not presenting a first-party password at all.
