<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/CSRF #Security/AppSec #Java/Spring/Security/FilterChain #SRS

# How does Spring Security mitigate XSS CSRF and clickjacking?

> [!abstract] Short answer
> **CSRF**: **`CsrfFilter`** is on by default for **unsafe** methods (POST, not GET). **Clickjacking**: default **`X-Frame-Options: DENY`**. **XSS**: defaults are **defense-in-depth headers**, not a sanitizer — **`X-Content-Type-Options: nosniff`**, **`X-XSS-Protection: 0`** (auditor off). **CSP is not default**; you add **`headers.contentSecurityPolicy`**. Session fixation is separate: **`changeSessionId()`** on login.

## Default filter chain and `headers()`, not one annotation

`@EnableWebSecurity` turns on **`CsrfFilter`** and **`HeaderWriterFilter`**. There is no `@EnableXssProtection`.

**CSRF.** Synchronizer token. Unsafe methods need the token (form parameter or header). GET/HEAD/TRACE/OPTIONS are skipped. Thymeleaf **`th:action`** POSTs pick it up via **`RequestDataValueProcessor`**. JWT APIs often **`csrf.disable()`** because the browser does not auto-attach a Bearer token.

**Clickjacking.** Default header:

```
X-Frame-Options: DENY
```

Pages cannot be framed. **`frameOptions.sameOrigin()`** if you need same-site iframes. CSP **`frame-ancestors`** is the newer complement; it is **not** sent until you configure CSP.

**XSS.** Spring Security does **not** HTML-encode your templates. Defaults:

```
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Pragma: no-cache
Expires: 0
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000 ; includeSubDomains
X-Frame-Options: DENY
X-XSS-Protection: 0
```

**Listing 1.** Official default set. **HSTS** only on HTTPS. **`nosniff`** blocks some polyglot XSS. **`X-XSS-Protection: 0`** follows current OWASP (the old browser XSS auditor is deprecated). Real XSS mitigation is **encode output / validate input**, then optional CSP:

```java
http
	.headers(headers -> headers
		.contentSecurityPolicy(csp -> csp
			.policyDirectives("script-src 'self'; object-src 'none'")));
```

**Listing 2.** CSP is opt-in. Spring will not invent a policy for you.

```d2
direction: down
csrf: "CsrfFilter\nunsafe methods" {
  width: 200
  height: 50
  style.fill: "#fff3e0"
}
click: "X-Frame-Options: DENY" {
  width: 200
  height: 45
  style.fill: "#c8e6c9"
}
xss: "nosniff + CSP (opt-in)\nencode output yourself" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}

csrf -> click
click -> xss
```

**Fig. 1.** Three different mechanisms. SQL injection is **not** in this diagram ([[Which default security headers does Spring Security add]], [[What is CsrfFilter in Spring Security]], [[What is a CSRF attack and how do you enable CSRF protection]], [[What is HeaderWriterFilter]]).

Session fixation (often listed with these exploits): on login, Servlet 3.1+ default is **`HttpServletRequest.changeSessionId()`**. **`none`** disables it and is not recommended.

> [!warning] Headers are not a JDBC firewall
> Spring Security does not parameterize SQL. Injection is **`PreparedStatement` / JPA bind parameters**, not **`CsrfFilter`**. Dumps that put SQL injection in the same list as XSS/CSRF are mixing layers.

> [!warning] Default XSS header is `0`, and CSP is off
> **`X-XSS-Protection: 0`** does **not** mean “XSS is solved.” Turning the old auditor **on** (`1; mode=block`) is the customization sample, not current default. Without output encoding and a CSP you wrote, reflected XSS still runs.

> [!tip] Interview answer
> CSRF is CsrfFilter on POSTs by default. Clickjacking is X-Frame-Options DENY via HeaderWriterFilter. XSS is not a Spring Security sanitizer: nosniff plus X-XSS-Protection 0, and you add Content-Security-Policy yourself. Session fixation is changeSessionId on login. SQL injection is the data-access layer.
