<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`BindingResult` (in `org.springframework.validation`) holds data-binding and validation errors for a command/form object.

Declare it **immediately after** the `@Valid` / `@Validated` argument. Then `result.hasErrors()` and return the form view.

When Spring sees `@Valid`, it finds a validator, runs constraint annotations, and puts errors on `BindingResult`, which is also added to the model for `<form:errors/>`.

> [!warning] Unverified traps from the dump
> - If BindingResult is not the next parameter after the validated object, Spring throws an exception instead of giving you the result.
> - Optional Model must come after BindingResult.
