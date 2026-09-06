<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/CGI #SRS

# What are the advantages of servlets over CGI?

> [!abstract] Short answer
> Jakarta Servlet **6.1 §1.4** lists four: **(1)** servlets are **generally much faster** than CGI because they use a **different process model**; **(2)** a **standard API** many servers implement; **(3)** **Java** (easier development, **platform independence**); **(4)** the rest of the **Java platform APIs**. CGI **executes a script per request** (program + **meta-variables**, response on **stdout**). A servlet is **loaded once**, **`init` once**, then **`service` on container threads**. Speed is **not** “cheaper than `new`.” What a servlet is: [[What is a servlet]]. Who runs it: [[What typical responsibilities does a servlet container have]]. Threads: [[How do servlets work in a multithreaded environment]]. Request path: [[How is an HttpServlet request processed]]. Packaging: [[How do you write a web application in Java]].

## CGI executes; the servlet instance stays

**CGI/1.1:** the HTTP server maps the URI, **converts** the client request to a CGI request, **executes** the script (normally as an **executable program**), and maps the script’s output back to HTTP. Input is **meta-variables** (often the process environment) plus a message body; output is **standard output** unless the platform defines another channel. Each execution is **independent** (Web is stateless). The server **may kill** the script process on error or timeout.

**Servlet:** the container **loads** the class, **`new`s** one instance per declaration (non-distributed), calls **`init`**, then **`service`** **0..n** times, often **concurrently**. Typed **`ServletRequest` / `ServletResponse`** objects replace env-vars and stdout. That is the **process-model** win: **no new OS process per hit**, **JVM and instance reused**, **init** cost paid once. Lifecycle: [[How does a servlet container manage the servlet lifecycle]].

Servlets sit **above CGI** and **below** frameworks such as **Jakarta Faces**. They are **portable server extensions**, not Netscape NSAPI / Apache modules (older specs placed them in that gap).

| CGI | Servlet |
| --- | --- |
| Execute script **per request** | **Reuse** instance; **`service` on threads** |
| Meta-variables + **stdout** | **Request / response objects**, standard **Jakarta Servlet API** |
| Language of the executable | **Java** + **platform APIs**, write once / run on any servlet container |
| Isolation by **process** | Shared instance → **you** handle concurrency |

```d2
direction: right
cgi: "CGI\nexecute program\nmeta-vars → stdout" {
  width: 200
  height: 56
  style.fill: "#fff3e0"
}
srv: "Servlet\ninit once\nservice on threads" {
  width: 200
  height: 56
  style.fill: "#e8f5e9"
}
cgi -> srv: "spec: generally faster\ndifferent process model"
```

**Fig. 1.** Spec advantage **(1)** is the **process model**. **(2)–(4)** are **API**, **Java**, and **Java libraries**.

```java
// Conceptual — Jakarta Servlet 6.1 vs CGI/1.1
// CGI: server executes the program again; QUERY_STRING in the environment; write HTTP to stdout.
public class HelloServlet extends HttpServlet {
    @Override
    public void init() { /* once per instance, not per request */ }

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws IOException {
        resp.setContentType("text/plain");
        resp.getWriter().write("hello"); // typed response, not stdout
    }
}
```

**Listing 1.** Same work as a CGI GET, without **re-executing** a process. **`init`** is **not** CGI’s per-request start.

> [!warning] Faster is “generally”, and isolation is gone
> CGI/1.1 invocation is **system-defined**; some servers **link** a script in-process. FastCGI-style daemons also keep a process warm. Do **not** claim every CGI fork. The servlet **instance is shared**: concurrent **`service`** is **required** to be thread-safe. Process isolation is **not** a servlet feature.

> [!warning] Servlets are not a high-level UI framework
> The spec places them **below** Jakarta Faces. A raw servlet still owns **headers, body, threads, and sessions**. Portability is **the Servlet API**, not “any JVM program dropped in `cgi-bin`”.

> [!tip] Interview answer
> Servlets beat classic CGI mainly on process model: the container keeps the servlet, runs init once, and handles requests on threads instead of executing a program per hit. You also get a standard API many servers share, plus Java and its libraries. The trade-off is that I must write the servlet for concurrent service, which CGI process isolation used to give me for free.
