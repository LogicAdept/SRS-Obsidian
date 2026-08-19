<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

use `WebClient`, not `RestTemplate`. `WebClient.create("https://api.example.com").get().uri("/data").retrieve().bodyToMono(String.class)` — non-blocking `Mono`/`Flux`.

> [!warning] Unverified traps from the dump
> - `RestClient` is the modern *blocking* fluent client on MVC; dumps for this cue name `WebClient` for the reactive app.

