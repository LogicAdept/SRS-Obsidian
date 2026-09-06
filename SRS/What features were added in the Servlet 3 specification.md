<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/JavaEE #SRS

# What features were added in the Servlet 3 specification?

> [!abstract] Short answer
> **Servlet 3.0** (**JSR 315**, Java EE **6**, final **10 Dec 2009**) added **pluggability**, **annotation registration**, **async request processing**, **multipart upload**, and **programmatic login**. Headline APIs: **`@WebServlet` / `@WebFilter` / `@WebListener`**, **`META-INF/web-fragment.xml`**, **`ServletContainerInitializer`**, **`ServletContext.addServlet`**, **`ServletRequest.startAsync` / `AsyncContext`**, **`@MultipartConfig` / `getParts()`**, **`HttpServletRequest.login` / `logout` / `authenticate`**, **`@ServletSecurity`**. **Non-blocking I/O did not ship** (that is **3.1**). Survey of 2.5–4.0: [[How would you explain what in Servlet 2.5 3.0 3.1 4.0]]. Filters: [[How would you explain servlet filters and request interception]]. Lifecycle vs async: [[How does a servlet container manage the servlet lifecycle]].

## What 3.0 actually shipped

JSR 315’s **proposal** listed more (Comet channels, non-blocking streams). The **3.0 final** is the list below (`javax.servlet`). Package rename is **5.0**, not 3.0.

| Theme | 3.0 feature |
| --- | --- |
| **Ease of development** | **`@WebServlet`**, **`@WebFilter`**, **`@WebListener`**, **`@WebInitParam`**. `web.xml` may be **absent** or used to **override**. |
| **Pluggability** | **`web-fragment.xml`** in `META-INF` of `WEB-INF/lib` JARs; **ordering**; **`ServletContainerInitializer`** + **`@HandlesTypes`**; **`addServlet` / `addFilter` / `addListener`** during startup only. |
| **Async** | **`asyncSupported`** (default **`false`**). **`startAsync`**, **`AsyncContext.complete` / `dispatch`**, async listeners. Frees the **container thread**; the **stream can still block**. |
| **Upload** | **`@MultipartConfig`** / `<multipart-config>`; **`HttpServletRequest.getPart` / `getParts`**. |
| **Security** | **`login` / `logout` / `authenticate`**; **`@ServletSecurity`** (not EE **`@RolesAllowed`** on the servlet). |
| **Resources / cookies** | Static files and JSPs from a JAR’s **`META-INF/resources`**. **HttpOnly** and **`SessionCookieConfig`**. |
| **Request helpers** | **`ServletRequest.getServletContext`**, dispatcher type, async flags. |

**`metadata-complete="true"`** (3.0+): skip **annotation and fragment** scan (unlike 2.5, which only skipped annotations). **`web.xml` wins** over fragments and annotations.

```d2
direction: down
ann: "@WebServlet / fragments / SCI" {
  width: 260
  height: 40
  style.fill: "#e8f5e9"
}
async: "startAsync / AsyncContext" {
  width: 240
  height: 40
  style.fill: "#e3f2fd"
}
nio: "3.1 ReadListener / WriteListener" {
  width: 260
  height: 40
  style.fill: "#fff3e0"
}
ann -> async: "3.0"
async -> nio: "not 3.0"
```

**Fig. 1.** **3.0 = annotations + fragments + async + parts + login.** **NIO is 3.1.**

```java
// Conceptual — Servlet 3.0 (javax.servlet)
@WebServlet(urlPatterns = "/upload", asyncSupported = true)
@MultipartConfig
public class UploadServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws Exception {
        Part file = req.getPart("file"); // 3.0 multipart
        AsyncContext ac = req.startAsync(); // 3.0 async, not 3.1 NIO
        ac.start(() -> { /* work; then ac.complete() */ });
    }
}
```

**Listing 1.** Three 3.0 APIs on one class. **`setReadListener` would be 3.1** and is omitted.

> [!warning] JSR 315 NIO / Comet is not Servlet 3.0
> The JSR text asked for **non-blocking input/output**. That landed in **Servlet 3.1** (`ReadListener` / `WriteListener`), and **only** after async or HTTP upgrade. Interview lists that put **NIO in 3.0** are mixing the **proposal** with the **final**. **`@WebServlet` is not 2.5.** **`value` and `urlPatterns` together** on `@WebServlet` is **illegal**. Fragment file name is **`web-fragment.xml`**, not `fragment.xml`.

> [!warning] `asyncSupported` defaults to false
> A 3.0 **`startAsync`** on a servlet or filter that did not opt in fails. Programmatic **`addServlet`** is legal only from a **declared / annotated listener** or **`ServletContainerInitializer.onStartup`** — not from an arbitrary **`service`**. **`getParts()`** without **`@MultipartConfig` / `<multipart-config>`** is not the 3.0 upload contract.

> [!tip] Interview answer
> Servlet 3.0 is Java EE 6, December 2009: drop most of web.xml with @WebServlet, plug frameworks in with web-fragment.xml and ServletContainerInitializer, process requests asynchronously with startAsync, read uploads with getParts, and call login or logout from code. I do not put non-blocking I/O on that list; that is 3.1.
