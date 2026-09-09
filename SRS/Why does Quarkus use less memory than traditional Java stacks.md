<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# Why does Quarkus use less memory than traditional Java stacks

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: fewer classes loaded at runtime (build-time work removes discovery machinery), no reflection-heavy frameworks, lazy proxies, metadata precomputed, native images avoid JVM heap overhead; RSS targets; dev-mode vs prod memory.
