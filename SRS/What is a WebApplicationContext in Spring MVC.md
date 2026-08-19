<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`WebApplicationContext` extends `ApplicationContext` with web extras, including `getServletContext()`.

Each `DispatcherServlet` has its own `WebApplicationContext` that holds web beans: controllers, handler mappings, view resolvers.

The root web context (if `ContextLoaderListener` is used) holds shared infrastructure beans visible to every servlet context.

> [!warning] Unverified traps from the dump
> - WebApplicationContext is not the same as a plain ApplicationContext used in a console app — it carries ServletContext.
