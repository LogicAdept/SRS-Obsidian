<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@RequestBody` on a parameter: deserialize the HTTP request body (JSON/XML) to a Java object via `HttpMessageConverter`.

`@ResponseBody` on a handler (or return type): write the return value to the HTTP response body; do not treat it as a view name and skip `ViewResolver`.

`@RestController` = `@Controller` + `@ResponseBody` on every method.

> [!warning] Unverified traps from the dump
> - This is not the same comparison as @ResponseBody vs ResponseEntity (status/headers).
> - @RequestBody is typical for POST/PUT/PATCH JSON, not for classic form posts (@ModelAttribute).
