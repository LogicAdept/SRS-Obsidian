<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@WebMvcTest` is a Boot **slice**: only the web layer (controllers, `@ControllerAdvice`, filters, interceptors) plus auto-configured `MockMvc`. It does **not** load `@Service` / `@Repository` / DB.

Collaborators of the controller must be `@MockBean`. Optionally restrict to one controller: `@WebMvcTest(SurveyController.class)`.

Older dumps: `@WebMvcTest(..., secure = false)` to skip Security.

> [!warning] Unverified traps from the dump
> - If Spring Security is on the classpath, unauthenticated MockMvc calls often get 401/302 unless you mock a user.
> - A nearby card lists slices in general; this one is the WebMvcTest interview cue.
