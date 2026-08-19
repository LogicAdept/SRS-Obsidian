<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: method security is a Spring AOP proxy. this.secured() inside the same class does not go through the proxy, so @PreAuthorize / @Secured do not run.

Fix in dumps: move the secured method to another Spring bean and inject it.
> [!warning] Unverified traps from the dump
> - AspectJ mode (AdviceMode.ASPECTJ) is the dump alternative when you must intercept self-calls. Default is PROXY.
