<!--
reps: 0
priority: 0
-->
#Java/Servlet/Context #SRS

# What are servlet attributes for and how do they work?

> [!abstract] Short answer
> **Attributes are named `Object`s the container or the application binds** on a **request**, **session**, or **`ServletContext`**. They carry **server-side state** that **HTTP parameters cannot**: objects, not only strings; **not** copied from the client query string. **Request** attributes last for **one request** (and **`RequestDispatcher` forward/include**). **Session** attributes last for that **`HttpSession`** in this **web app**. **Context** attributes are **application-wide** in **this JVM**. Request API: [[How would you explain the ServletRequest interface]]. Sessions: [[How would you explain HTTP sessions in servlet based applications]]. Context: [[How would you explain ServletContext in Java web applications]]. JSP EL maps: [[What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects]].

## Three maps, one name-per-key rule

Jakarta Servlet **6.1**:

| Where | API | Who sees it | Typical use |
| --- | --- | --- | --- |
| **Request** | `ServletRequest.getAttribute` / `setAttribute` / `removeAttribute` | This request, including a **dispatcher** target | Controller → view; container extras (`jakarta.servlet.request.X509Certificate`, include/forward/error attrs) |
| **Session** | `HttpSession` same names | Any servlet in the **same `ServletContext`** on the **same session** | Login identity, cart |
| **Context** | `ServletContext` same names | Any servlet in the **same web application** | App-wide cache, shared config objects |

**One value per name.** Names starting with **`jakarta.`** are **reserved**. Application names should look like reverse-domain keys. Request **`setAttribute(name, null)`** is **`removeAttribute(name)`**. Request attributes are **reset between requests**.

**Request attributes** exist so the container can expose facts **outside** the rest of the API, and so a servlet can **hand objects to another servlet** via **`RequestDispatcher`**. Dispatch: [[How would you explain the servlet RequestDispatcher for forward and include]]. Error pages read **error** request attributes: [[How would you explain error context attributes in servlet error handling]].

**Session bind:** objects implementing **`HttpSessionBindingListener`** get **`valueBound`** before they are visible in **`getAttribute`**, and **`valueUnbound`** after they are not. Listeners **`ServletRequestAttributeListener`**, **`HttpSessionAttributeListener`**, **`ServletContextAttributeListener`** see add/replace/remove. The container **need not** serialize those notifications when context/session attributes change **concurrently**.

**Threading (session):** the container keeps the **attribute map** structurally thread-safe. **You** must make the **objects inside** thread-safe if two requests share them. **Distributed apps:** context attributes are **local to the JVM** (not a cluster store). Session values that must migrate should be **`Serializable`**; otherwise the container may throw **`IllegalArgumentException`**.

```d2
direction: down
req: "ServletRequest\nthis request (+ dispatch)" {
  width: 240
  height: 48
  style.fill: "#e3f2fd"
}
ses: "HttpSession\nsame app + same session" {
  width: 240
  height: 48
  style.fill: "#fff8e1"
}
ctx: "ServletContext\nwhole web app, this JVM" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
req -> ses: "shorter → longer lifetime" {
  style.stroke-dash: 3
}
ses -> ctx: " " {
  style.stroke-dash: 3
}
```

**Fig. 1.** Same **`getAttribute` / `setAttribute` names**, three **lifetimes**. Not **init parameters** and not **HTTP headers**.

```java
// Conceptual — Jakarta Servlet 6.1
request.setAttribute("com.example.order", order); // Object, this request
request.getRequestDispatcher("/view.jsp").forward(request, response);

request.getSession().setAttribute("com.example.user", user);     // until invalidate / timeout
getServletContext().setAttribute("com.example.cache", cache);    // all servlets, this JVM
```

**Listing 1.** Bind an **object** for a **forward**; session and context use the **same method names** with **longer** scope.

> [!warning] Attributes are not parameters
> **`getParameter`** is **client** data (`String` / `String[]`). **`getAttribute`** is **server** objects. They do not alias. Putting a **mutable** object in **session** or **context** and mutating it from **`service`** without your own locking races: the container protects the **map**, not your bean.

> [!warning] Context attributes are not cluster memory
> In a **distributable** app, **`ServletContext` attributes stay on the JVM that set them**. Sharing across nodes needs **session** (with **`Serializable`** values), a **database**, or an **EJB**. Do not store into names under **`jakarta.`**. Cross-context **dispatch** may **not** retrieve the same request attribute object in the **caller**.

> [!tip] Interview answer
> Servlet attributes are named objects on the request, the HttpSession, or the ServletContext. I use request attributes to pass a model into a forwarded JSP; session for per-user state; context for app-wide objects in this JVM. They are not request parameters, jakarta-dot names are reserved, and I treat values in session or context as shared mutable state I must make thread-safe myself.
