<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`DispatcherServlet` is the Front Controller: it maps HTTP requests to handlers, runs interceptors, and resolves views or writes the body.

`ContextLoaderListener` starts and shuts down the **root** `WebApplicationContext` and ties that context’s lifecycle to the `ServletContext`. Shared beans (services, repositories) live there.

Each `DispatcherServlet` creates a **child** context (controllers, `HandlerMapping`, `ViewResolver`, …). Children can see root beans; the root cannot see child beans.

> [!warning] Unverified traps from the dump
> - Boot often collapses this into one context; classic war + web.xml apps still show two contexts.
> - Root context is stored on the ServletContext under WebApplicationContext.class.getName() + ".ROOT".
