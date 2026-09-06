<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# How would you explain the ServletResponse interface?

> [!abstract] Short answer
> **`ServletResponse` is the protocol-neutral view of one outgoing reply.** The container **creates** it and passes it into **`service` / `doFilter`**. You set **content type, length, locale, charset**, then write with **`getWriter()`** (characters) **or** **`getOutputStream()`** (bytes) — **not both**, unless you **`reset()`**. Buffering, **commit**, and **`reset` / `resetBuffer`** live here. HTTP status, headers, **`sendError` / `sendRedirect`** are **`HttpServletResponse`**. Pair: [[How would you explain the ServletRequest interface]]. Writer vs stream: [[Can a servlet use PrintWriter and ServletOutputStream on the same response]]. Redirect vs forward: [[How does sendRedirect differ from forward in servlets]].

## Buffer, charset, commit, close

**Body.** `getWriter()` returns a **`PrintWriter`** using **`getCharacterEncoding()`**. `getOutputStream()` returns a **`ServletOutputStream`** with **no** charset conversion. Calling **`flush()`** on either **commits**. Mixing binary and text in one body means **stream only**, and you encode the text yourself. After **`reset()`**, the writer/stream choice is **cleared** (stale objects are **undefined**). JSP’s writer: [[What is the difference between JspWriter and servlet PrintWriter]].

**Charset.** Set it **before `getWriter` and before commit**: **`setCharacterEncoding`** (String, or **`Charset` since 6.1**), **`setContentType("text/html;charset=UTF-8")`**, or implicitly **`setLocale`**. Explicit charset **wins** over `setLocale`. After `getWriter` or commit, those calls **do not change** encoding. If still unset, the writer uses **`ISO-8859-1`**. App-wide: `<response-character-encoding>` / `ServletContext.setResponseCharacterEncoding`. **`setLocale` after commit is a no-op**; if you never set locale, the **container default** is used and HTTP **`Content-Language` is not specified**. The container **must not invent a default `Content-Type`**.

**Buffer.** Optional. `getBufferSize()` is **0** if none. `setBufferSize` asks for a **minimum**; call it **before any body** or it throws **`IllegalStateException`**. Filling the buffer **flushes immediately** and **commits** if that is the first bytes to the client. **`isCommitted`**: status and headers have gone. **`flushBuffer`** forces that. **`reset`** (uncommitted only) clears **buffer, headers, status, and writer/stream state**. **`resetBuffer`** clears **body only**. Either method **throws** if already committed.

**Close.** The container **flushes remaining buffer** when the response closes: **`service` returns**, **`setContentLength` / `setContentLengthLong` bytes have been written** (length **> 0**), **`sendError`**, **`sendRedirect`**, or **`AsyncContext.complete`**. `sendError` / `sendRedirect` **commit and terminate**; further writes are **ignored**; if already committed they throw **`IllegalStateException`**. Headers after commit (except trailers) are **ignored**.

**Lifetime.** Valid only in **`service` / `doFilter`**, unless the matching request **`startAsync`** — then until **`complete`**. Containers **recycle** the object. Filters: [[How would you explain servlet filters and request interception]].

```d2
direction: down
set: "setContentType / charset / locale / buffer" {
  width: 300
  height: 40
  style.fill: "#fff8e1"
}
xor: "getWriter XOR getOutputStream" {
  width: 280
  height: 40
  style.fill: "#e3f2fd"
}
buf: "buffer → flush → committed" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
done: "service returns or content-length met" {
  width: 300
  height: 40
  style.fill: "#e8f5e9"
}
set -> xor
xor -> buf
buf -> done
```

**Fig. 1.** Charset and headers must be set **before** the first flush. Commit is one-way.

```java
// Conceptual — jakarta.servlet, Servlet 6.1
@Override
public void service(ServletRequest req, ServletResponse resp) throws IOException {
    resp.setCharacterEncoding(java.nio.charset.StandardCharsets.UTF_8);
    resp.setContentType("text/plain;charset=UTF-8");
    resp.setBufferSize(8192);
    try (var out = resp.getWriter()) { // IllegalStateException if getOutputStream() already used
        out.write("ok");
    } // flush/close of the writer commits
}
```

**Listing 1.** Set **charset before `getWriter`**. Default encoding is **ISO-8859-1**. HTTP status codes stay on **`HttpServletResponse`**.

> [!warning] Commit is a one-way door
> First bytes to the client **lock** status, headers, charset, and buffer size. Then **`reset` / `resetBuffer` / `setBufferSize` / `sendRedirect` / `sendError` throw**, and late **`setContentType` is ignored**. Do not `flush` until you are done with headers.

> [!warning] `getWriter` and `getOutputStream` share one body
> The second call throws **`IllegalStateException`** unless **`reset()`** ran in between. `reset()` after commit is illegal. Writing past **`setContentLength`** can **close** the response early while `service` is still running.

> [!tip] Interview answer
> ServletResponse is how I send the body: set content type and charset, then either a PrintWriter or a ServletOutputStream, never both unless I reset. Buffering delays commit so I can still change headers; the first flush to the client commits. HTTP status, setHeader, sendError, and sendRedirect are on HttpServletResponse, and the object is only valid for this service call unless async is started.
