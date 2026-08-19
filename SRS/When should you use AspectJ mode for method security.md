<!--
reps: 0
priority: 0
-->
#Java/Spring/Security/MethodSecurity #Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dump: default AdviceMode.PROXY only intercepts calls through the Spring proxy. Use AdviceMode.ASPECTJ when you must secure self-invocation or otherwise weave the class.

Most dumps still say: prefer extracting a second bean over switching the whole app to AspectJ.
> [!warning] Unverified traps from the dump
> - AspectJ mode needs a weaver. Setting mode = ASPECTJ on the annotation without compile/load-time weaving is a silent no-op.
