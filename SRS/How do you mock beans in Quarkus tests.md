<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# How do you mock beans in Quarkus tests

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: @InjectMock replaces a bean in the container (QuarkusTest mock support), @InjectMock for @Inject fields, combined with @MockBean alternative (deprecated in favor of InjectMock?) — verify in docs; works only in same-JVM tests, not integration tests.
