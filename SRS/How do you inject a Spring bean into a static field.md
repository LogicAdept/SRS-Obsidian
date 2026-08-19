<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Spring does not inject into `static` fields. `@Autowired` on a static field leaves it `null`.

Workaround shown in dumps: a non-static setter that Spring can call, which then assigns the static field.

```java
@Component
public class TestDataInit {
    private static OrderItemService orderItemService;

    @Autowired
    public void setOrderItemService(OrderItemService orderItemService) {
        TestDataInit.orderItemService = orderItemService;
    }
}
```

Static initialization still runs before the bean is created, so anything that reads the static field too early can still see `null`.

> [!warning] Unverified traps from the dump
> - This pattern is a last resort; prefer instance injection. Static holders hide the lifecycle and break tests.
> - Field `@Autowired private static …` is a popular lie that “just works.”
