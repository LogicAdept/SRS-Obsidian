<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A `@InitBinder` method customizes binding for request parameters, URI variables, and command objects: register `PropertyEditor`s, formatters, and validators.

One argument must be `WebDataBinder`. Other arguments can be handler types except command objects and `BindingResult`.

If `value` is empty, the method runs for every request to that controller; if set, only for matching attribute/parameter names.

Typical dump example: default date format via `CustomDateEditor` on `Date.class`.

> [!warning] Unverified traps from the dump
> - InitBinder on a @ControllerAdvice can apply globally.
> - Do not put the form object itself as an InitBinder argument.
