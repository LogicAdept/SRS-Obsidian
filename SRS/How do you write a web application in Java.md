<!--
reps: 0
priority: 0
-->
#Java/Servlet #SRS

# How do you write a web application in Java?

> [!abstract] Short answer
> A Java web app is a **collection of servlets, pages, classes, and static files** that the container mounts at one **context path** (one **`ServletContext`**). You **write web components** (typically **`HttpServlet`**), **map** them with **`@WebServlet`** or `web.xml`, **package** the tree as a directory or **WAR**, and **deploy** it to a **servlet container**. The client URL is `host:port` + **context path** + **url-pattern**. `web.xml` is **optional** when you use annotations (or ship only static files / JSP). Servlet: [[What is a servlet]]. Context: [[How would you explain ServletContext in Java web applications]]. Descriptor: [[How would you explain the Java EE web deployment descriptor]]. Request path: [[How is an HttpServlet request processed]].

## Assemble a web application, then deploy it

This is **not** `public static void main`. The container accepts HTTP, builds `HttpServletRequest` / `HttpServletResponse`, and calls your component. Jakarta Faces, Jakarta REST, and similar stacks still run as **web components on a servlet container**.

**1. Write a component.** Extend `HttpServlet` and override `doGet` / `doPost` / … Map the servlet with `@WebServlet("/greeting")` or a `<servlet>` plus `<servlet-mapping>` in `WEB-INF/web.xml`. If the same setting appears in both, the **descriptor wins**.

**2. Lay out the application.** The **document root** holds public files (`index.html`, images). **`WEB-INF`** holds what clients must not fetch: `web.xml`, `classes/` (servlets and utilities), `lib/*.jar`. The app class loader uses **`WEB-INF/classes` first**, then JARs in `lib`. A **WAR** is that tree zipped (plus `META-INF` for the archive tool). You may also run it **unpacked**.

**3. Deploy and hit a URL.** Copy the WAR (or exploded tree) into the container’s deploy location. Default **context path** is often the WAR base name. Then request **host + port + context path + url-pattern**. No servlet on `/` → **404** until you map one or a welcome file.

A `web.xml` is **not required** if there are **no** servlet/filter/listener components, or those components are declared with **annotations**. `metadata-complete="true"` means the container **ignores** `@WebServlet` / `@WebFilter` / `@WebListener` and `web-fragment.xml`.

```d2
direction: down
client: "HTTP request" {
  width: 180
  height: 36
  style.fill: "#fff8e1"
}
url: "context path + url-pattern" {
  width: 240
  height: 36
  style.fill: "#e3f2fd"
}
war: "WAR / directory\nWEB-INF/classes + lib" {
  width: 240
  height: 48
  style.fill: "#e3f2fd"
}
svc: "HttpServlet.doGet / doPost" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
client -> url
url -> war
war -> svc
```

**Fig. 1.** The unit of deployment is the web application, not a standalone class.

```
/index.html
/WEB-INF/web.xml
/WEB-INF/classes/com/example/Greeting.class
/WEB-INF/lib/helper.jar
```

**Listing 1.** Spec layout: public files at the root; code and descriptor under `WEB-INF`.

```java
// Conceptual — jakarta.servlet.annotation, Servlet 6.1
@WebServlet("/greeting")
public class Greeting extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws IOException {
        String name = req.getParameter("name");
        if (name == null || name.isBlank()) {
            resp.sendError(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }
        resp.setContentType("text/plain;charset=UTF-8");
        resp.getWriter().write("Hello, " + name + "!");
    }
}
```

**Listing 2.** Map in the class; package it under `WEB-INF/classes` and deploy the WAR. Call `/context-path/greeting?name=Duke`.

> [!warning] `WEB-INF` and `META-INF` are not public URLs
> A client request for those directories must get **404**. Servlet code can still read them with `ServletContext.getResource*`. Duplicate **context paths** are rejected. Case-sensitive matching: `/WEB-INF` and `/web-inf` must not leak the directory.

> [!warning] Annotation mapping is skipped when the descriptor is complete
> `@WebServlet` is processed only for classes in **`WEB-INF/classes`** or JARs in **`WEB-INF/lib`**. `metadata-complete="true"` ignores those annotations. Frameworks (Spring MVC, Faces, REST) still **package this same WAR**; they do not replace the servlet web application model.

> [!tip] Interview answer
> I write HttpServlet classes, map them with WebServlet or web.xml, and put classes and JARs under WEB-INF in a directory or WAR. The container deploys that unit at a context path and calls the servlet for host plus context path plus url-pattern. web.xml is optional when annotations declare the components, and WEB-INF is never served to the browser.
