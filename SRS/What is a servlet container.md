<!--
reps: 0
priority: 0
-->
#Java/Servlet/Container #SRS

# What is a servlet container?

> [!abstract] Short answer
> The cue means **servlet container** (servlet **engine**): the **web-server or application-server component** that **hosts servlets**. It **provides the network I/O**, **decodes MIME requests**, **formats MIME responses**, and **manages each servlet’s lifecycle**. A servlet is a **class inside** that engine, not the engine itself. Jakarta Servlet **6.1** requires **HTTP/1.1 and HTTP/2** (and **HTTPS** support). What a servlet is: [[What is a servlet]]. What the engine does: [[What typical responsibilities does a servlet container have]]. Lifecycle: [[How does a servlet container manage the servlet lifecycle]]. Engine vs full Java EE server: [[Why use Java EE application servers when servlet containers exist]].

## The engine that owns sockets and `Servlet`

**§1.2:** the container is **part of** a **web server** or **application server**. It may be **built into** the HTTP server, an **add-on** via that server’s native API, or **built into / installed on** a Java EE **application server**.

It **does not** replace the servlet class. The container **loads** your **`HttpServlet`**, calls **`init` / `service` / `destroy`**, and hands **request/response** objects. Methods: [[What are the three core Servlet lifecycle methods and their roles]]. It **may cache** per HTTP caching rules and **may restrict** what the servlet is allowed to do. Sessions live **in the container**, scoped per web app: [[How would you explain HTTP sessions in servlet based applications]].

**§1.3 sequence:** browser → web server → **container** (same process, other process, or other host) → **mapped servlet** → flush response → back to the HTTP server.

```d2
direction: down
http: "HTTP server or Java EE server" {
  width: 260
  height: 40
}
eng: "servlet container / engine" {
  width: 240
  height: 40
  style.fill: "#fff8e1"
}
srv: "your HttpServlet instance" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
http -> eng: "hand off request"
eng -> srv: "service(req, res)"
```

**Fig. 1.** **Container servlet** in interview Russian is **контейнер сервлетов** = **this engine**, not a special servlet type.

```java
// Conceptual — Jakarta Servlet 6.1
// You write the component. The container (not this class) binds the port and calls service.
@WebServlet("/ping")
public class PingServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.getWriter().write("ok");
    }
}
```

**Listing 1.** A **servlet**. The **container** is Tomcat/Jetty/… or the servlet engine **inside** WildFly/GlassFish — **not** this class.

> [!warning] Application servers are not “a servlet container” as their whole product
> A **Java EE / Jakarta EE server** **contains** a servlet engine **plus** EJB, REST, JTA, and so on. Listing **WildFly** or **WebLogic** as *only* a servlet container mixes **engine** and **platform**. A **standalone** engine can still be a **full HTTP server**.

> [!warning] No container, no servlet
> **`java -cp app.jar PingServlet`** does not run a servlet. **`service` is called by the engine**, often **concurrently**. Do not confuse **servlet container** with **`ServletContext`** (the **application** object) or with **Kubernetes**.

> [!tip] Interview answer
> A servlet container is the engine that speaks HTTP, maps a URL to a servlet, and drives init, service, and destroy. My class is the component; the container is Tomcat, Jetty, or the servlet engine inside an application server. It is not a kind of servlet, and a full Java EE server is more than that engine.
