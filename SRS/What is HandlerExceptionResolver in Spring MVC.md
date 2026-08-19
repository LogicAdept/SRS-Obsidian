<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`HandlerExceptionResolver` handles exceptions thrown while executing a handler.

Dumps: `DispatcherServlet` registers `DefaultHandlerExceptionResolver` (older package `mvc.support`) which maps standard Spring MVC exceptions to HTTP status codes.

You can implement the interface (`resolveException` → `ModelAndView`) and register it on `WebMvcConfigurer.configureHandlerExceptionResolvers`, or rely on `@ExceptionHandler` / `@ControllerAdvice`.

> [!warning] Unverified traps from the dump
> - DefaultHandlerExceptionResolver is not the only resolver Boot registers (also ExceptionHandlerExceptionResolver, ResponseStatusExceptionResolver, …).
