<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# How do you schedule periodic tasks in Quarkus

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: quarkus-scheduler — @Scheduled annotation (every=, cron=, delayed=), runs on its own scheduler threads (not event loop), identity overlap control, must be on @ApplicationScoped beans; cron syntax and dialects.
