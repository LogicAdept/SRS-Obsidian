<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@RequestParam` binds a **query** (or form) parameter: `/users?id=101`.

`@PathVariable` binds a **URI template** segment: `/users/101` with mapping `/users/{id}`.

Dumps: `@RequestParam` optional by default (later Spring versions changed required defaults — treat as a claim); `@PathVariable` required by default. Use params for filters; path variables for resource ids.

> [!warning] Unverified traps from the dump
> - Whether @RequestParam is required by default depends on Spring version; do not memorize one dump’s table blindly.
> - A Map<String, String> can receive all path variables or all request params, depending on the annotation.
