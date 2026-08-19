<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: no for the default proxy mode. Private (and typically final) methods are not advised. The interceptor only sees calls that go through the Spring proxy to a public method on the bean.
> [!warning] Unverified traps from the dump
> - Annotating a private helper and calling it from a public method is still self-invocation plus an unproxied method — double miss.
