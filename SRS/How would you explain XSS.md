<!--
reps: 0
priority: 0
-->
#Security/AppSec #SRS

# How would you explain XSS

> [!abstract] Short answer
> Cross-site scripting (XSS) is the injection of browser-executable script through untrusted data that reaches an HTML page without context-appropriate output encoding. The OWASP prevention cheat sheet groups it into three types - reflected, stored, and DOM-based - and the fix is always the same direction: **encode on output for the exact context** (HTML body, attribute, JavaScript, URL), with safe sinks and CSP as supporting layers.

## The three types

- **Reflected**: the payload arrives in the request (query param, header) and the server echoes it into the response - attacker crafts a link, victim clicks.
- **Stored**: the payload persists (comment field, profile bio) and executes for every viewer - the highest-value form.
- **DOM-based**: the vulnerability lives entirely client-side; a JS sink consumes attacker-controllable input - `innerHTML`, `document.write`, `eval`, `location.href = ...` - with no server round trip.

```d2
direction: right
a: "Attacker crafts URL\n<script> payload" { width: 250; height: 80; style.fill: "#ffebee"
v: "Victim opens link" { width: 190; height: 60; style.fill: "#fff3e0"
s: "Server reflects param\ninto HTML unencoded" { width: 260; height: 80; style.fill: "#ffebee"
b: "Browser executes script\nwith victim's origin" { width: 280; height: 80; style.fill: "#ffebee"
x: "Session theft:\nreads cookies, acts as user" { width: 270; height: 80; style.fill: "#ffebee"
a -> v -> s -> b -> x
```

**Fig. 1.** Reflected XSS chain. The script runs with the victim's origin, so anything the app can do - cookies, tokens in DOM, authorized API calls - the script can do.

## Prevention, in the cheat sheet's order

- **Output encoding, per context**: HTML-escape in body text (`<` `>` `&`), attribute-escape including quotes, JavaScript-encode for script contexts, percent-encode URLs. The same input needs different encodings depending on where it lands.
- **Safe APIs instead of sinks**: `textContent` instead of `innerHTML`; framework auto-escaping (React, Angular) - and the documented escapes hatches (`dangerouslySetInnerHTML`, `bypassSecurityTrust*`) treated as loud exceptions.
- **HTML sanitization** only for genuinely rich input, with a maintained sanitizer - never a regex filter.
- **CSP** as a second layer: a restrictive `Content-Security-Policy` blocks inline script even when encoding fails ([[Which default security headers does Spring Security add]]).

> [!warning] "HttpOnly stops XSS"
> HttpOnly only hides the cookie from `document.cookie` - the script still runs, can call the same APIs in-session, read DOM-resident tokens, and keylog. Encoding kills the bug; HttpOnly, CSP, and [[Where should you store a JWT in a browser]] merely limit the loot. Also: "we filter `<script>` on input" fails on event handlers, `javascript:` URLs, encoding tricks, and non-script sinks.

XSS sits in the OWASP catalogue under injection-class risks ([[What is the OWASP Top 10]]); its server-side cousin is [[How would you explain SQL injection attacks and defenses]], and the CSRF confusion is settled in [[What is the difference between CORS and CSRF in Spring Security]].

> [!tip] Interview answer
> XSS is untrusted data executing as script in a victim's browser - reflected, stored, or DOM-based via dangerous sinks. The defense is context-aware output encoding at render time plus safe APIs and CSP as a backstop; HttpOnly cookies and token placement only limit what a successful payload steals.
