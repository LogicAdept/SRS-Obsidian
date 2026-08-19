<!--
reps: 0
priority: 0
-->
#Java/Spring/Boot #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@SpringBootApplication` includes `@ComponentScan` of the annotated class's package and sub-packages. Dumps: put the main class in the root package so the rest of the project is scanned. A main class in `com.acme.app.web` will not see `com.acme.app.service`.

> [!warning] Unverified traps from the dump
> - Moving `main` into a nested package is a dump-style 'my `@Service` is not a bean' bug.
