<!--
reps: 0
priority: 0
-->
#Java/Spring/Security #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: the default strategy is ThreadLocal so Authentication is available anywhere on the same request thread without passing SecurityContext as a method argument. That is also why a thread pool can leak a previous user’s context if you do not clear or wrap the executor.
> [!warning] Unverified traps from the dump
> - MODE_INHERITABLETHREADLOCAL is not a free pass for pools: reused worker threads can inherit the wrong user.
