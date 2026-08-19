<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps (Spring testing TOC / Boot lists): the TestContext Framework is Spring’s annotation-driven support for **loading and caching** an `ApplicationContext` around JUnit/TestNG tests (`@ContextConfiguration`, `@SpringBootTest`, `@DirtiesContext`, `@ActiveProfiles`, …).

It is test-framework agnostic. Caching means two test classes with the same config share one context so suites stay fast.

> [!warning] Unverified traps from the dump
> - Cache key includes classes, profiles, property sources — a small annotation difference starts a second context.
