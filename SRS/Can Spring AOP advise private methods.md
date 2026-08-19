<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: **no**. Spring AOP is proxy-based and intercepts calls through the proxy, typically **public** methods on the bean’s API.

Private methods are invoked on `this` inside the class, so they never hit the proxy. Use AspectJ weaving if you must advise private/protected call sites.

> [!warning] Unverified traps from the dump
> - Package-visible / protected methods on CGLIB proxies are a grey area dumps often collapse to “public only”.
> - Nearby card lists proxy limitations more broadly (final, self-invocation).
