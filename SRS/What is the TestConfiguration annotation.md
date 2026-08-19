<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@TestConfiguration` defines beans or overrides **only for tests** (nested in a test class or a test-only config).

Dumps: custom beans / replacements that must not leak into the main `@SpringBootApplication` scan.

> [!warning] Unverified traps from the dump
> - A nested @TestConfiguration is picked up by that test; a top-level one may need @Import. Component scan of src/test/java can accidentally pull it into every test.
