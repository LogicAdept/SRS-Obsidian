<!--
reps: 0
priority: 0
-->
#Java/Quarkus #SRS #New

# What bean scopes does Quarkus support

> [!warning] Untrusted draft
> Drafted from general framework knowledge, not from an opened question dump. Not yet checked against official documentation. Do not treat this as a review answer.
Draft cue: ArC supports CDI scopes: @Dependent (pseudo), @ApplicationScoped (normal), @RequestScoped (normal), @Singleton (pseudo), plus extras like @Startup-annotated beans and various Quarkus-provided scopes (transaction-scoped, etc.).
Normal scopes get client proxies; @Inject works at build time; @SessionScoped is not available without a servlet container extension.
