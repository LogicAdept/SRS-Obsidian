<!--
reps: 0
priority: 0
-->
#Java/Servlet #Networking/Web/Protocols/HTTP #SRS

# How does sendRedirect differ from forward in servlets?

> [!abstract] Short answer
> **`RequestDispatcher.forward`** is **server-side**: the **same** request/response is handed to another resource in this web app; the **browser URL does not change**; **request attributes survive**. **`HttpServletResponse.sendRedirect`** is **client-side**: the container **commits** a redirect (**default `SC_FOUND` 302**, `Location` header), the browser **issues a new request**, and **request attributes are gone**. Forward cannot leave this application’s dispatcher paths; redirect **may be any URL**. Dispatcher: [[How can one servlet call or forward to another servlet]]. API: [[How would you explain the servlet RequestDispatcher for forward and include]]. Views: [[How does JSP servlet JSP interaction work]].

## Same request versus a second request

**Forward.** Call only while the response is **uncommitted**. Uncommitted buffer **is cleared**, then the **target** `service`s and **finishes** the response (container commits/closes unless async). Path getters on the target match the dispatcher path (not for `getNamedDispatcher`). Original path is in `jakarta.servlet.forward.*`. Same **thread / JVM**. Query string on the dispatcher path is **merged** for that dispatch.

**Redirect.** `sendRedirect(location)` sets **302** and a **`Location`**, **clears** the buffer (replaced by a short hypertext note), **commits**, and **closes** the response. Nothing you write afterward is sent. Relative locations are **turned into absolute URLs** unless the container is configured to pass them through. Unconvertible location → **`IllegalArgumentException`**. Servlet 6.1 also has `sendRedirect(location, sc)` / `clearBuffer` if you need **303** (`SC_SEE_OTHER`) or to keep the buffer. Pass the URL through **`encodeRedirectURL`** when session tracking may use rewriting.

**What the client sees.** Forward: address bar still shows the **first** URL. Redirect: the client **follows `Location`**. That second request has **new** parameters (only what you put on the redirect URL), **new** attributes, **same session cookie** if one exists.

**Where you can go.** Forward (and include) stay inside **this** `ServletContext` path space — including **`WEB-INF`** JSPs the browser cannot request. Redirect can be **another host**. A redirect to `/WEB-INF/…` is a **client** GET of a hidden tree → **404**.

```d2
direction: down
req: "client request" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
fw: "forward\nsame request, hidden URL" {
  width: 240
  height: 48
  style.fill: "#e8f5e9"
}
rd: "sendRedirect 302\nLocation + new client request" {
  width: 280
  height: 48
  style.fill: "#e3f2fd"
}
req -> fw
req -> rd
```

**Fig. 1.** Forward never round-trips the browser. Redirect always does.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
req.setAttribute("msg", "ok");
req.getRequestDispatcher("/WEB-INF/views/ok.jsp").forward(req, resp);
// vs
resp.sendRedirect(resp.encodeRedirectURL(req.getContextPath() + "/ok"));
// attribute "msg" is not on the follow-up GET
```

**Listing 1.** Use forward to render with request data. Use redirect when the client must **change URL** (PRG after POST: prefer **303**).

> [!warning] Both throw if the response is committed
> Uncommitted leftover bytes: **forward** discards them then the target writes; **`sendRedirect`** discards them and sends the redirect body. After commit, both throw **`IllegalStateException`**. **`sendRedirect` from an include is ignored.** Do not write the body after either call.

> [!warning] 302 is not “always GET”
> The no-arg `sendRedirect` is **302 Found**. Whether the next request repeats **POST** is **user-agent defined**. For “always GET the `Location`,” pass **`SC_SEE_OTHER` (303)**. Do not use redirect to pass request-scoped model data.

> [!tip] Interview answer
> Forward keeps the same request and response inside the container, so attributes and the original URL stay, and the target finishes the body. sendRedirect commits a 302 with Location, the browser calls again, and those attributes are gone. I forward to a WEB-INF JSP to render; I redirect when the address bar must change, using 303 after a POST if I need a GET.
