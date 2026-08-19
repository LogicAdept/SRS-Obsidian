<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@ResponseStatus` puts an HTTP status (and optional reason) on a handler method or on an exception class.

Dump pattern: annotate a custom exception so an uncaught throw becomes that status via `HandlerExceptionResolver`, without writing an `@ExceptionHandler`.

```java
@ResponseStatus(HttpStatus.NOT_FOUND)
public class ResourceNotFoundException extends RuntimeException { ... }
```

> [!warning] Unverified traps from the dump
> - If you also catch that exception in @ExceptionHandler, the @ResponseStatus-on-exception path may not run.
> - reason is not always sent to the client (container/version dependent).
