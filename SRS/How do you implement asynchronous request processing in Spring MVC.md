<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Return `Callable<T>` or `DeferredResult<T>` (dumps also mention `SseEmitter` for SSE) so the container thread is not blocked for the whole job.

`Callable`: Spring runs the task on a task executor and writes the result when it completes.

`DeferredResult`: you complete it later from another thread (`setResult`).

> [!warning] Unverified traps from the dump
> - Need async supported on the servlet (Servlet 3) and MVC async config; Boot usually enables it.
> - This is servlet async, not WebFlux.
