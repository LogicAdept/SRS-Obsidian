<!--
reps: 0
priority: 0
-->
#Java/Servlet #Java/JDBC #Java/Logging #SRS

# How do you connect to a database and add logging in a servlet?

> [!abstract] Short answer
> Inject a **`javax.sql.DataSource`** into the servlet (`@Resource` or a JNDI lookup). On each request call **`getConnection()`**, run JDBC, then **close** the `Connection` (try-with-resources). Log with **`GenericServlet.log(String)`** / **`log(String, Throwable)`** — they write to the **container** log and **prepend the servlet name**. Do **not** store a live `Connection` in a servlet field: `HttpServlet` is invoked concurrently and lists **database connections** among shared resources you must not race.

## DataSource in the servlet, `Connection` on the request

`DataSource` is a **factory** for connections and the JDBC **preferred** alternative to `DriverManager`. Implementations are typically registered in **JNDI**. Jakarta EE resource injection can put that factory on a container-managed servlet:

```java
@Resource(name = "java:comp/DefaultDataSource")
private javax.sql.DataSource dsc;
```

**Listing 1.** Conceptual `@Resource` field on an `HttpServlet`. A setter annotated `@Resource` is equally valid. The annotation lives in `jakarta.annotation` and resolves **by name**, not by type.

Keep the **`DataSource`** (thread-safe factory) as the instance field. Call **`getConnection()`** inside `doGet` / `doPost`, then close it ([[How do you close a database connection properly]], [[How do you establish a database connection in Java]]). A pooling `DataSource` still requires that `close()`; the pool reuses the physical connection ([[What are database connection pools for]]).

`Servlet.init` runs **once** before any `service` call, so looking up the `DataSource` there is fine. Holding the **`Connection`** from `init` until `destroy` is not: the container may run **`service` on multiple threads** at once, and `HttpServlet` names **database connections** as shared resources that need synchronization — or, better, no sharing ([[How do servlets work in a multithreaded environment]]).

```d2
direction: right
ds: "DataSource field\n@Resource / JNDI" {
  width: 240
  height: 80
  style.fill: "#fff3e0"
}
req: "doGet / doPost\ngetConnection()" {
  width: 230
  height: 80
  style.fill: "#e3f2fd"
}
log: "log(msg) or log(msg, t)\nthen close Connection" {
  width: 260
  height: 80
  style.fill: "#e8f5e9"
}

ds -> req -> log
```

**Fig. 1.** Share the factory, not the connection. Log through the servlet API, then release JDBC objects.

## Servlet logging vs JDBC tracing

`HttpServlet` extends `GenericServlet`. `GenericServlet.log(String)` writes to a **servlet log file, prepended by the servlet’s name**, by calling `ServletContext.log(String)`. The overload with a `Throwable` also writes a **stack trace**. The **name and type of that file are container-specific** (often the server event log). That is the Servlet API’s logging hook — not `System.out`.

`DataSource.getLogWriter` / `setLogWriter` is a **JDBC** character stream for driver tracing. It starts **null** (logging disabled) and does **not** go to `ServletContext.log`. Do not confuse driver tracing with servlet logs.

```java
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

import javax.sql.DataSource;

import jakarta.annotation.Resource;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

public class PersonNameServlet extends HttpServlet {
    @Resource(name = "java:comp/env/jdbc/appDb")
    private DataSource dataSource;

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp)
            throws ServletException, IOException {
        String idParam = req.getParameter("id");
        try (Connection con = dataSource.getConnection();
             PreparedStatement ps = con.prepareStatement(
                     "SELECT name FROM person WHERE id = ?")) {
            ps.setInt(1, Integer.parseInt(idParam));
            try (ResultSet rs = ps.executeQuery()) {
                if (!rs.next()) {
                    log("no person for id=" + idParam);
                    resp.sendError(HttpServletResponse.SC_NOT_FOUND);
                    return;
                }
                log("loaded person id=" + idParam);
                resp.setContentType("text/plain;charset=UTF-8");
                resp.getWriter().write(rs.getString(1));
            }
        } catch (SQLException e) {
            log("query failed for id=" + idParam, e);
            throw new ServletException(e);
        }
    }
}
```

**Listing 2.** Per-request `getConnection`, `PreparedStatement`, try-with-resources, `log` on success and `log(message, t)` on `SQLException`. `init` can stay for other one-time setup ([[What are the three core Servlet lifecycle methods and their roles]]).

> [!warning] Do not keep a `Connection` on the servlet instance
> Concurrent `doGet` threads would share it. `HttpServlet` lists **database connections** next to files and instance variables as shared resources. Checkout from `DataSource` **per request** and `close()` in that request.

> [!warning] `log()` is not `DataSource.setLogWriter`
> Servlet `log` goes to a **container-chosen** file and prepends the servlet name. JDBC’s log writer is driver tracing on a `PrintWriter`, default **off**. Using `DriverManager.getConnection` inside `doGet` also skips the container `DataSource` (pooling, JNDI config).

> [!warning] `@Resource` is name-based
> A wrong JNDI name or type mismatch shows up at **runtime**. Names such as `java:comp/DefaultDataSource` are **product defaults**, not a `DataSource` every servlet container invents for you.

> [!tip] Interview answer
> In a servlet, inject or look up a `DataSource`, then `getConnection()` on each request and close it with try-with-resources. Log with `log(message)` or `log(message, throwable)` so the container log includes the servlet name and stack traces. Never store the `Connection` in a field — the servlet handles concurrent requests.

## See also

- [[How do JDBC interface types such as Statement and PreparedStatement differ]]
- [[How would you explain ServletContext in Java web applications]]
- [[Why override the no argument init method in a servlet]]
