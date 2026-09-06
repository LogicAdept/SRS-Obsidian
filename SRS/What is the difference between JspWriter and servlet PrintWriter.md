<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# What is the difference between JspWriter and servlet PrintWriter?

> [!abstract] Short answer
> **`JspWriter`** is the JSP implicit **`out`**: a **`java.io.Writer`** that **buffers** (by default) and sits **in front of** the response. **`PrintWriter`** is what **`ServletResponse.getWriter()`** returns for a **servlet**. JSP authors **must not** write to that **`PrintWriter`** or the **`OutputStream`**. **`JspWriter.print` throws `IOException`**; **`PrintWriter.print` does not**. Buffering / `autoFlush` / `clear` exist on **`JspWriter` only**. What JSP is: [[What is Java Server Pages JSP]]. Servlet writer: [[How would you explain the ServletResponse interface]]. Error pages vs a flushed buffer: [[How would you explain error context attributes in servlet error handling]].

## Interposed buffer vs the response writer

Jakarta Pages **4.0**: template and actions write to **`out`**, type **`jakarta.servlet.jsp.JspWriter`**. That object **may differ** from **`response.getWriter()`** and is **interposed** to implement the **`page`** directive **`buffer`**.

| | **`JspWriter` (`out`)** | **`PrintWriter` (`response.getWriter()`)** |
| --- | --- | --- |
| **Where** | JSP / tag files | Servlet (and the **backing** stream under `out`) |
| **Type** | Abstract **`Writer`**; **emulates** some **`PrintWriter` / `BufferedWriter`** | **`java.io.PrintWriter`** |
| **`print` / `println`** | **`throws IOException`** | **No `IOException`** (check **`checkError()`**) |
| **Buffer** | Default **≥ 8kb**. **`buffer="none"`** writes through to the response **`PrintWriter`**. | Response buffer is **`ServletResponse`**, not `clear()`/`getRemaining()` |
| **Overflow** | **`autoFlush=true`** (default) **flush**; **`false`** → **`IOException`**. Illegal with **`buffer=none`**. | N/A as JSP `autoFlush` |
| **Discard buffer** | **`clear()`** fails if **already flushed**; **`clearBuffer()`** does not | No JSP `clear` |

Until a **buffered** `JspWriter` **flushes**, **`setContentType`** (and similar) remain legal because the **response `PrintWriter` may not exist yet**. Nested actions may **temporarily replace `out`** with another **buffered** `JspWriter`; **flush** that nested stream or its content is **discarded**. **`BodyContent`** uses **`UNBOUNDED_BUFFER`**.

A servlet uses **`getWriter()`** **or** **`getOutputStream()`**, not both. JSP already owns **`out`**.

```d2
direction: down
jsp: "JSP out : JspWriter\n(buffer, autoFlush, clear)" {
  width: 280
  height: 48
  style.fill: "#e8f5e9"
}
pw: "ServletResponse PrintWriter" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
jsp -> pw: "flush / buffer=none"
```

**Fig. 1.** **`out` is not `getWriter()`** until the JSP buffer **commits** through.

```jsp
<%-- Conceptual — Jakarta Pages 4.0 --%>
<%@ page buffer="8kb" autoFlush="true" %>
<%
    out.print("hello");           // JspWriter; may throw IOException
    // response.getWriter().print("no");  // prohibited on a JSP
%>
```

**Listing 1.** Write **`out`**, not **`response.getWriter()`**. A servlet has no **`out`**; it calls **`getWriter()`** itself.

> [!warning] Do not mix `out` and `response.getWriter()`
> The spec **prohibits** JSP authors from writing to the response **`PrintWriter` or `OutputStream`**. Doing so **duplicates** or **interleaves** bytes with the **`JspWriter` buffer** and can **commit** the response so **`clear()` / `setContentType` / `errorPage` fail**.

> [!warning] `PrintWriter` hides I/O failures
> **`out.print`** can throw. **`getWriter().print`** usually **does not**. After **`autoFlush=true`** has **flushed**, a later **`errorPage` forward may fail**. **`clear()`** after a flush is **`IOException`**; use **`clearBuffer()`** only to drop **unflushed** bytes.

> [!tip] Interview answer
> JspWriter is the JSP implicit out: a Writer with a page buffer, autoFlush, and print methods that throw IOException. The servlet PrintWriter is response.getWriter(), which I use in a servlet and must not use from a JSP. Buffering is why a JSP can still change content type until out flushes through to that PrintWriter.
