<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`HandlerAdapter` invokes the handler `HandlerMapping` selected. Different handler types need different adapters.

For annotated controllers it is `RequestMappingHandlerAdapter`: it resolves method arguments (`@PathVariable`, `@RequestBody`, …), calls the method, and turns the return value into a `ModelAndView` or a written response.

`DispatcherServlet` looks up an adapter that `supports` the handler, then calls `handle`.

> [!warning] Unverified traps from the dump
> - HandlerMapping finds the method; HandlerAdapter actually runs it. Interviewers often mix the two.
