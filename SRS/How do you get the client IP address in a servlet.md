<!--
reps: 0
priority: 0
-->
#Java/Servlet #Networking/Web/Protocols/HTTP #SRS

# How do you get the client IP address in a servlet?

> [!abstract] Short answer
> Call **`ServletRequest.getRemoteAddr()`** (on `HttpServletRequest` in an HTTP servlet). That is the IP of the **remote end of the connection**: the **client or the last proxy**, unless the container applies a protocol mechanism such as **RFC 7239 `Forwarded`**. **`getRemoteHost()`** is the FQDN of that same address, or the IP if the engine skips reverse DNS. **`getRemotePort()`** is that remote port. Server bind address is **`getLocalAddr()`**, not the client: [[How do you get server information from a servlet]]. Request API: [[How would you explain the ServletRequest interface]].

## Remote end of the connection

There is no separate “client IP” method. `getRemoteAddr()` returns a `String` IP for the **remote end** of the connection on which the request was received. By default that is the **client or last proxy** that sent the request. The container **may** instead take an address from a protocol-specific mechanism (the Servlet API names **RFC 7239**), which can differ from the TCP peer.

`getRemoteHost()` resolves **that** address to a hostname when the engine both can and chooses to; otherwise it returns the IP (skipping DNS is allowed for performance). `getRemotePort()` is the remote IP port, with the same default (client or last proxy) and the same optional RFC 7239 substitution.

HTTP reverse proxies sit on the TCP connection the servlet sees. Without container support for `Forwarded`, `getRemoteAddr()` is typically the **proxy**, not the browser. RFC 7239’s `Forwarded` `for=` parameter is the standardized way to disclose the originating client through trusted proxies; non-standard `X-Forwarded-For` is **not** a Servlet API.

```d2
direction: right
browser: "browser" {
  width: 100
  height: 40
  style.fill: "#e8f5e9"
}
proxy: "proxy" {
  width: 100
  height: 40
  style.fill: "#fff8e1"
}
srv: "servlet\ngetRemoteAddr" {
  width: 160
  height: 48
  style.fill: "#e3f2fd"
}
browser -> proxy: "TCP"
proxy -> srv: "TCP peer"
```

**Fig. 1.** Default `getRemoteAddr()` is the TCP remote peer — often the last proxy.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
protected void doGet(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
    String ip = req.getRemoteAddr();
    String host = req.getRemoteHost(); // may equal ip
    int port = req.getRemotePort();
    resp.setContentType("text/plain;charset=UTF-8");
    resp.getWriter().printf("remote=%s host=%s port=%d%n", ip, host, port);
}
```

**Listing 1.** Client (or last hop) identity from the request. Do not use `getLocalAddr()` here.

> [!warning] Last proxy is still “the client” to TCP
> Interview answers that always print `getRemoteAddr()` as “the user’s home IP” fail behind a load balancer. Trust **container-configured** forwarded identity, not a raw header the browser can send. Forged `Forwarded` / `X-Forwarded-For` from the public Internet is not a substitute for `getRemoteAddr()`.

> [!warning] `getRemoteHost()` is not a second source of truth
> It names **`getRemoteAddr()`’s** address. If DNS is off or fails, you get the **same IP string**. Do not treat a hostname here as proof of identity.

> [!warning] Local vs remote
> `getLocalAddr()` / `getLocalPort()` are the **interface that accepted** the request. Mixing them with `getRemote*` is the usual mix-up with [[How do you get server information from a servlet]].

> [!tip] Interview answer
> I use request.getRemoteAddr for the client IP. That is the remote end of the TCP connection, so with a reverse proxy it is often the proxy unless the container applies RFC 7239 Forwarded. getRemoteHost is just a possible DNS name for that address, and getLocalAddr is the server side, not the client.
