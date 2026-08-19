<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

The proxy intercepts only calls that go **through the proxy**. `this.otherMethod()` is a direct call on the target, so `@Transactional` / `@Async` / `@Cacheable` / custom `@Around` do not run.

Dumps’ fixes: move the method to another bean; self-inject (`@Lazy` / `ObjectProvider`); or AspectJ weaving; some lists mention `AopContext.currentProxy()` with `exposeProxy=true`.

> [!warning] Unverified traps from the dump
> - A Language-tagged self-invocation card already exists; this one is the AOP wording interviewers use.
> - AopContext couples the class to Spring AOP and is off by default.
