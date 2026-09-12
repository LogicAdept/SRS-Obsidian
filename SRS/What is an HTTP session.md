<!--
reps: 0
priority: 0
-->
#Networking/Web/Cookies #SRS
# What is an HTTP session

> [!abstract] Short answer
> An HTTP session is a server-side mechanism for keeping per-client state across stateless HTTP requests: on first contact the server creates a session object with an id, hands the id to the browser (normally in a Set-Cookie header), and every following request carries the id back, letting the server look up that client's state — login, cart, preferences. The state lives on the server; HTTP itself stays stateless ([[Why is REST stateless]]).

## The lifecycle

1. **Create:** the server allocates a session (id + attributes + expiry), e.g. a `JSESSIONID` cookie in servlet containers — [[How would you explain HTTP sessions in servlet based applications]] details the Java mechanics.
2. **Carry:** the browser returns the id on every request via the Cookie header (or a URL parameter when cookies are disabled — [[What is URL rewriting for session tracking]]).
3. **Use:** the server attaches the request to the stored object: authentication state, cart, CSRF token, workflow step.
4. **Expire/destroy:** idle timeout (server-side) or logout invalidates it; the cookie may be a session cookie (no Max-Age — dies with the browser) or persistent.

```d2
direction: down
login: "POST /login (credentials)" { width: 250; height: 60; style.fill: "#e3f2fd" }
create: "Server: create session\nid=7f3a..., store state" { width: 270; height: 80; style.fill: "#fff3e0" }
cookie: "Set-Cookie: session=7f3a...\n(HttpOnly, Secure, SameSite)" { width: 310; height: 80; style.fill: "#fff3e0" }
next: "GET /cart\nCookie: session=7f3a..." { width: 260; height: 70; style.fill: "#e8f5e9" }
lookup: "Server: load session 7f3a ->\nknows the user" { width: 270; height: 80; style.fill: "#e8f5e9" }
login -> create -> cookie -> next -> lookup
```

**Fig. 1.** The id is the only thing crossing the wire repeatedly; everything else lives in server memory or a shared session store.

## Where sessions are stored (the scaling question)

- **Sticky in-memory:** fast, but pins the client to one node and dies on restart — a load-balancing constraint ([[What is the difference between L3 L4 and L7]]: sticky routing is an L7 concern).
- **Shared store:** Redis/memcached/DB — replicas can serve any client; the classic horizontal-scale answer.
- **Client-side tokens:** signed JWTs move the state into the token — no server store, at the cost of revocation difficulty; often paired with a short-lived session cookie pattern ([[What is an HTTP cookie]] carries the attribute vocabulary: HttpOnly, Secure, SameSite).

> [!warning] Session ids are the crown jewels — and sessions are not "the login"
> Predictable or leaked ids are hijacking vectors (session fixation: plant your id, let the victim authenticate into it — mitigate by regenerating ids on login). The cookie must be HttpOnly (no JS access against XSS), Secure (HTTPS-only), SameSite (CSRF mitigation). Two misstatements to avoid: "HTTP sessions make HTTP stateful" — the protocol stays stateless, the *application* adds state; and "session = cookie" — the cookie is one transport for the id, with URL rewriting and JWTs as alternatives ([[What is idempotency in HTTP and in messaging]] is the adjacent discipline for state-changing retries).

Java-side detail: [[How would you explain HTTP sessions in servlet based applications]]; the web-app context: [[What is a web application]].

> [!tip] Interview answer
> An HTTP session is server-side per-client state bridged across stateless requests by an opaque id — usually a cookie like JSESSIONID, with URL rewriting as fallback. I structure the answer around creation, id transport, lookup and expiry, then the scaling fork: sticky in-memory vs shared Redis store vs client-side JWTs. Security closers: HttpOnly/Secure/SameSite attributes and id regeneration on login against fixation.
