<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@DirtiesContext` marks the test’s `ApplicationContext` dirty: remove from the TestContext cache and close. The next test with the same config gets a new container.

Typical dump reason: the test changed a singleton’s state. Class- or method-level.

> [!warning] Unverified traps from the dump
> - Default modes differ for class vs method; AFTER_CLASS vs AFTER_EACH_TEST_METHOD is a follow-up.
