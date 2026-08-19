<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Integration #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`TestRestTemplate` is Boot’s test HTTP client for calls against a running app (typically `@SpringBootTest` + `RANDOM_PORT`).

Dump: `restTemplate.exchange(url, HttpMethod.GET, entity, String.class)` then assert body with JSONAssert.

Unlike MockMvc, this goes through the real server (filters, security, serialization) over HTTP.

> [!warning] Unverified traps from the dump
> - Do not confuse with RestTemplate in production code. WebTestClient is the reactive / newer alternative in dumps.
