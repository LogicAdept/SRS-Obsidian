<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Spring/Security #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `@WithMockUser`, `@WithUserDetails`, or `SecurityMockMvcRequestPostProcessors`.

Example: `@WithMockUser(username = "user", roles = {"USER"})` on a `@WebMvcTest` method, then `mockMvc.perform(get("/user")).andExpect(status().isOk())`.

Needs `spring-security-test`.

> [!warning] Unverified traps from the dump
> - @WebMvcTest loads the security filter chain if Security is on the classpath — without a mock user you get 401/302.
