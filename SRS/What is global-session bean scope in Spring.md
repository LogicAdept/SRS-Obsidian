<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Scopes #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`global-session` (XML `scope="globalSession"`, constant `WebApplicationContext.SCOPE_GLOBAL_SESSION`) scoped a bean to a **global HTTP session**. Dumps say it is only valid in a web-aware `ApplicationContext` and was aimed at **Portlet** apps (one session spanning several portlets), unlike ordinary `session` (one HTTP session).

> [!warning] Unverified traps from the dump
> - Spring 5 dumps list Portlet support as **removed**. Answering “we use global-session in Boot REST” is a stale-list trap.
> - Servlet apps use `session`, not `global-session`.
