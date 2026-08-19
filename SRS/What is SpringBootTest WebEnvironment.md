<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

in28minutes uses `webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT` so an embedded server binds an ephemeral port (`@LocalServerPort`).

Other dump values: `MOCK` (default — mock servlet, MockMvc), `DEFINED_PORT`, `NONE` (no web).

> [!warning] Unverified traps from the dump
> - RANDOM_PORT + TestRestTemplate is not the same as MockMvc on MOCK — different network stack.
