<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Mocking #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@SpyBean` puts a **spy** (partial mock) of a real Spring bean into the test context: real methods run unless stubbed.

Contrast: `@MockBean` replaces the bean with a full mock.

> [!warning] Unverified traps from the dump
> - Spying a bean that is already a JDK/CGLIB proxy is a common failure mode.
