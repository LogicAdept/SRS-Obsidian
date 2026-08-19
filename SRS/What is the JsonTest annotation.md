<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@JsonTest` is a Boot slice that loads **only JSON** serialization components (Jackson `ObjectMapper`, `@JsonComponent`, …) to test DTO mapping without MVC or JPA.

> [!warning] Unverified traps from the dump
> - It will not start MockMvc or a database.
