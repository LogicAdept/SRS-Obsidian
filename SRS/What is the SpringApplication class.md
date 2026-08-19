<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`SpringApplication` bootstraps and launches a Spring application from `main`. Dumps: it sets up the application context, auto-configuration, and the embedded server. Typical call: `SpringApplication.run(MyApp.class, args)`.

> [!warning] Unverified traps from the dump
> - `run` is not just `new AnnotationConfigApplicationContext` — Boot still applies its startup extras.
