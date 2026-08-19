<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Integration #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Empty `contextLoads` test:

```java
@SpringBootTest
class ApplicationContextLoadTest {
    @Test
    void contextLoads() {}
}
```

Fails if Boot cannot start the context (bad auto-config, missing bean). Early smoke test, not a substitute for slice tests.

> [!warning] Unverified traps from the dump
> - A passing contextLoads test can still hide broken web/security wiring you never called.
