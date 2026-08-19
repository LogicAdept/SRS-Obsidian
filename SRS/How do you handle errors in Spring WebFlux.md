<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`onErrorReturn` for a static default; `onErrorResume` for a dynamic fallback, alternate path, or wrap-and-rethrow; plus a global error response customization. Also `onErrorMap`. Pipeline dumps add `retry(n)`.

`onErrorResume` on the chain, and app-wide `@ControllerAdvice` with `@ExceptionHandler` that returns reactive types.

You cannot rely on try/catch because execution is deferred. `doOnError` is side effects only and does **not** recover.

> [!warning] Unverified traps from the dump
> - `doOnError` vs `onErrorResume` is the popular lie that dump flags.
> - Global `@ControllerAdvice` returning `Mono` is WebFlux-shaped; MVC `ResponseEntityExceptionHandler` examples in other dumps are not the same stack.

