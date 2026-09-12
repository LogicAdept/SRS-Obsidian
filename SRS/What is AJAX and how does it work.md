<!--
reps: 0
priority: 0
-->
#Networking/Web #SRS
# What is AJAX and how does it work

> [!abstract] Short answer
> AJAX (Asynchronous JavaScript And XML) is the technique of the browser making HTTP requests from page JavaScript without reloading the page, then updating the DOM with the response — the basis of "dynamic" web applications. The XML in the name is historical: today the payload is JSON, the machinery is XMLHttpRequest or, preferably, fetch() (per MDN), and "async" means the request runs off the page's critical path with a callback/promise continuation.

## The request lifecycle in the page

1. An event fires (click, timer, input).
2. JavaScript issues an HTTP request: `fetch(url, {method, headers, body})` or the older `XMLHttpRequest`.
3. The browser's networking stack sends it like any HTTP request — same-origin policy applies unless the server answers with CORS headers.
4. The callback/promise continuation runs when the response arrives; the code mutates the DOM — no navigation, no full re-render.

```javascript
// Conceptual: the classic AJAX loop
const response = await fetch('/api/cart', { method: 'GET' });
const cart = await response.json();          // JSON today, not XML
document.querySelector('#count').textContent = cart.items.length;
```

**Listing 1.** Fetch the fragment, patch the DOM: the page stays interactive while the request is in flight.

```d2
direction: right
ui: "Page event\n(click / input)" { width: 210; height: 70; style.fill: "#e3f2fd" }
js: "fetch/XHR\nasync request" { width: 200; height: 70; style.fill: "#fff3e0" }
srv: "Server / API\nJSON response" { width: 210; height: 70; style.fill: "#e8f5e9" }
dom: "DOM update\nno page reload" { width: 220; height: 70; style.fill: "#fff3e0" }
ui -> js -> srv -> dom
```

**Fig. 1.** The round trip that replaced the form-submit-and-reload model of the early web.

## Why it mattered and what it enables

- **Partial updates:** bandwidth and latency drop because only data moves, not full pages — the founding idea of SPA frameworks.
- **Asynchrony:** the UI thread is not blocked; multiple requests can be in flight ([[What is the difference between polling and long polling]] builds update loops on this).
- **API reuse:** the same JSON endpoints serve the web client and mobile apps; server-side rendering re-enters later for first-paint performance.

> [!warning] AJAX is a technique, not a protocol — and async does not mean "parallel to everything"
> There is no AJAX protocol: any in-page HTTP call qualifies, and the interview lie "AJAX requires XMLHttpRequest" ignores fetch and the fact that a form POST via JS is the same idea. Two real pitfalls: (1) same-origin/CORS — a cross-origin AJAX call is refused unless the server opts in, which is why "it works in Postman but fails in the browser"; (2) browser limits on concurrent connections per origin shape how many requests an SPA can have in flight ([[What is HTTP]] for the underlying semantics). Also XHR's synchronous mode is deprecated — "AJAX" never required blocking the UI.

Related: [[What is a web application]] (the architecture AJAX enables), [[What is the World Wide Web]] for the static-page baseline it replaced.

> [!tip] Interview answer
> AJAX is the browser-side pattern of issuing asynchronous HTTP calls from JavaScript and patching the DOM with the result — no reload, JSON instead of the historical XML, fetch() as the modern API. I mention CORS as the top production pitfall and close with the architectural consequence: partial updates are what made SPAs and shared JSON APIs possible.
