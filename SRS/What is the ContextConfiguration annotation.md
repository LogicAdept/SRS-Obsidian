<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/Testing #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@ContextConfiguration` tells the Spring TestContext framework **how to load** the `ApplicationContext` for a test (XML or `@Configuration` classes).

```java
@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration(classes = PaymentConfiguration.class)
public class PaymentServiceTests {
  @Autowired PaymentService paymentService;
}
```

Lower-level than `@SpringBootTest` (no Boot auto-config unless you include it).

> [!warning] Unverified traps from the dump
> - JUnit 5: @ExtendWith(SpringExtension.class) or @SpringJUnitConfig instead of SpringJUnit4ClassRunner.
