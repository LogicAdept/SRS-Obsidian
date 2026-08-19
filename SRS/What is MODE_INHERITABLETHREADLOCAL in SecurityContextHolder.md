<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: SecurityContextHolder.setStrategyName(MODE_INHERITABLETHREADLOCAL) copies context to child threads. Interview follow-up: do not always use it — pooled threads reuse workers; user X then user Y can inherit X’s Authentication. Prefer MODE_THREADLOCAL plus DelegatingSecurityContextExecutor at submit time.
> [!warning] Unverified traps from the dump
> - Setting the strategy after threads are already running does not retrofit them.
