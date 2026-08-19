<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A `HandlerInterceptor` runs around the handler:

- `preHandle` — after mapping, before the adapter invokes the controller. Return `false` to abort (write your own response).
- `postHandle` — after the handler, before view rendering. Can add model attributes.
- `afterCompletion` — after the view (or after the request finishes). Runs only if this interceptor’s `preHandle` returned `true`. Reverse order vs `preHandle`.

Use for logging, shared model attributes, timing — not as a security layer (dumps still mention auth).

> [!warning] Unverified traps from the dump
> - For @ResponseBody / ResponseEntity, the body is often committed inside the HandlerAdapter, so postHandle is too late to change the response; use ResponseBodyAdvice.
> - HandlerInterceptorAdapter is a convenience base class; dumps still recommend it, but it was deprecated.
> - Filters wrap the servlet; interceptors only see requests that reached a HandlerMapping (typically controllers, not static files).
