<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps use `JSONAssert.assertEquals(expected, actualJson, false)` in MockMvc / `TestRestTemplate` tests so you compare JSON documents without a brittle full-string equals.

The boolean is *strict*: `false` allows extra fields.

> [!warning] Unverified traps from the dump
> - JSONAssert is org.skyscreamer, not a Spring class. JUnit 5 tests more often use jsonPath or AssertJ.
