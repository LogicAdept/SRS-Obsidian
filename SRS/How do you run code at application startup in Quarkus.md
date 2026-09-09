<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# How do you run code at application startup in Quarkus

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: observe StartupEvent via @Observes, use @Startup on a bean, or run RUNTIME_INIT tasks via init tasks; the run() method order vs constructor vs PostConstruct.
Warning: beans are lazy; observing StartupEvent forces eager instantiation.
