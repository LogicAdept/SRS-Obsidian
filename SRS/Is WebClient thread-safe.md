<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/WebFlux #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. `WebClient` is thread-safe because it is immutable.

> [!warning] Unverified traps from the dump
> - Immutability of the client is not the same as sharing a mutable `WebClient.Builder` incorrectly, which dumps do not discuss.

