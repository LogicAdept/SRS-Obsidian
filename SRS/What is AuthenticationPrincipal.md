<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #Java/Annotations #Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: @AuthenticationPrincipal on a controller parameter injects Authentication.getPrincipal() (often UserDetails) without SecurityContextHolder.getContext() and a cast. Preferred in controllers over Principal (username only) or a static holder call.
> [!warning] Unverified traps from the dump
> - Anonymous or missing auth: the argument can be null. error = true on the annotation makes that a failure instead of null.
> - Do not put SecurityContextHolder in @Async business code; this annotation is for the MVC call.
