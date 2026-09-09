<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# What are the limitations of GraalVM native images

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: closed-world assumption — no runtime class loading, dynamic proxies/reflection must be registered (Quarkus does this at build for its stack), resources need inclusion, JNI limited; build cost (memory, minutes), no JIT warmup tradeoff, C2 absent; some libraries unsupported; static init restrictions.
