<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/CSRF #Security/AppSec #SRS

# What is the difference between CORS and CSRF in Spring Security?

> [!abstract] Short answer
> **CSRF** is a **server** check: stop **forged state-changing** requests that reuse **automatic credentials** (cookies). Spring Security does that with a **synchronizer token** (`CsrfFilter`, **on by default**). **CORS** is a **browser** policy: which **other origins' JavaScript** may **call** your API and **read** the response. Spring only **emits CORS headers** (`CorsFilter` / `http.cors()`). They are **orthogonal**. CORS does **not** replace CSRF; disabling one never fixes the other.

## Two different attackers

Spring's CSRF walkthrough is a **cross-site HTML form** `POST` to your app while the victim is logged in. The browser **attaches `JSESSIONID`**. The attacker never needed JavaScript and never needed to **read** the response. See [[What is a CSRF attack and how do you enable CSRF protection]] and [[What is CsrfFilter in Spring Security]].

Spring's CORS intro is the **other tab**: a **script** on `evil.com` must **not** make **AJAX** to your bank with the victim's credentials. Browsers block that by default (same-origin). **CORS** is how **you** list origins, methods, and headers the browser may allow. That is implemented **in the browser**; Spring Security's `cors()` only **supports** it with response headers. `.cors(CorsConfigurer::disable)` does **not** turn CORS off in the browser — it **removes Spring's CORS support**, so a cross-origin SPA **cannot** talk to you.

The CORS protocol **preflights** (`OPTIONS`) requests that go **beyond what an HTML form can send**. A classic form `POST` (`application/x-www-form-urlencoded`) is **not** preflighted, still **sends cookies**, and still **changes state**. That is why a CORS allowlist is **not** a CSRF defense.

```d2
direction: right
evil: "evil.com" {
  width: 120
  height: 50
  style.fill: "#fce4ec"
}
form: "HTML form POST\n(no preflight)" {
  width: 180
  height: 70
  style.fill: "#fff3e0"
}
ajax: "JS fetch / XHR\n(CORS + maybe OPTIONS)" {
  width: 200
  height: 70
  style.fill: "#e3f2fd"
}
api: "Your Spring API" {
  width: 160
  height: 50
  style.fill: "#e8f5e9"
}

evil -> form
evil -> ajax
form -> api: "cookies + no CSRF token\n→ CsrfFilter 403"
ajax -> api: "browser enforces CORS\nheaders from CorsFilter"
```

**Fig. 1.** CSRF is the form (and any auto-credentialed mutation). CORS is the JavaScript caller. Both can appear on one SPA, as two filters.

| | **CSRF** | **CORS** |
|---|---|---|
| Who enforces it | **Server** (`CsrfFilter`) | **Browser** (Spring adds headers) |
| Default in Security | **Enabled** for unsafe methods | **Not** a substitute login; you **opt in** (`CorsConfigurationSource` / MVC / `http.cors()`) |
| Typical failure | **403** missing/invalid token | Preflight or JS **blocked**; often looks like OPTIONS failing **before** the POST |
| Turns off when | Bearer-only, non-browser clients — see [[Why do you disable CSRF for a JWT REST API]] | You still need CORS if a **browser** SPA is on another origin |

## How Spring wires them

CORS **must run before** Spring Security: a preflight **`OPTIONS` has no cookies**. If Security runs first, it treats the caller as **unauthenticated** and rejects the preflight. Provide a `UrlBasedCorsConfigurationSource` bean (Security auto-wires `CorsFilter`) or `http.cors(Customizer.withDefaults())` to reuse **Spring MVC** CORS. `CorsConfigurer` (since **4.1.1**) adds `CorsFilter` or `PreFlightRequestFilter`.

```java
@Bean
UrlBasedCorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration configuration = new CorsConfiguration();
    configuration.setAllowedOrigins(List.of("https://app.example.com"));
    configuration.setAllowedMethods(List.of("GET", "POST"));
    UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
    source.registerCorsConfiguration("/**", sourceConfig(configuration));
    return source;
}
```

**Listing 1.** Conceptual — Security CORS support. CSRF stays **on** unless you disable it on a chain that truly has no cookie session. AJAX still needs a CSRF **header**: [[How do you handle CSRF tokens in AJAX requests in Spring Security]].

> [!warning] CORS success is not CSRF success
> A browser may **allow** `https://app.example.com` to `fetch` your API **and** still get **403** from `CsrfFilter` if the CSRF header is missing. Conversely, `csrf.disable()` does **nothing** for a failed **OPTIONS** preflight. Debug CORS on **OPTIONS** first, then CSRF on the **real** POST.

> [!warning] `allowCredentials` shares cookies and CSRF tokens
> Spring Framework: enabling credentialed CORS is a **high trust** setting and **widens** the attack surface — it can expose **cookies and CSRF tokens** to the allowed origin. Do not pair `allowCredentials` with origin `*`. A cross-origin SPA with cookies still needs CSRF (or Bearer-in-header and no cookies).

> [!tip] Interview answer
> CSRF is server-side protection against cross-site form POSTs that ride on cookies; Spring enables it by default with a synchronizer token. CORS is the browser's rule for which origins' JavaScript may call you; Spring only adds CorsFilter headers, and it must run before Security so cookie-less OPTIONS preflights succeed. They are separate: allowing an origin does not prove intent, and disabling CSRF will not fix a preflight failure.
