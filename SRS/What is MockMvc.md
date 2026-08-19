<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Mocking #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: MockMvc is a Spring Test utility that **simulates HTTP requests** against Spring MVC without starting a real servlet container. It runs in-memory.

Typical use: `@Autowired MockMvc` in `@WebMvcTest`, or `@SpringBootTest` plus `@AutoConfigureMockMvc`. `perform(get(...))` then `andExpect(status().isOk())` (status, JSON, model, view).

> [!warning] Unverified traps from the dump
> - @SpringBootTest alone does not inject MockMvc; you need @AutoConfigureMockMvc. @WebMvcTest includes it.
