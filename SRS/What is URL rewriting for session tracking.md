<!--
reps: 0
priority: 0
-->
#Networking/Web/Cookies #SRS
# What is URL rewriting for session tracking

> [!abstract] Short answer
> URL rewriting for session tracking keeps per-client state working when cookies are unavailable: the server appends the session identifier to every URL it emits (path parameter or query parameter), so each link the user follows carries the id back in the request target. It is the cookieless fallback for the mechanism described in [[What is an HTTP session]] — same id, worse transport.

## How it works

1. The server creates the session and, seeing no cookie support (client sent no session cookie, or cookies are explicitly disabled), starts rewriting: every href, form action and redirect target gains the id — in servlet containers historically `;jsessionid=...` as a path parameter, in generic web apps `?sid=...`.
2. The user clicks a rewritten link; the request target carries the id; the container extracts it (getRequestedSessionId / parameter parsing) and binds the request to the stored session.
3. Rewriting must happen on *every* URL the server produces — one missed link drops the session (the next request has no id and appears brand new).

```d2
direction: down
resp: "Response HTML\n<a href='/cart;jsessionid=7f3a'>" { width: 340; height: 80; style.fill: "#fff3e0" }
req: "Next request\nGET /cart;jsessionid=7f3a" { width: 320; height: 80; style.fill: "#e3f2fd" }
sess: "Container: extract id ->\nattach session state" { width: 300; height: 80; style.fill: "#e8f5e9" }
resp -> req -> sess
```

**Fig. 1.** The id rides in the URL instead of the Cookie header; every generated link must carry it.

## The servlet API angle

In Jakarta/Java EE the only correct way is `response.encodeURL(url)` (and `encodeRedirectURL` for redirects): the container appends the id *only when it decides cookies are not working*, and leaves URLs untouched otherwise — hand-concatenating `;jsessionid` yourself breaks cookie-enabled clients. The comparison card [[What is the difference between encodeURL and encodeRedirectURL]] drills the two methods; [[How would you explain HTTP sessions in servlet based applications]] shows the session side they serve.

> [!warning] URL rewriting leaks the session id everywhere a URL goes
> The id ends up in browser history, server/proxy access logs, Referer headers (leaking to third-party sites), bookmarks shared between people, and HTTP-cached pages — each is a hijack vector cookies (HttpOnly, never logged) do not have. Caches add a correctness trap: a URL with *my* id cached and served to *you* is session pollution. Modern practice: treat rewriting as a compatibility fallback at most, force cookies (Secure, HttpOnly, SameSite — [[What is an HTTP cookie]]), and prefer short-lived tokens in Authorization headers for API clients. Also, do not confuse session-tracking rewriting with URL *encoding* for safe characters ([[What is URL encoding and how do you perform it in Java]]) — different mechanisms with confusingly similar names.

Context: [[Why is REST stateless]] (why state has to be carried at all), [[What is a web application]] where this legacy mechanism still shows up.

> [!tip] Interview answer
> URL rewriting is the cookieless session-tracking fallback: the server appends the session id to every URL it emits and extracts it from the request target next time. In servlets the correct entry points are encodeURL and encodeRedirectURL — they rewrite only when cookies are not working. The tradeoff I stress: the id leaks into logs, history and Referer, and caches can mix sessions — so it is a legacy fallback, not a design choice.
