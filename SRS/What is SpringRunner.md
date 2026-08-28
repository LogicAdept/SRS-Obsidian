<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Testing/JUnit #Java/Annotations #SRS

# What is `SpringRunner`?

> [!abstract] Short answer
> **`SpringRunner`** (Spring Framework 4.3+, `org.springframework.test.context.junit4`) is a **JUnit 4** alias for **`SpringJUnit4ClassRunner`**. `@RunWith(SpringRunner.class)` constructs a **`TestContextManager`** so JUnit 4 tests get TestContext: context load, `@Autowired` on the test instance, transactions, `@DirtiesContext`. It requires **JUnit 4.12 or higher**. It is **not** a JUnit 5 API.

## Runner versus rules versus Jupiter

`SpringJUnit4ClassRunner` extends JUnit’s `BlockJUnit4ClassRunner`. `SpringRunner` is `final` and only exists to shorten the `@RunWith` line. The constructor takes the test `Class` and **`createTestContextManager`**. `createTest()` builds the instance then **`prepareTestInstance`**. Class/method before/after statements wrap TestContext callbacks (`RunBeforeTestClassCallbacks`, …).

JUnit 5 replacements: [[What is SpringExtension]], `@SpringJUnitConfig`, Boot `@SpringBootTest` (`@ExtendWith(SpringExtension.class)`). The shared engine is [[What is the Spring TestContext Framework]]. Config: [[What is the ContextConfiguration annotation]].

```java
@RunWith(SpringRunner.class)
@ContextConfiguration(classes = TestConfig.class)
public class SimpleJUnit4Test {

	@Autowired
	TitleRepository titles;

	@Test
	public void findById() {
		assertNotNull(titles.findById(10L));
	}
}
```

**Listing 1.** Conceptual JUnit 4 TestContext test. Without `@ContextConfiguration` (or Boot’s loader), default listeners still expect a context — the support-classes “empty listeners” sample is only for tests that **disable** that.

You **cannot** also `@RunWith(MockitoJUnitRunner.class)` or JUnit 4 `Parameterized`: one runner per class. Combine TestContext with those runners via **`SpringClassRule` + `SpringMethodRule`** (JUnit 4.12+), which are runner-independent.

```d2
direction: down
runwith: "@RunWith(SpringRunner.class)" {
  width: 260
  height: 40
  style.fill: "#e3f2fd"
}
alias: "SpringJUnit4ClassRunner" {
  width: 240
  height: 40
  style.fill: "#fff3e0"
}
tcm: "TestContextManager" {
  width: 220
  height: 40
  style.fill: "#e8f5e9"
}
di: "prepareTestInstance\n(field/setter injection)" {
  width: 260
  height: 50
  style.fill: "#fce4ec"
}

runwith -> alias
alias -> tcm
tcm -> di
```

**Fig. 1.** JUnit 4 has a single `Runner`. `SpringRunner` is that runner with TestContext wired in.

JUnit 4 does **not** use Jupiter `ParameterResolver`. **`@Autowired` on a test constructor has no effect** for JUnit 4 / TestNG: TestContext does not construct those test classes. Use **fields or setters**. Abstract bases (`AbstractJUnit4SpringContextTests`) are optional.

> [!warning]No runner means no TestContext DI
> A plain JUnit 4 class with `@Autowired` fields and **no** `@RunWith(SpringRunner.class)` (and no Spring rules) never calls `TestContextManager.prepareTestInstance`. Those fields stay **null**. Putting `@RunWith(SpringRunner.class)` on a **JUnit Jupiter** class is the wrong annotation: Jupiter looks for `@ExtendWith`, not `@RunWith`.

> [!warning]One runner only
> `@RunWith(MockitoJUnitRunner.class)` **replaces** `SpringRunner`. Keep Mockito and TestContext together with **`@ClassRule SpringClassRule`** plus **`@Rule SpringMethodRule`**, or move to Jupiter and `@ExtendWith` for both Spring and Mockito.

> [!tip] Interview answer
> **`SpringRunner` is the short JUnit 4 name for `SpringJUnit4ClassRunner`.** `@RunWith(SpringRunner.class)` is how JUnit 4 tests enter TestContext. JUnit 5 uses `SpringExtension` instead. Forget the runner and `@Autowired` on the test class is never processed. Need Mockito’s runner too? Use Spring’s JUnit 4 rules, not two `@RunWith` annotations.
