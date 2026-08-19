<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebMvc #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`ContentNegotiationManager` picks the response media type from path extension, query parameter, and/or `Accept` header.

Configure via `WebMvcConfigurer.configureContentNegotiation` (`favorPathExtension`, `favorParameter`, `ignoreAcceptHeader`, `defaultContentType`).

> [!warning] Unverified traps from the dump
> - favorPathExtension has been discouraged/deprecated in later Spring versions; dumps still show it as true.
