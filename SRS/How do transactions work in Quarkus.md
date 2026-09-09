<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# How do transactions work in Quarkus

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: Narayana transaction manager; jakarta @Transactional (javax→jakarta since 3.0) with JTA semantics, TransactionMode/rollbackOn; @Transactional on class/method; programmatic via UserTransaction; reactive variant @WithTransaction for hibernate-reactive; @ReactiveTransaction semantics.
Mandatory transactional beans default; Agroal pool integration; transaction scope.
