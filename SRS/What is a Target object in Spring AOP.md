<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The target (advised object) is the object one or more aspects apply to — the original bean behind the proxy.

Callers usually hold the **proxy**, not the raw target. Self-calls on `this` hit the target and skip advice.

> [!warning] Unverified traps from the dump
> - JoinPoint.getTarget() vs getThis() is a follow-up: target is the advised object, this is the proxy (dump claim — verify).
