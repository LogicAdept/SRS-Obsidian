<!--
reps: 0
priority: 0
-->
#Networking/Web/Protocols/HTTP #Networking/DNS #SRS
# What happens when you type a URL into a browser and press Enter

> [!abstract] Short answer
> The browser parses the URL, resolves the hostname via DNS, opens a TCP connection (with a TLS handshake for HTTPS), sends an HTTP request, renders the response incrementally (HTML -> DOM, CSS -> CSSOM, JS executes, resources load), and reuses or closes the connection. The full answer is a pipeline walk through DNS, TCP, TLS, HTTP and rendering — interviewers want the order and the failure points, not the browser's source code.

## The pipeline

1. **Parse the URL:** scheme (HTTP vs HTTPS), host, port, path, query. Invalid or search-like input goes to the search engine; plain HTTP defaults to port 80, HTTPS to 443.
2. **DNS resolution:** browser cache -> OS stub resolver -> recursive resolver with caching ([[What is DNS and how does DNS resolution work]]); result: an IP for the host.
3. **TCP connection:** three-way handshake with that IP:port ([[What is the TCP three-way handshake]]) — one RTT before any HTTP byte moves.
4. **TLS handshake (HTTPS only):** certificate validation, key exchange (TLS 1.3 does it in one round trip after the TCP handshake; session resumption can skip more) — [[What is the difference between HTTP and HTTPS]].
5. **HTTP request:** `GET /path HTTP/1.1` (+Host, headers, cookies) or an HTTP/2 stream on an existing connection ([[What is HTTP]]).
6. **Server processing and response:** the edge proxies to an app server; the response arrives with status, headers (Content-Type, Cache-Control), and the body ([[Which HTTP status codes matter most in REST API design]]).
7. **Rendering:** parse HTML -> DOM; CSS -> CSSOM; layout and paint; discovered subresources (CSS, JS, images) trigger more requests, possibly in parallel over the same HTTP/2 connection; JavaScript may mutate the DOM or fire XHR/fetch calls ([[What is AJAX and how does it work]]).
8. **Connection reuse:** keep-alive/HTTP-2 multiplexing keeps the socket warm for the next request.

```d2
direction: down
u: "Parse URL" { width: 160; height: 55; style.fill: "#e3f2fd" }
d: "DNS: host -> IP" { width: 200; height: 55; style.fill: "#e3f2fd" }
t: "TCP handshake (1 RTT)" { width: 240; height: 55; style.fill: "#fff3e0" }
tls: "TLS handshake (if https)" { width: 250; height: 55; style.fill: "#fff3e0" }
h: "HTTP request / response" { width: 250; height: 55; style.fill: "#e8f5e9" }
r: "Render: DOM, CSSOM, JS,\nsubresource fetches" { width: 280; height: 80; style.fill: "#e8f5e9" }
u -> d -> t -> tls -> h -> r
```

**Fig. 1.** The ordered pipeline; each arrow is a place where latency and failure actually live.

## Where the interview follow-ups point

- **Latency budget:** DNS + TCP + TLS are round trips before the first byte of content — that is why connection reuse, CDN edge caching, and TLS 1.3/QUIC's faster handshakes exist ([[What is HTTP 3 and why does it use QUIC]]).
- **Caching short-circuits:** a cached response (fresh per Cache-Control) skips steps 2–6 entirely; a revalidation may send only a 304 ([[How do you make REST API responses cacheable]]).
- **Failure localization:** "cannot resolve host" = DNS; "connection refused" = TCP/port; certificate warning = TLS; 404/500 = application — this mapping IS the bottom-up troubleshooting grid ([[How do you use a bottom-up OSI approach when troubleshooting]]).

> [!warning] The order is not fixed — redirects, caches and proxies rearrange everything
> A 301 redirect restarts the pipeline at step 2 for a *new* URL; HSTS upgrades HTTP to HTTPS before any request; a corporate proxy may terminate TLS and re-origin the connection; DNS may answer from cache in microseconds. Reciting one rigid sequence "DNS, ARP, TCP..." without the conditionals (cache hit? HTTPS? proxy? HTTP/2 reuse?) is what separates the memorized answer from the understood one — and ARP specifically only ever happens on the *local link* toward the gateway ([[What is ARP and how does it work]]), not "for the web server".

The protocols involved: [[What is HTTP]], [[What is the TCP IP protocol suite]]; the serving side: [[What is a web server]].

> [!tip] Interview answer
> Parse the URL; resolve the host through DNS caches; TCP three-way handshake; TLS handshake for HTTPS; send the HTTP request; server responds; browser renders — DOM/CSSOM/JS — fetching subresources, often multiplexed over the same connection; then keep-alive reuses it. I frame each step with its latency cost and failure mode: DNS failure, refused TCP, certificate warnings, HTTP error codes — that shows the pipeline, not just a memorized list.
