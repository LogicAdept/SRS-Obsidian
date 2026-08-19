<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps state: a `@Controller` bean is a **singleton** by default, like other Spring beans.

That means one instance serves concurrent requests — controllers should be thread-safe (no request-specific mutable fields; put per-request state on parameters, `Model`, or scoped beans).

> [!warning] Unverified traps from the dump
> - You can still mark a controller with @Scope("request") or "session"; that is not the default.
