<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.

Draft: Quarkus is built on a common Vert.x layer. The HTTP layer (Quarkus REST, formerly RESTEasy Reactive) can serve requests on the event loop or on worker threads and lets both styles coexist in one app.
Rules of thumb (draft): methods returning plain types/blocking types run on worker threads; methods returning Uni/Multi and not annotated run on the event loop; @Blocking forces a worker thread; @NonBlocking forces the event loop.
Mutiny is the reactive programming model: Uni emits one item or failure; Multi emits n items, completion or failure; extensions expose Uni/Multi APIs (REST client, reactive datasources, Reactive Messaging).
Thread safety: event loop must not be blocked; JDBC and Hibernate are blocking by default, hence worker-thread dispatch unless reactive drivers are used.
Interview caution: "unify" means one stack where both models coexist and interoperate, not that blocking code becomes magically non-blocking.

> [!warning] Unverified traps from the draft
> - Facts above are plausible but unchecked; version numbers and exact API names must be confirmed against official docs before this card is used as a review answer.
> - Comparison cards must keep both sides tagged and avoid absolute always/never claims.
