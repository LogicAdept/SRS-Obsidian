<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Cache #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@SpringBootTest` plus verifying the cached method runs once for two identical calls. One dump uses Mockito `verify(..., times(1))` on the service after two `getUserById` calls.

Goal: prove the second call was a hit and evictions behave.

> [!warning] Unverified traps from the dump
> - Verifying a `@Autowired` real service with Mockito `times(1)` only works if that bean is a mock — the dump snippet is easy to copy wrong.
> - Slice tests may use a no-op cache unless you opt in.

