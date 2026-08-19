<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Weaving links aspects with target objects to produce an advised object.

Times dumps name:

- **Compile-time** — AspectJ `ajc` rewrites bytecode (also post-compile weave of jars).
- **Load-time (LTW)** — a special class loader / Java agent weaves when the class is loaded.
- **Runtime** — Spring AOP: create a proxy around the bean. No bytecode change of the target class.

Spring AOP weaves at **runtime** via proxies. AspectJ supports compile-time and load-time as well.

> [!warning] Unverified traps from the dump
> - Some dumps claim Spring “supports three weaving mechanisms”; typical Spring AOP is runtime proxies only unless you add AspectJ LTW.
