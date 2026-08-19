<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #Java/Spring/Framework/Testing #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`WebClient` is the reactive HTTP client (non-blocking, backpressure, lambdas, sync and async). `WebTestClient` is for tests — a thin shell around `WebClient`. It can hit a real server over HTTP or bind directly to a WebFlux app with mock request/response and no HTTP server.

`WebTestClient` is the test-time reactive client that can bind to WebFlux with mock request/response.

> [!warning] Unverified traps from the dump
> - Production `WebClient` is not a MockMvc stand-in; `WebTestClient` is the test client dumps name.
> - Do not use production `WebClient` as your MockMvc stand-in.

