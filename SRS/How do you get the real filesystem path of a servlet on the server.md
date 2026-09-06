<!--
reps: 0
priority: 0
-->
#Java/Servlet/Context #SRS

# How do you get the real filesystem path of a servlet on the server?

> [!abstract] Short answer
> Use **`ServletContext.getRealPath(virtualPath)`**. Pass a context-relative virtual path (prefer a leading **`/`**; if you omit it, the container pretends you wrote `/` + path). You get an **OS-native** absolute file path, or **`null`** when there is no local file (unexploded WAR, remote FS, database). That is **not** the `.class` file of your servlet type. Extra path info on **this request** is **`HttpServletRequest.getPathTranslated()`**. Context: [[How would you explain ServletContext in Java web applications]]. Path parts: [[How is an HttpServlet request processed]].

## Virtual path → local file, if any

The spec groups two **path translation** helpers:

- **`getServletContext().getRealPath(path)`** — file-system string for a **virtual path** under this context (for example `"/index.html"` maps like the URL that would serve that document). Separators match the host OS.
- **`request.getPathTranslated()`** — real path of this request’s **`pathInfo`** only. `null` if there is no extra path, or if translation is impossible. The container **does not decode** that string.

Translation **must** return **`null`** when the container cannot name a local file: app run **from an archive**, **remote** store, or **database**. `META-INF/resources` inside `WEB-INF/lib` JARs count **only if already unpacked**; then `getRealPath` returns that unpacked location.

To **read** app content without a disk path, use **`getResource` / `getResourceAsStream`** — those work from a WAR. A writable scratch dir is the context attribute **`jakarta.servlet.context.tempdir`** (`java.io.File`), not `getRealPath`.

```d2
direction: down
virt: "virtual path /WEB-INF/data.txt" {
  width: 280
  height: 40
  style.fill: "#fff8e1"
}
rp: "getRealPath\nOS file or null" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
res: "getResource(AsStream)\nworks from WAR" {
  width: 240
  height: 48
  style.fill: "#e3f2fd"
}
virt -> rp
virt -> res
```

**Fig. 1.** Filesystem translation can fail. Resource lookup does not need a real path.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
protected void doGet(HttpServletRequest req, HttpServletResponse resp)
        throws ServletException, IOException {
    ServletContext ctx = getServletContext();
    String root = ctx.getRealPath("/");           // context root, or null
    String file = ctx.getRealPath("/WEB-INF/data.txt");
    String extra = req.getPathTranslated();       // pathInfo on disk, or null
    File tmp = (File) ctx.getAttribute("jakarta.servlet.context.tempdir");
    if (file == null) {
        try (InputStream in = ctx.getResourceAsStream("/WEB-INF/data.txt")) {
            // packed WAR: no File, still readable
        }
    }
}
```

**Listing 1.** `getRealPath` for a named virtual path; `getPathTranslated` for extra path info; stream fallback when `null`.

> [!warning] Packed WAR → `null`, not an exception
> `getRealPath("/")` is **not** guaranteed on production exploded-vs-packed layouts. `NullPointerException` on `new File(getRealPath(...))` is the usual crash. Prefer `getResourceAsStream` for classpath/WAR content.

> [!warning] Not the servlet class file, and not a sandbox
> This API does **not** locate `MyServlet.class`. It **bypasses** implicit `WEB-INF` / `META-INF` hiding and explicit security constraints. Do not concatenate **unsanitized** client path segments into `getRealPath`. The argument is canonicalized before matching — still do not treat the result as safe to expose or execute from user input.

> [!warning] `getPathTranslated` is only `pathInfo`
> `requestURI = contextPath + servletPath + pathInfo`. No extra path → `getPathTranslated()` is `null` even when `getRealPath("/")` works. Do not confuse with `getServletPath()` (URL mapping, not a file).

> [!tip] Interview answer
> I call getServletContext().getRealPath with a slash-leading virtual path and I handle null when the app is not exploded on disk. getPathTranslated is only the extra pathInfo of this request, translated the same way. To read a resource I use getResourceAsStream instead of assuming a File.
