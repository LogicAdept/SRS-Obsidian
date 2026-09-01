<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/OOP #Java/Language/Modifiers/Abstract #SRS

# Why is HttpServlet declared as an abstract class?

> [!abstract] Short answer
> It is a **template to subclass**, not a servlet you deploy as-is. `HttpServlet` implements HTTP **`service`** by dispatching to **`doGet` / `doPost` / `doPut` / `doDelete` / …**. Those `doXxx` methods already have **bodies**; the class is still **`abstract`** so you cannot construct it and so the API states you **must override at least one** method (usually a `doXxx`, or `init` / `destroy` / `getServletInfo`). Dispatch: [[How is an HttpServlet request processed]]. Methods: [[What are the main HttpServlet request handling methods]]. vs `GenericServlet`: [[What is the difference between GenericServlet and HttpServlet]].

## Incomplete as a website servlet

The Jakarta Servlet API gives two abstract classes that implement `Servlet`: `GenericServlet` and `HttpServlet`. For HTTP, you **extend `HttpServlet`**. The container still calls `init`, `service`, `destroy` on **your** class ([[How would you explain the servlet container lifecycle for servlets]]).

**`service` is already written.** The public `service(ServletRequest, ServletResponse)` forwards to the HTTP `service`, which picks `doGet`, `doPost`, and the other `doXxx` methods. There is almost no reason to override `service` ([[When must you override the service method in a Java servlet]]).

**`abstract` without forcing `abstract` methods.** An `abstract` class cannot be instantiated. That matches the constructor text: it does nothing **because this is an abstract class**. The `doXxx` defaults are not a useful site; the JavaDoc requires a subclass to override **at least one** method. `abstract` is the language way to say “this type is incomplete” even when every method has a default body ([[When should you use an abstract class versus an interface]]).

An interface would not hold this shared dispatch implementation. A concrete `HttpServlet` you could `new` would still not be what you map in `web.xml` / `@WebServlet`.

```d2
direction: down
svc: "HttpServlet.service" {
  width: 220
  height: 40
  style.fill: "#fff8e1"
}
do: "doGet / doPost / …" {
  width: 220
  height: 40
  style.fill: "#e3f2fd"
}
you: "your subclass override" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
svc -> do: "dispatch"
you -> do: "override at least one"
```

**Fig. 1.** The abstract class owns HTTP dispatch. Your class supplies the method you actually support.

```java
// Conceptual — jakarta.servlet.http
public abstract class HttpServlet extends GenericServlet {
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        /* default: not a useful GET handler */
    }

    protected void service(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        /* dispatch to doGet / doPost / … */
    }
}

class HelloServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {}
}
```

**Listing 1.** Conceptual. `HelloServlet` is the instantiable servlet. `new HttpServlet()` would not compile.

> [!warning] `abstract` here does not mean “has abstract methods”
> Interview traps claim `HttpServlet` is abstract **because** `doGet` is abstract. The `doXxx` methods are **concrete**. The class is abstract so the base type is not constructed and so you are told to override something.

> [!warning] Do not override `service` to “make it abstract-enough”
> Dispatch already lives in `HttpServlet`. Override `doGet` or `doPost`. Override `service` only for a non-HTTP or custom protocol case.

> [!warning] Constructor vs `init`
> The empty `HttpServlet()` is not servlet initialization. Use `init` / `ServletConfig` for container setup ([[Should you define a constructor for a servlet and how should you initialize it]]).

> [!tip] Interview answer
> HttpServlet is abstract because it is a base class to extend, not to deploy. It already implements HTTP service by calling doGet, doPost, and the other doXxx methods. Those methods have defaults; the class is still abstract so you cannot instantiate it and so you must override at least one method in a subclass. GenericServlet is the protocol-neutral abstract parent.
