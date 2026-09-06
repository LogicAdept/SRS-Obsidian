<!--
reps: 0
priority: 0
-->
#Java/Servlet/Context #SRS

# How do you get server information from a servlet?

> [!abstract] Short answer
> **Container product:** `getServletContext().getServerInfo()` — `servername/versionnumber`, optionally extra text in parentheses. **Servlet spec the container implements:** `getMajorVersion()` / `getMinorVersion()`. **Spec level of this app:** `getEffectiveMajorVersion()` / `getEffectiveMinorVersion()`. **This request’s server host/port:** `request.getServerName()` / `getServerPort()` (often `Host` / HTTP authority / RFC 7239). **Local NIC:** `getLocalName()`, `getLocalAddr()`, `getLocalPort()`. Context: [[How would you explain ServletContext in Java web applications]]. Request: [[How would you explain the ServletRequest interface]]. Client address is different: [[How do you get the client IP address in a servlet]].

## Context vs this request

`ServletContext` answers “what am I running in?”. `ServletRequest` answers “where did **this** connection land?”

| API | Returns |
| --- | --- |
| `ServletContext.getServerInfo()` | Container name and version, form `servername/versionnumber` (example in the API: `JavaServer Web Dev Kit/1.0`). Optional parenthetical extras are allowed. |
| `getMajorVersion()` / `getMinorVersion()` | Jakarta Servlet spec **X.Y that this container supports** (`X` and `Y` as ints). |
| `getEffectiveMajorVersion()` / `getEffectiveMinorVersion()` | Spec version **this web app is based on** — may differ from the container’s supported pair. |
| `getVirtualServerName()` | **Configuration name of the logical host** (virtual hosting). Same for every context on that host; **stable and distinct**; **not** required to be a hostname or IP. |
| `ServletRequest.getServerName()` / `getServerPort()` | Host and port **the request was sent to** — protocol mechanism (`Host`, HTTP/2 authority, RFC 7239) or else resolved name / listen port. |
| `getLocalName()` / `getLocalAddr()` / `getLocalPort()` | Interface that **received** the request (FQDN of that address, or the IP if the engine skips reverse DNS). RFC 7239 may still substitute. |
| `getScheme()` / `getProtocol()` | Scheme (`http`, `https`, …) and protocol string (`HTTP/1.1`). |

From `HttpServlet`, `getServletContext()` is on `GenericServlet` / `ServletConfig`. From a request, `getServletContext()` is the context of the **last dispatch**.

```d2
direction: down
q: "what server am I on?" {
  width: 260
  height: 40
  style.fill: "#fff8e1"
}
ctx: "ServletContext\ngetServerInfo, versions, virtual host" {
  width: 280
  height: 56
  style.fill: "#e3f2fd"
}
req: "ServletRequest\ngetServerName/Port vs getLocal*" {
  width: 280
  height: 56
  style.fill: "#e8f5e9"
}
q -> ctx
q -> req
```

**Fig. 1.** Product/version live on the context. Host and bind address live on the request.

```java
// Conceptual — jakarta.servlet, Servlet 6.1
protected void doGet(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
    ServletContext ctx = getServletContext();
    resp.setContentType("text/plain;charset=UTF-8");
    resp.getWriter().printf(
            "container=%s%nservlet-api=%d.%d (app effective %d.%d)%n"
                    + "virtual-host=%s%n"
                    + "sent-to=%s:%d scheme=%s protocol=%s%n"
                    + "local=%s/%s:%d%n",
            ctx.getServerInfo(),
            ctx.getMajorVersion(), ctx.getMinorVersion(),
            ctx.getEffectiveMajorVersion(), ctx.getEffectiveMinorVersion(),
            ctx.getVirtualServerName(),
            req.getServerName(), req.getServerPort(),
            req.getScheme(), req.getProtocol(),
            req.getLocalName(), req.getLocalAddr(), req.getLocalPort());
}
```

**Listing 1.** Container identity and spec numbers from the context; per-request host vs local interface from the request.

Disk path of the app is **`getRealPath`**, not server info ([[How do you get the real filesystem path of a servlet on the server]]). Temporary dir is the `jakarta.servlet.context.tempdir` context attribute.

> [!warning] `getServerName` is not “the machine’s hostname”
> Proxies, `Host` headers, HTTP/2 authority, and RFC 7239 forwarded data can differ from `getLocalAddr()`. Do not treat `getVirtualServerName()` as DNS either — it is a **logical-host config key** for virtual hosting ([[What typical responsibilities does a servlet container have]]).

> [!warning] Container version ≠ application `web.xml` version
> A Servlet 6.1 container can still report **effective** 5.0/6.0 for an older descriptor. Logging `getServerInfo()` plus **both** version pairs avoids mixing “what the engine can do” with “what this WAR declared.”

> [!warning] `getRemote*` is the other end
> `getRemoteAddr` / `getRemoteHost` / `getRemotePort` describe the **client (or last proxy)**, not the server. Using them for “server information” is the usual mix-up.

> [!tip] Interview answer
> I use ServletContext.getServerInfo for the container name and version string, and getMajorVersion with getMinorVersion for the Servlet API the engine supports. Effective major/minor is the spec level of this application. For the host and port of this request I use getServerName and getServerPort, and getLocalAddr when I need the interface that actually accepted the connection.
