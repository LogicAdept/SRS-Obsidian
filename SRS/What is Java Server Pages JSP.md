<!--
reps: 0
priority: 0
-->
#Java/JSP #Java/Servlet #SRS

# What is Java Server Pages JSP?

> [!abstract] Short answer
> **Jakarta Server Pages (JSP)** is the Jakarta EE **text-page** technology for **dynamic web content** (HTML, XHTML, XML, …). A **JSP page** describes how to turn a **request** into a **response** by mixing **template text** with **directives, actions, EL, and (optionally) scripting**. The container **translates** it to a **servlet** (`jakarta.servlet.Servlet`) and then **runs** that class. HTTP is the default protocol (`HttpServletRequest` / `HttpServletResponse`). What a servlet is: [[What is a servlet]]. Why JSP vs raw servlets: [[Why do you need JSP]]. EL maps: [[What are the implicit EL scope objects in JSP and how do they differ from servlet scoped objects]]. Session on the page: [[Is a session object always created on a JSP page and can it be disabled]].

## Text page → servlet implementation class

Jakarta Pages **4.0 §1.1**: the page defines a **JSP page implementation class**. At request time the **JSP container** (same as **web container**) delivers the request to **that object**. **Web component** = **servlet or JSP**; both are described with the **`servlet`** element in `web.xml`. Default mapping: **`.jsp`** (XML documents **`.jspx`**).

**Two phases.** **Translation** (once per page, any time from deploy to first request): validate syntax, produce the servlet class. **Request** (once per hit): instantiate/use that class like any servlet (`jspInit` / `_jspService` / `jspDestroy` align with servlet `init` / `service` / `destroy`). Translation can also be **ahead of time** so the first client is not paying compile cost.

**Authoring pieces:** template data; standard **directives** and **actions**; **tag libraries**; **EL**; scripting (page authors are expected to **avoid** scriptlets and **need not know Java**; **`scripting-invalid`** makes leftover `<%` a **translation error**). JSP inherits **web apps, `ServletContext`, sessions, request/response** from the servlet spec. A servlet can **forward/include** a JSP: [[How would you explain the servlet RequestDispatcher for forward and include]]. MVC hop: [[How does JSP servlet JSP interaction work]]. Page-author style: [[What are practical guidelines for working with JSP]].

```d2
direction: down
src: "*.jsp text\ntemplate + actions + EL" {
  width: 240
  height: 48
  style.fill: "#fff8e1"
}
impl: "JSP implementation class\nimplements Servlet" {
  width: 260
  height: 48
  style.fill: "#e8f5e9"
}
req: "request phase\nHttpServletRequest → response" {
  width: 280
  height: 48
}
src -> impl: "translation (once)"
impl -> req: "per request"
```

**Fig. 1.** JSP is **not** a second HTTP engine. It **is** a servlet after translation.

```jsp
<%-- Conceptual — Jakarta Pages 4.0 --%>
<%@ page contentType="text/html;charset=UTF-8" %>
<p>Hello ${param.name}</p>
```

**Listing 1.** Template plus **EL**. The container turns this into an **`HttpServlet`**. Scriptlets are optional and discouraged for page authors.

> [!warning] Jasper is not “the JSP spec”
> **Jasper** is **Tomcat’s** compiler. Any compliant **JSP container** may translate. Do not treat **`.ear`** as required: a JSP lives in a **web application** (often a **WAR**). **`javax.servlet.jsp`** is the pre-Jakarta package.

> [!warning] First request can compile
> If the container translates **on demand**, the **first hit** pays **translation + compile**, and a bad page is **HTTP 500**, not a comment in the HTML. Precompile if that lag matters. A **`.jspf` segment** is not necessarily a legal top-level page. **`session="true"`** is the default on the generated servlet.

> [!tip] Interview answer
> JSP is a text document that mixes markup with JSP actions and EL. The container translates it into a servlet and then runs that class for each request. I use it as the view, not as a replacement for the servlet container, and I keep Java out of the page when I can.
