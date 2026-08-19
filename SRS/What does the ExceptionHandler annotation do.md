<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@ExceptionHandler` marks a controller method that handles thrown exceptions. The exception types on the annotation should match the method argument.

Alone: only that controller. With `@ControllerAdvice`: global.

Handler methods may take servlet types (`HttpServletRequest`, …) but dumps say **not** `Model` as a parameter.

Same exception type: cannot define two handlers in one class (startup failure). In two classes, whichever is found first wins.

> [!warning] Unverified traps from the dump
> - Unhandled exceptions become HTTP 500 unless mapped.
> - @ResponseStatus on a custom exception is a different path (HandlerExceptionResolver) and should not also be caught elsewhere if you rely on it.
