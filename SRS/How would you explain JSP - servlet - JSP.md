<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# How would you explain JSP - servlet - JSP?

> [!abstract] Short answer
> A **form JSP** posts to a **servlet**; that servlet does the work, **`setAttribute`s** on the **same request**, then **`RequestDispatcher.forward`** to a **result JSP** that renders with **EL** or **`<jsp:useBean>`**. Interview shorthand calls this **MVC** (JSP = view, servlet = controller, Java types = model). The **API** is still **forward + request attributes**, not a type named MVC. Mechanics: [[How does JSP servlet JSP interaction work]]. Dispatcher: [[How can one servlet call or forward to another servlet]]. Beans: [[How do you populate a JavaBean or object attributes from a request]]. Redirect is a different request: [[How does sendRedirect differ from forward in servlets]].

## View, controller, then view again — one request at the end

**First JSP.** Markup and a form whose **`action`** is the servlet’s URL. That hop is **HTTP** (new request, **parameters**). Keep this page thin: collect input, do not own the business rules.

**Servlet (controller).** `doGet` / `doPost` reads `getParameter`, talks to ordinary Java objects (the **model**), then `request.setAttribute("…", value)`. It does **not** write the HTML. `forward` to a JSP, often under **`WEB-INF`** so the browser cannot open the view by URL.

**Second JSP (view).** Same request: EL `${…}` sees those attributes. `jsp:useBean` / `jsp:getProperty` still need the bean **introduced** on this page. This JSP is itself a servlet (`_jspService`); the container **dispatches** to it.

**Why two JSPs.** The inbound page is the **form**; the outbound page is the **result**. They can be the same file if you forward back to it, but the **servlet still sits in the middle**. `<jsp:forward>` from a JSP to a servlet is the **server-side** equivalent of “go run the controller.”

**Not this pattern:** `sendRedirect` (new request, attributes gone), calling `service` on `new OtherServlet()`, or stuffing business logic into scriptlets so there is no servlet in the middle.

```d2
direction: down
v1: "JSP form\naction=servlet" {
  width: 200
  height: 48
  style.fill: "#fff8e1"
}
c: "HttpServlet\nparameters → model → setAttribute" {
  width: 280
  height: 48
  style.fill: "#e3f2fd"
}
v2: "JSP view\nEL / useBean" {
  width: 200
  height: 48
  style.fill: "#e8f5e9"
}
v1 -> c
c -> v2
```

**Fig. 1.** HTTP into the servlet; **forward** into the view.

```java
// Conceptual — jakarta.servlet.http, Servlet 6.1
req.setAttribute("order", order);
req.getRequestDispatcher("/WEB-INF/views/order.jsp").forward(req, resp);
```

**Listing 1.** Controller ends at `forward`. The JSP reads `order` on this request.

> [!warning] MVC is the nickname, not an interface
> The Servlet and Pages specs do **not** define Model/View/Controller types. They define **`RequestDispatcher`**, **request attributes**, and JSP actions. Faces (and Spring MVC) are **other** controller stacks on the same container.

> [!warning] Redirect breaks the hand-off
> After `sendRedirect`, the result JSP does **not** see those attributes. Commit the response before `forward` and you get **`IllegalStateException`**. Put views under **`WEB-INF`** and reach them only by dispatch.

> [!tip] Interview answer
> JSP-servlet-JSP means a form page posts to a servlet, the servlet runs the model and forwards to a JSP that draws the result. That is the usual MVC story on the Servlet API: JSPs are views, the servlet is the controller. I forward so the view shares the request; I do not redirect if the view needs those attributes.
