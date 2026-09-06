<!--
reps: 0
priority: 0
-->
#Java/Servlet/Filters #SRS

# What servlet wrapper classes exist?

> [!abstract] Short answer
> Four **decorator** types since **Servlet 2.3**: **`ServletRequestWrapper`**, **`ServletResponseWrapper`**, and the HTTP subclasses **`HttpServletRequestWrapper`**, **`HttpServletResponseWrapper`**. Each **implements** the matching request/response interface, **holds** the wrapped object, and **delegates** every method unless you **override**. Use them in a **filter** (or before **`RequestDispatcher`**) to change parameters, body, or headers **without** reimplementing the whole interface. Filters: [[How would you explain servlet filters and request interception]]. Dispatch: [[How would you explain the servlet RequestDispatcher for forward and include]]. Request API: [[How would you explain the ServletRequest interface]]. Response: [[How would you explain the ServletResponse interface]].

## Four classes, Wrapper / Decorator

Jakarta Servlet **6.1**:

| Class | Wraps | Extends |
| --- | --- | --- |
| **`jakarta.servlet.ServletRequestWrapper`** | `ServletRequest` | `Object` |
| **`jakarta.servlet.http.HttpServletRequestWrapper`** | `HttpServletRequest` | `ServletRequestWrapper` |
| **`jakarta.servlet.ServletResponseWrapper`** | `ServletResponse` | `Object` |
| **`jakarta.servlet.http.HttpServletResponseWrapper`** | `HttpServletResponse` | `ServletResponseWrapper` |

**`getRequest()` / `setRequest()`** (and **`getResponse()` / `setResponse()`**) access the wrappee. **`null`** wrappee → **`IllegalArgumentException`**. **`isWrapperFor(instance)`** and **`isWrapperFor(Class)`** walk the chain (**Servlet 3.0**).

**Dispatcher (§9.2):** `forward`/`include` may take the **original** `service` arguments **or** subclasses of these wrappers, and those wrappers **must wrap** the objects the **container** passed in.

**Async `startAsync(req, res)`:** arguments MUST be those originals **or** subclasses of **`ServletRequestWrapper` / `ServletResponseWrapper`**.

These are **not** `Integer`/`Boolean` **language wrappers**.

```d2
direction: down
app: "your HttpServletRequestWrapper" {
  width: 280
  height: 40
  style.fill: "#e8f5e9"
}
http: "HttpServletRequestWrapper" {
  width: 240
  height: 36
}
base: "ServletRequestWrapper" {
  width: 220
  height: 36
  style.fill: "#fff8e1"
}
orig: "container HttpServletRequest" {
  width: 240
  height: 36
}
app -> http -> base -> orig: "delegates"
```

**Fig. 1.** Override **`getParameter`** (or **`getWriter`**) on the **HTTP** wrapper; everything else **calls through**.

```java
// Conceptual — Jakarta Servlet 6.1
public class TrimRequest extends HttpServletRequestWrapper {
    public TrimRequest(HttpServletRequest req) { super(req); }

    @Override
    public String getParameter(String name) {
        String v = super.getParameter(name);
        return v == null ? null : v.trim();
    }
}
// in doFilter: chain.doFilter(new TrimRequest(req), resp);
```

**Listing 1.** Filter passes a **wrapper** down the chain. Un-overridden methods still hit the **container** request.

> [!warning] Wrappers must wrap the container objects
> A homemade class that **implements `HttpServletRequest` from scratch** is **not** a legal dispatcher/`startAsync` wrapper. The spec requires **subclasses of the 2.3 wrapper types** around the **original** request/response.

> [!warning] Override both stream and writer if you wrap the body
> Changing only **`getWriter()`** leaves **`getOutputStream()`** on the **raw** response (and the reverse). **`isWrapperFor`** exists so async **outbound** filters can tell whether **their** wrapper is still in the chain.

> [!tip] Interview answer
> The servlet API gives four wrapper classes: ServletRequestWrapper and ServletResponseWrapper, plus HttpServletRequestWrapper and HttpServletResponseWrapper. They implement the decorator pattern and forward every call unless I override. I subclass the HTTP ones in a filter to change parameters or the body, and I pass that wrapper to doFilter or RequestDispatcher.
