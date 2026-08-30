<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/CSRF #Security/JWT #Security/AppSec #SRS

# Why do you disable CSRF for a JWT REST API?

> [!abstract] Short answer
> **CSRF targets cookie-based browser sessions** — the browser **automatically resends session cookies** on cross-site POSTs. A **pure JWT REST API** that accepts **`Authorization: Bearer`** tokens the client **must attach explicitly** is **not vulnerable in the same way**, so teams typically **`csrf.disable()`** together with **`SessionCreationPolicy.STATELESS`**. **Keep CSRF enabled** when authentication still rides on **cookies** (session login, JWT-in-cookie SPAs).

## What CSRF actually exploits

Spring Security's CSRF guide walks through the classic attack: while logged into **`bank.example.com`**, the victim visits **`evil.com`**, which submits a hidden form **`POST`** to the bank. The browser **includes `JSESSIONID` automatically** even though the victim never intended the transfer.

The synchronizer-token defense requires a **`_csrf` parameter or header** that **evil.com cannot read or forge** (same-origin policy). The token must live in a part of the request the **browser does not attach by itself** — unlike cookies.

```d2
direction: right
browser: "Victim browser\n(logged in)" {
  width: 180
  height: 60
  style.fill: "#e3f2fd"
}
evil: "evil.com form POST" {
  width: 160
  height: 50
  style.fill: "#fce4ec"
}
api: "Your API" {
  width: 120
  height: 50
  style.fill: "#e8f5e9"
}

browser -> evil: "user clicks"
evil -> api: "Cookie sent\nautomatically"
api -> browser: "CSRF token\nmissing → 403"
```

**Fig. 1.** Cookie session auth is the CSRF surface; a secret header the browser never auto-sends is not.

## Why Bearer JWT APIs usually disable CSRF

A typical stateless resource server:

1. Client obtains a JWT out-of-band (login endpoint, IdP, mobile SDK).
2. Client sends **`Authorization: Bearer <jwt>`** on each API call.
3. **`SessionCreationPolicy.STATELESS`** — no server session cookie is created.

Foreign sites **cannot cause the browser to attach your API's Bearer token** the way they attach cookies. Spring's guidance: use CSRF for requests **processed by browsers for normal users**; services used **only by non-browser clients** (mobile apps, machine-to-machine APIs) **may disable CSRF**.

That matches common Boot configuration:

```java
http
    .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
    .csrf(csrf -> csrf.disable())
    .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
```

**Listing 1.** Conceptual stateless JWT chain — no session cookie, CSRF filter removed.

Official docs also warn: **"stateless" alone does not guarantee safety**. If authentication still lives in a **cookie** (including a JWT stored in a cookie), the app **remains CSRF-vulnerable** — same as session cookies or HTTP Basic, which browsers can resend automatically.

## CSRF vs CORS (do not conflate)

| Mechanism | Protects against |
|---|---|
| **CSRF** | Unwanted **state-changing** requests that reuse **automatic credentials** (cookies) |
| **CORS** | Which **origins' JavaScript** in a browser may **read responses** from your API |

CORS does **not** stop CSRF — a simple HTML form POST **does not perform a CORS preflight** and can still hit your endpoint with cookies attached. Configure CORS in Spring Security (**`CorsFilter` / `http.cors`**) for browser SPAs; it is **orthogonal** to disabling CSRF on a Bearer-only API. See [[What is CorsFilter in Spring Security]].

> [!warning] Valid JWT but POST returns 403
> Spring Security **enables CSRF by default** (including Boot 3). A **`POST /api/...`** with a correct Bearer token but **no CSRF token** fails in **`CsrfFilter`** with **403**, which is easy to misread as a JWT problem. Either supply CSRF tokens (cookie-session or cookie-JWT SPAs) or **`csrf.disable()`** on a chain that truly uses header-only Bearer auth. See [[What is CsrfFilter in Spring Security]] and [[How do you implement JWT authentication in Spring Security]].

> [!tip] Interview answer
> CSRF matters when the browser automatically sends credentials — usually session cookies. A stateless JWT API that requires an explicit Authorization Bearer header is not forged that way, so csrf.disable() with STATELESS is standard. Keep CSRF if you use cookie auth or JWT-in-cookie; CORS is a separate browser policy, not a CSRF replacement.
