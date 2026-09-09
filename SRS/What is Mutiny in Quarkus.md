<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# What is Mutiny in Quarkus

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: Mutiny is the reactive programming library Quarkus standardizes on — event-driven, with two core types: Uni (0..1 item) and Multi (0..n items), built on a subscription model where pipelines are declared first and run on subscription.
Contrast with CompletableFuture/Reactor; key operators; lazy vs eager; cancellation.
