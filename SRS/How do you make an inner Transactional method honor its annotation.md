<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps prefer extracting the inner method into another @Service so the call is cross-bean and always hits the proxy. Alternative: inject the same type with @Lazy and call self.inner() — the injected reference is the proxy, not this.

Some lists add TransactionTemplate for a programmatic boundary without relying on a second @Transactional. AopContext.currentProxy() appears as a last resort and needs the proxy to be exposed.
> [!warning] Unverified traps from the dump
> - Self-injection can form a circular dependency; dumps pair it with @Lazy.
> - AopContext.currentProxy() couples the class to Spring AOP and throws if exposeProxy is not enabled.
