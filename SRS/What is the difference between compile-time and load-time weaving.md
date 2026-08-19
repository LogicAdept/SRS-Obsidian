<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

**Compile-time:** AspectJ `ajc` weaves during compilation (or post-compile into class/JAR files). Bytecode is already advised before the JVM runs your app.

**Load-time:** weaving happens when classes are loaded. Needs a special class loader or Java agent. Dumps: may slow class loading.

Spring AOP’s default proxy approach is neither of these; it is runtime wrapping.

> [!warning] Unverified traps from the dump
> - You can still use AspectJ LTW inside a Spring app when proxy AOP is not enough.
