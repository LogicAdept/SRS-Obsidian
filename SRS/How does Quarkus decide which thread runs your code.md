<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# How does Quarkus decide which thread runs your code

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: Quarkus separates the event loop (IO) threads from worker threads. REST endpoints run on the event loop when they return Uni/Multi or are declared non-blocking; blocking code must switch to a worker thread via @Blocking or by returning ordinary types (which Quarkus dispatches to a worker).
Smart dispatch in Quarkus REST: annotations and the return type decide the thread; running JDBC/JPA on the event loop starves all other requests.
