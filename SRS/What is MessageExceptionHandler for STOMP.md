<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebSocket #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@MessageExceptionHandler` on a controller catches exceptions from message handling. Dump sends the string to `@SendTo("/topic/errors")`.

> [!warning] Unverified traps from the dump
> - Not `@ControllerAdvice` `@ExceptionHandler` for HTTP, though the name is similar.

