<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`WebApplicationInitializer` configures the `ServletContext` in Java and replaces `web.xml`.

Dump `onStartup`: create `AnnotationConfigWebApplicationContext`, register MVC config, `addServlet("dispatcher", new DispatcherServlet(context))`, `setLoadOnStartup(1)`, `addMapping("/")`.

`AbstractAnnotationConfigDispatcherServletInitializer` is the usual subclass that splits root vs servlet config classes.

> [!warning] Unverified traps from the dump
> - Servlet 3+ container required; Boot uses a different embedded-container path.
