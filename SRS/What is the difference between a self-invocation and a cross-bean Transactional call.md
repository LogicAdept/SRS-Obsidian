<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A call from another Spring bean goes through the transactional proxy, so TransactionInterceptor sees the inner @Transactional and re-evaluates propagation, isolation, and rollback rules. A same-class this.inner() call is a direct invoke on the target object; the proxy is not in the path, so the inner annotation is ignored.

Dumps contrast: userService.saveUser() from a controller or another service starts a transaction; registerUser() calling saveUser() in the same class does not apply saveUser's attributes.
> [!warning] Unverified traps from the dump
> - JDK and CGLIB proxies both skip this.inner(); subclassing does not intercept self-calls.
> - If the outer method is already transactional, the inner self-call still runs in that outer transaction — not because REQUIRED joined, but because the inner interceptor never ran.
