<!--
reps: 0
priority: 0
-->
#Security/JWT #Security/AppSec #SRS

# Where should you store a JWT in a browser

> [!abstract] Short answer
> The honest answer is a trade: **memory-only** for the short-lived access token with a **httpOnly, Secure, SameSite cookie** for the refresh token is the defensible default; `localStorage` is the most convenient and the most dangerous option, because any XSS can read it and exfiltrate. Cookies bring the CSRF problem back, which is the price of XSS-theft resistance ([[How would you explain XSS]]).

## The three options and what actually threatens them

| Storage | XSS can read it | CSRF exposed | Survives reload | Notes |
|---|---|---|---|---|
| JS variable (memory) | the running script, not persistence | no (Bearer header) | no | lost on refresh - pair with silent re-auth |
| localStorage / sessionStorage | yes, trivially | no | yes | any XSS exfiltrates the token |
| httpOnly cookie | no (not script-readable) | yes | yes | needs SameSite + CSRF handling |

```d2
direction: right
xss: "XSS runs" { width: 140; height: 60; style.fill: "#ffebee"
ls: "localStorage\n-> token stolen" { width: 240; height: 70; style.fill: "#ffebee"
co: "httpOnly cookie\n-> script cannot read" { width: 260; height: 70; style.fill: "#e8f5e9"
api: "Attacker can still\ncall APIs as the user\nwhile XSS lives" { width: 280; height: 80; style.fill: "#fff3e0" */
xss -> ls
xss -> co -> api
```

**Fig. 1.** httpOnly keeps the token out of the thief's hands but does not neutralize the XSS itself - the injected script can simply act in-session. httpOnly is theft mitigation, not XSS fix.

## The workable pattern

- Keep the **access token in memory** (or a httpOnly cookie), send it as a Bearer header.
- Put the **long-lived refresh token in a httpOnly, Secure, SameSite** cookie scoped to the auth endpoint path, so a successful XSS run still cannot mint new access tokens after the page unloads ([[How do you revoke a JWT]] covers killing even that window).
- If tokens must live in cookies, the API inherits CSRF obligations - SameSite=Lax/Strict plus an anti-CSRF token or custom-header check ([[What is a CSRF attack and how do you enable CSRF protection]]).
- Cookie-based auth on a different domain needs careful `SameSite=None; Secure` handling - and then CSRF protection is not optional.

> [!warning] "localStorage is fine if we have no XSS"
> There is no such guarantee - one vulnerable dependency, one injected script, and the token leaves the origin. And "SameSite protects localStorage" mixes up mechanisms: SameSite governs cookie sending, it does nothing to script-readable storage. The realistic statement is: XSS anywhere equals token theft from localStorage ([[Where should you store a JWT in a browser]] is exactly the question to ask any SPA design).

> [!tip] Interview answer
> Default: access token in memory with Bearer headers, refresh token in a httpOnly Secure SameSite cookie on the auth path. localStorage wins on convenience but hands every XSS the token; cookies win on theft resistance but reintroduce CSRF, so they come with SameSite and CSRF tokens. And whichever you pick, httpOnly does not fix XSS - it only limits what the XSS steals.
