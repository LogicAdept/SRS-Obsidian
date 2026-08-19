<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Testing/JUnit #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Older dumps: `@RunWith(SpringRunner.class)` (alias of `SpringJUnit4ClassRunner`) so JUnit 4 runs with the Spring TestContext framework (`@SpringBootTest`, `@WebMvcTest`, `@ContextConfiguration`).

JUnit 5 dumps: `@ExtendWith(SpringExtension.class)` or meta-annotations that include it (`@SpringBootTest` already does).

> [!warning] Unverified traps from the dump
> - Forgetting the runner/extension means @Autowired on the test class stays null.
