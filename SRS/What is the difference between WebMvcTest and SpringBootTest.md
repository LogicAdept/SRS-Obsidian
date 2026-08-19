<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@WebMvcTest`: web slice only, fast, MockMvc auto-configured, mock services with `@MockBean`.

`@SpringBootTest`: full (or almost full) Boot context including auto-config. Slow. Real collaborators unless you mock them. For HTTP you add `@AutoConfigureMockMvc` or `webEnvironment = RANDOM_PORT` + `TestRestTemplate`.

`@ContextConfiguration` is the lower-level TestContext way to load a hand-picked config.

> [!warning] Unverified traps from the dump
> - You cannot put both @WebMvcTest and @SpringBootTest on the same class (dump/Baeldung claim).
