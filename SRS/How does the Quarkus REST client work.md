<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# How does the Quarkus REST client work

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: declare an interface annotated @RegisterRestClient with Jakarta REST annotations; Quarkus generates the implementation at build time (quarkus-rest-client / quarkus-rest-client-jackson); inject via @RestClient; config via quarkus.rest-client.<key>.* (url, timeouts); MicroProfile REST Client spec.
