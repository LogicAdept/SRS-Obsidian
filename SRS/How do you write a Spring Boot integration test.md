<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Integration #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

in28minutes:

```java
@RunWith(SpringRunner.class)
@SpringBootTest(classes = Application.class,
    webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class SurveyControllerIT {
  @LocalServerPort
  private int port;
}
```

Then `TestRestTemplate.exchange` against `http://localhost:` + port. Dumps: this is the full stack, real HTTP, slower than MockMvc slices.

> [!warning] Unverified traps from the dump
> - RANDOM_PORT needs a servlet container; MOCK does not bind a port.
