<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

In the Front Controller pattern, all requests first go to one controller instead of many servlets. That controller chooses the handler, then decides which view to render, and sends the response.

Spring MVC’s `DispatcherServlet` is that front controller. Dumps usually register one servlet mapped to `/` so every HTTP request passes through it.

You can still declare more than one `DispatcherServlet` (for example `/api` vs `/`) — each loads its own child `WebApplicationContext`.

> [!warning] Unverified traps from the dump
> - Having several DispatcherServlets is allowed; each has its own servlet-level context.
> - Root beans are shared; servlet contexts cannot be seen from the root.
