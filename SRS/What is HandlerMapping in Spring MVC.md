<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`HandlerMapping` maps an incoming request to a handler (usually a `@RequestMapping` method) using URL, HTTP method, and other request state.

It returns a `HandlerExecutionChain`: the handler plus interceptors.

Dumps still name older mappings (`BeanNameUrlHandlerMapping`, `SimpleUrlHandlerMapping`). Annotation apps use `RequestMappingHandlerMapping` (older lists say `DefaultAnnotationHandlerMapping`).

> [!warning] Unverified traps from the dump
> - DefaultAnnotationHandlerMapping is a Spring 3-era name; current annotation mapping is RequestMappingHandlerMapping.
> - DispatcherServlet already uses HandlerMapping; you rarely call getHandler yourself.
