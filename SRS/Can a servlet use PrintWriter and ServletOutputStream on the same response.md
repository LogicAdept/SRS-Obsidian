<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# Can a servlet use PrintWriter and ServletOutputStream on the same response?

> [!abstract] Short answer
> **No — not through both getters on one `ServletResponse`.** `getWriter()` and `getOutputStream()` are exclusive body channels. The second getter throws `IllegalStateException`. The documented exception is `reset()` while the response is still uncommitted: that clears the getter state so the other channel may be opened. Mixed binary-plus-text (multipart) stays on `ServletOutputStream`; you encode character sections yourself. Response API: [[How would you explain the ServletResponse interface]]. Writer vs stream types: [[What is the difference between PrintWriter and PrintStream]].

## One body, one channel

The container gives the servlet a `ServletResponse` (usually `HttpServletResponse`). That object exposes two ways to write the entity body:

- **`getOutputStream()`** — a `ServletOutputStream` for **binary** data. The container does **not** character-encode those bytes.
- **`getWriter()`** — a `PrintWriter` for **character** text. It encodes with `getCharacterEncoding()`. If that encoding was still the unspecified default `ISO-8859-1`, `getWriter` **locks it to `ISO-8859-1`**. JSP `out` is a different writer type: [[What is the difference between JspWriter and servlet PrintWriter]].

Either getter may be used to write the body, **not both**, except after `reset()`. The trigger is **calling** the other getter, not whether you already flushed bytes. Calling `getWriter()` twice is not the forbidden pair; calling `getOutputStream()` after `getWriter()` (or the reverse) is.

`setCharacterEncoding`, `setContentType` (when it carries a charset), and `setLocale` must run **before** `getWriter` and **before** commit, or they do not change the writer charset. After `getWriter`, later charset calls are ignored. An unknown charset makes a later `getWriter()` throw `UnsupportedEncodingException`; binary content can still go out through `getOutputStream()`.

`flush()` on either the `PrintWriter` or the `ServletOutputStream` **commits** the response (status and headers are sent). After commit, `reset()` throws `IllegalStateException`.

```d2
direction: down
resp: "ServletResponse" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
pick: "pick exactly one getter" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
w: "getWriter()\nPrintWriter, charset" {
  width: 220
  height: 56
  style.fill: "#e8f5e9"
}
s: "getOutputStream()\nServletOutputStream, bytes" {
  width: 220
  height: 56
  style.fill: "#fff3e0"
}
bad: "the other getter\nIllegalStateException" {
  width: 240
  height: 50
  style.fill: "#ffebee"
}
rst: "reset() if not committed\nclears getter state" {
  width: 240
  height: 50
  style.fill: "#e3f2fd"
}
resp -> pick
pick -> w
pick -> s
w -> bad
s -> bad
w -> rst
s -> rst
```

**Fig. 1.** One response body channel. The other getter is illegal until an uncommitted `reset()`.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
protected void doGet(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
    resp.setCharacterEncoding("UTF-8");
    resp.setContentType("text/plain");
    PrintWriter writer = resp.getWriter();
    writer.write("hello");
    // resp.getOutputStream(); // IllegalStateException — getter already chosen
}

protected void doPost(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
    PrintWriter writer = resp.getWriter();
    writer.write("will be discarded");
    resp.reset(); // legal only if not committed
    ServletOutputStream out = resp.getOutputStream();
    out.write(new byte[] { 1, 2, 3 });
    // writer.write("no"); // stale after reset — undefined
}
```

**Listing 1.** Choose `getWriter` **or** `getOutputStream`. `reset()` before commit is the specified way to switch; the old writer or stream is then stale.

For mixed binary and text on one response (for example multipart), do **not** call `getWriter()`. Use `getOutputStream()` and write character sections as encoded bytes (an `OutputStreamWriter` you construct yourself is still the stream channel, not `getWriter()`).

> [!warning] `resetBuffer()` does not unlock the other getter
> `resetBuffer()` drops buffered body bytes and leaves status, headers, and the **getter choice** in place. Only `reset()` clears “`getWriter` / `getOutputStream` already called”. After commit, both `reset()` and `resetBuffer()` throw `IllegalStateException`.

> [!warning] A filter or include can already own the channel
> The same `ServletResponse` object travels down the filter chain and into a forward/include. If a filter, error page, or included servlet already called `getWriter()`, your later `getOutputStream()` fails even though **your** method never called `getWriter()`. Flushing anywhere commits the response and blocks `reset()`.

> [!warning] Charset is frozen at `getWriter`
> Set encoding **before** the writer. Skipping that step makes `getWriter` fix `ISO-8859-1`. Wrapping `getOutputStream()` in your own `PrintWriter` is not `getWriter()` and does not run that charset bookkeeping — you then own encoding and buffering.

> [!tip] Interview answer
> You cannot use both ServletResponse getters on one response: getWriter for character text, getOutputStream for bytes, and the second getter throws IllegalStateException. Reset before commit is the specified switch, and the old writer or stream is then stale. For mixed binary and text, stay on ServletOutputStream and encode the character parts yourself.
