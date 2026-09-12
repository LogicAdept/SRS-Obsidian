<!--
reps: 0
priority: 0
-->
#Networking/Web #SRS
# What is a web application

> [!abstract] Short answer
> A web application is software whose client runs in the browser (HTML/CSS/JavaScript), whose server side exposes logic and data over HTTP(S), and whose "installation" is a URL — updates deploy to the server and every user gets them on the next load. It differs from a static site (only served documents) and from a classic desktop app (local install, local state).

## Architecture in three tiers

1. **Browser client.** Renders the UI; state lives in the page (or SPA frameworks); persistence client-side via cookies, localStorage/IndexedDB. Talks only HTTP(S) (plus WebSocket upgrades) — the browser is the runtime and the sandbox ([[What is the difference between polling and long polling]] for its asynchronous options).
2. **Application server / backend.** Business logic and APIs (REST/GraphQL/gRPC-web), sessions, auth; often behind reverse proxies and load balancers ([[What is an application server]], [[What is a web server]] for the serving tier).
3. **Data tier.** Databases, caches, object storage; the backend owns it — the browser never talks to the DB directly.

```d2
direction: right
ui: "Browser client\nHTML/CSS/JS, SPA state" { width: 250; height: 90; style.fill: "#e3f2fd" }
api: "Backend\nHTTP API, auth, sessions" { width: 250; height: 90; style.fill: "#fff3e0" }
db: "Data tier\nDB, cache, storage" { width: 220; height: 80; style.fill: "#e8f5e9" }
ui -> api -> db
```

**Fig. 1.** The canonical three tiers; every arrow is an HTTP(S) or internal protocol call.

## What makes it "web" rather than a website

- **Behavior, not just content:** server-side processing (forms, transactions) plus client-side interactivity (fetch/XHR updating the page without reloads — [[What is AJAX and how does it work]]).
- **Session and identity:** cookies + server sessions or tokens ([[What is an HTTP cookie]], [[What is an HTTP session]]).
- **Zero-install updates and multi-tenant scale:** the deployment story that defines the model — and its costs: latency sensitivity, browser fragmentation, and statelessness of HTTP shaping API design ([[Why is REST stateless]]).

> [!warning] "Web application" is not the same as "site with forms", and the browser is a hostile runtime
> The boundary interviewers probe: a *website* mostly publishes; a *web application* executes user-specific workflows with state and authorization. Two real constraints of the platform: the client can never be trusted (validation happens server-side; the client is observability, not security), and cross-origin rules (CORS/same-origin) shape the API surface — an SPA on another domain must be explicitly allowed by the server. And offline capability is not free: service workers and caching are add-on engineering, not defaults ([[What is GZIP and how do you enable HTTP response compression in Spring Boot]] shows the transfer-optimization side).

Related serving-tier cards: [[What is the difference between a web server and an application server]], [[Which HTTP status codes matter most in REST API design]].

> [!tip] Interview answer
> A web application is browser-client + HTTP backend + server-owned data tier, delivered by URL and updated server-side. The distinction I draw: static site serves documents; a web app runs workflows with sessions and authorization. I also name the platform's twin realities: the client is untrusted, and HTTP statelessness pushes session/state design (cookies, tokens) into the architecture.
