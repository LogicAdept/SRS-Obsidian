<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`ApplicationContext` is the general IoC container (stand-alone or web).

`WebApplicationContext` is the web specialization: associated with `DispatcherServlet`, has `ServletContext`, typically configured via `*-servlet.xml` or Java MVC config.

Dumps contrast: no servlet association vs associated with `DispatcherServlet`; desktop/console vs web/REST.

> [!warning] Unverified traps from the dump
> - In Boot the distinction is often hidden by auto-config; the types still exist.
