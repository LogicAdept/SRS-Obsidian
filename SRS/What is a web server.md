<!--
reps: 0
priority: 0
-->
#Networking/Web #SRS
# What is a web server

> [!abstract] Short answer
> A web server is software (or the machine running it) that accepts HTTP requests and returns HTTP responses — mostly static files from disk (HTML, CSS, JS, images) and increasingly reverse-proxying or load-balancing to backends. NGINX, Apache httpd, Caddy, IIS are the canonical names; MDN's definition captures the dual meaning: hardware + software working together.

## What it does per request

1. **Listen** on a port (80/443/8080) and accept TCP connections; terminate TLS if HTTPS ([[What is the difference between HTTP and HTTPS]]).
2. **Parse** the request line and headers (method, path, Host, headers) — the serving side of [[What is HTTP]].
3. **Match** the path to a handler: file from the document root (with MIME type by extension — [[What is a MIME type]]), redirect/rewrite rule, cache hit, or proxy_pass to an upstream.
4. **Respond** with status, headers (Content-Type, Content-Length, Cache-Control, Set-Cookie) and body; log the transaction.
5. **Concurrency:** one thread/process per connection (classic Apache prefork), or event-loop + worker processes (NGINX) — the reason NGINX holds tens of thousands of idle keep-alive connections cheaply ([[What is the difference between HTTP 1.1 and HTTP 2]] interacts with keep-alive behavior).

```d2
direction: down
c: "Client (browser)" { width: 200; height: 60; style.fill: "#e3f2fd" }
ws: "Web server\nTLS, parse, static files,\nrewrite, cache, proxy" { width: 300; height: 100; style.fill: "#fff3e0" }
app: "Application server / API\n(business logic)" { width: 280; height: 80; style.fill: "#e8f5e9" }
fs: "Document root\nHTML, CSS, JS, images" { width: 240; height: 80; style.fill: "#f3e5f5" }
c -> ws
ws -> fs: "static hit"
ws -> app: "proxy_pass / FastCGI"
```

**Fig. 1.** The web server as edge: static content served directly, dynamic work delegated to the application tier.

## Where it sits in the stack

The web server is the *serving tier* — often also the reverse proxy and load balancer in front of application servers ([[What is the difference between a web server and an application server]] covers the division of labor). Its HTTP-level duties matter for the whole system: compression ([[What is GZIP and how do you enable HTTP response compression in Spring Boot]]), TLS termination, rate limiting, redirects, cache headers.

> [!warning] "Web server cannot execute code" is outdated, and "NGINX replaces the app server" is wrong
> Modern web servers run dynamic code through modules (mod_php historically, njs, Lua in OpenResty) — the real boundary is *purpose*: a web server optimizes HTTP serving/proxying; an application server hosts the application runtime (servlet container, Node process, WSGI). Also, a web server is not synonymous with "the machine": one box can run many web servers behind one load balancer, and one web server can front hundreds of containers ([[What is the difference between L3 L4 and L7]] for where load balancing happens).

Sibling tier: [[What is an application server]]; the full request path: [[What happens when you type a URL into a browser and press Enter]].

> [!tip] Interview answer
> A web server accepts HTTP(S), parses requests, serves static content by MIME type, applies rewrites and caching, and reverse-proxies dynamic work to application servers — NGINX, Apache, Caddy are the defaults. Its two production jobs I stress: TLS termination at the edge and event-loop concurrency that keeps many idle connections cheap. It hosts no business logic — that is the application server's tier.
