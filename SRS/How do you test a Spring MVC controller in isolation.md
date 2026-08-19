<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Testing/Mocking #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Use `@WebMvcTest` with `MockMvc` and `@MockBean` for the service:

```java
@RunWith(SpringRunner.class)
@WebMvcTest(value = SurveyController.class, secure = false)
public class SurveyControllerTest {
  @Autowired private MockMvc mockMvc;
  @MockBean private SurveyService surveyService;
}
```

Stub the service with Mockito, `MockMvcRequestBuilders.get(...)`, then assert status/JSON (`JSONAssert` in older lists, `jsonPath` in newer).

> [!warning] Unverified traps from the dump
> - secure = false is a deprecated WebMvcTest attribute; Security tests use @WithMockUser instead.
