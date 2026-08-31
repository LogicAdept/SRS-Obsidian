<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/CSRF #Security/AppSec #SRS

# What is a CSRF attack and how do you enable CSRF protection?

> [!abstract] Short answer
> A **CSRF** attack forges a **state-changing** request in the victim's browser while they are logged in: the browser **attaches session cookies automatically**, so `evil.com` can `POST` to `bank.example.com` without reading the response. Spring Security's **synchronizer token** is **on by default** for **unsafe** methods — you do not "turn it on"; you keep `CsrfFilter` and send the token as a **form field or header** the browser will **not** add by itself. Disable CSRF only for **non-browser** clients (typically a Bearer JWT API). Missing or wrong token → **403**.

## What the attack actually is

The bank is logged in (`JSESSIONID`). The victim then visits `evil.com`, which auto-submits a hidden `POST /transfer`. Same-origin policy **blocks** the attacker from **reading** the bank's cookies or HTML, but it does **not** stop the browser from **sending** those cookies on a cross-site POST. The two POSTs look identical to the server unless something in the request is **not** auto-attached.

That extra secret is the **CSRF token**. The server stores an **expected** value (default: HTTP session via `HttpSessionCsrfTokenRepository`) and requires a matching **actual** value in a parameter (default `_csrf`) or header (`X-CSRF-TOKEN` / `X-XSRF-TOKEN`). `CsrfFilter` compares them. See [[What is CsrfToken]] and [[What is CsrfFilter in Spring Security]].

```d2
direction: right
victim: "Logged-in browser\nJSESSIONID cookie" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
evil: "evil.com\nhidden POST /transfer" {
  width: 200
  height: 70
  style.fill: "#fce4ec"
}
filter: "CsrfFilter\nunsafe methods" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
ok: "Controller" {
  width: 120
  height: 50
  style.fill: "#e8f5e9"
}
deny: "403 Forbidden" {
  width: 140
  height: 50
  style.fill: "#fce4ec"
}

victim -> evil: "user visits"
evil -> filter: "cookie auto-sent\nno _csrf token"
filter -> deny: "mismatch / missing"
filter -> ok: "header or _csrf\nmatches expected"
```

**Fig. 1.** Cross-site POST rides the session cookie. `CsrfFilter` rejects it unless the request also carries a token the attacker cannot read.

`DEFAULT_CSRF_MATCHER` **skips GET, HEAD, TRACE, and OPTIONS** and checks **every other** method (POST, PUT, PATCH, DELETE, …). Safe methods **must stay read-only**. Putting a token on GET leaks it through `Referer` and logs.

**SameSite** on the session cookie (`Lax` / `Strict`) is a second, weaker line: the browser may omit `JSESSIONID` on cross-site POSTs. Spring Security **does not** set `SameSite` on the container session cookie (Spring Session can). Treat SameSite as **defense in depth**, not a substitute for the synchronizer token. Older browsers ignore it; `Lax` still sends cookies on top-level GET navigations.

## Enabling protection (it is already on)

Servlet `HttpSecurity` **enables CSRF by default**. Explicit opt-in is `Customizer.withDefaults()` (or an empty `<csrf/>` in XML). XML has been **on by default since Spring Security 4.0**; Java config was already on. Current style is a `SecurityFilterChain` bean — not `WebSecurityConfigurerAdapter`.

```java
@Configuration
@EnableWebSecurity
public class SecurityConfig {

	@Bean
	public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
		http
			.authorizeHttpRequests((authorize) -> authorize.anyRequest().authenticated())
			.csrf(Customizer.withDefaults());
		return http.build();
	}
}
```

**Listing 1.** Conceptual — CSRF is already the default; this only makes it visible. Omit `.csrf(...)` and `CsrfFilter` still runs.

The page must **copy** the token into a part of the next unsafe request the browser does not attach:

```html
<input type="hidden" name="${_csrf.parameterName}" value="${_csrf.token}"/>
```

**Listing 2.** Hidden field from the `_csrf` request attribute. Spring's form tags and any `RequestDataValueProcessor` integration can inject this on POST forms for you.

JSON bodies are **not** form parameters: a `_csrf` field **inside** JSON never reaches the resolver. Send a header instead (meta tags + AJAX, or a cookie repository + `X-XSRF-TOKEN`). See [[How do you handle CSRF tokens in AJAX requests in Spring Security]].

Use CSRF for **any request a browser can make as a normal user**. Cookie-session apps, form login, HTTP Basic in a browser, and **JWT-in-a-cookie** SPAs stay vulnerable — "stateless" does not mean safe if the browser still auto-sends the credential. A **pure non-browser** API (header-only `Authorization: Bearer`) is the usual case for `csrf.disable()`. See [[Why do you disable CSRF for a JWT REST API]].

```java
http.csrf((csrf) -> csrf.disable());
```

```xml
<http>
	<csrf disabled="true"/>
</http>
```

**Listing 3.** Conceptual — full disable. Prefer `csrf.ignoringRequestMatchers(...)` when only some paths are non-browser. A cookie-session POST without a token is **403**, not 401; that is also why upgrades (Security 4 XML default, Security 6 still on) suddenly fail POSTs that never sent `_csrf`.

MockMvc: `post("/login")` without `.with(csrf())` → **403 Forbidden**; `.with(csrf())` is the test helper.

> [!warning] GET that changes state bypasses CSRF
> `CsrfFilter` does **not** check GET (or HEAD, TRACE, OPTIONS). A cross-site `<img>` whose `src` is the bank's `/transfer` GET, or a GET logout, is forgeable with a navigation and **no** token. Do not "fix" 403s by moving mutations onto GET. Logout defaults to POST for the same reason.

> [!warning] Disabling CSRF because "we use JSON" is not enough
> A browser can still POST `enctype="text/plain"` (or `transfer.json`) and ride cookies. JSON needs a **header** token, not `csrf.disable()`, unless **no** browser session cookie (or auto-sent Basic) is in play. SameSite-only is also not enough: Spring Security's CSRF feature does not set it, and `Lax` still sends cookies on some cross-site GETs.

> [!tip] Interview answer
> CSRF is a logged-in browser sending a forged state-changing request; the attacker rides cookies they cannot read. Spring Security's synchronizer token is on by default for every method except GET, HEAD, TRACE, and OPTIONS — enable it by leaving CsrfFilter in the chain and putting `_csrf` or X-CSRF-TOKEN on forms and AJAX. Disable it only for non-browser Bearer APIs. A POST without the token is 403; a mutating GET is not protected at all.
