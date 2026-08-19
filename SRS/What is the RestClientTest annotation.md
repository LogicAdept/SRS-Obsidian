<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@RestClientTest` is a Boot slice for **HTTP clients** (`RestTemplate` / `WebClient` beans). Dumps: use it instead of `@WebMvcTest` (controllers) or `@SpringBootTest` (full app).

Often paired with `MockRestServiceServer`.

> [!warning] Unverified traps from the dump
> - It does not test your @RestController; it tests the client that calls someone else.
