<!--
reps: 0
priority: 0
-->
#Java/Spring/Transactions/SelfInvocation #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: default EnableTransactionManagement mode is proxy, which cannot advise local this-calls. Switch to AspectJ mode when you must wrap self-invocations with @Transactional as well — there is no proxy; the class bytecode is woven so any method call can start or join a transaction.

Interview lists still recommend extracting a second bean for ordinary code. AspectJ is the option when many self-calls must be advised and you accept weaving.
> [!warning] Unverified traps from the dump
> - AspectJ mode needs spring-aspects plus compile-time or load-time weaving; setting mode without a weaver does not intercept self-calls.
> - Prefer a second bean over weaving the whole application just to fix one self-invocation.
