<!--
reps: 0
priority: 0
-->
#Networking/Web/Cookies #SRS
# What is an HTTP cookie

> [!abstract] Short answer
> An HTTP cookie (RFC 6265bis) is a small key/value record a server asks the browser to store and echo back on every later request to that site — the standard mechanism for carrying per-client state over stateless HTTP: session ids, preferences, tracking. Attributes govern lifetime (Expires/Max-Age), visibility (Domain, Path), and safety (Secure, HttpOnly, SameSite).

## The mechanics

1. **Set:** the server sends `Set-Cookie: session=7f3a; HttpOnly; Secure; SameSite=Lax; Max-Age=3600; Path=/` — one header per cookie.
2. **Store:** the browser keeps it in its cookie jar, scoped by domain/path and attributes.
3. **Return:** every subsequent matching request carries `Cookie: session=7f3a` automatically — the server looks the id up ([[What is an HTTP session]] is the state that usually hangs off it).
4. **Expire:** session cookies die with the browser session; persistent cookies at Expires/Max-Age; deletion = Set-Cookie with a past date.

```d2
direction: right
srv: "Server\nSet-Cookie: sid=7f3a..." { width: 240; height: 80; style.fill: "#fff3e0" }
jar: "Browser cookie jar\nscoped by Domain+Path" { width: 250; height: 90; style.fill: "#e3f2fd" }
req: "Every later request:\nCookie: sid=7f3a" { width: 260; height: 80; style.fill: "#e8f5e9" }
srv -> jar -> req
req -> srv: "stateless HTTP remembers"
```

**Fig. 1.** The cookie is the state carrier; the server-side session (or token) is the state itself.

## Attributes are the interview's real subject

| Attribute | Controls | Missing it means |
|---|---|---|
| `Domain` | which sites receive it (no port) | host-only cookie (default) |
| `Path` | URL prefix scope | `/` |
| `Expires` / `Max-Age` | lifetime | session cookie (browser exit) |
| `Secure` | HTTPS-only transmission | cookie may travel over plain HTTP |
| `HttpOnly` | invisible to JavaScript (`document.cookie`) | XSS can steal the session id |
| `SameSite=Lax/Strict/None` | cross-site sending (CSRF mitigation) | browser default (Lax nowadays) |

> [!warning] Cookies are not authentication — they are the transport of it, and the attack surface too
> Risks: **session hijacking** via XSS when HttpOnly is off; **CSRF** when cookies auto-attach cross-site (SameSite + CSRF tokens fix it); **fixation** when ids are not regenerated at login. Misconceptions to kill: "cookies are code executed in the browser" (they are opaque strings the server defines); "a cookie can be read by other websites" (SameSite/Domain scoping prevents it — that is the point of the jar); "deleting the cookie logs out the server" (the session may live on server-side until its own expiry — [[How would you explain HTTP sessions in servlet based applications]] shows both ends in Java). Third-party tracking cookies are the ones browsers are killing, first-party state cookies are not going anywhere.

Scope companions: [[What is URL rewriting for session tracking]] (cookieless fallback), [[What is an HTTP session]] (what the id refers to), [[What is the difference between HTTP and HTTPS]] (why Secure needs TLS).

> [!tip] Interview answer
> A cookie is the browser-side storage the server writes via Set-Cookie and the browser returns via Cookie headers — how stateful apps ride stateless HTTP. I organize the answer around the attributes, because they are the security story: Max-Age for lifetime, Secure, HttpOnly against XSS theft, SameSite against CSRF. Close with the distinction: the cookie carries the id; the session or token is the actual state.
