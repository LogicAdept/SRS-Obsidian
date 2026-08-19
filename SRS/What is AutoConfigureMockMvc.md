<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@AutoConfigureMockMvc` registers an injectable `MockMvc` in a **full** `@SpringBootTest` (where MockMvc is not auto-added).

`@WebMvcTest` already includes this. GFG: `@SpringBootTest` + `@AutoConfigureMockMvc` tests the web layer with the rest of the context still loaded — slower than a slice.

> [!warning] Unverified traps from the dump
> - @AutoConfigureMockMvc does not make @SpringBootTest fast; the full context still starts.
> - addFilters = false can skip the Security filter chain (dump/follow-up).
