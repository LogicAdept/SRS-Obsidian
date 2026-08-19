<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Autowired` (and `@Inject`) on these types is satisfied by the container itself; you do not declare a collaborator `@Bean` of that type:

- `BeanFactory`
- `ApplicationContext`
- `ResourceLoader`
- `ApplicationEventPublisher`
- `MessageSource`

Same idea as the Aware interfaces, without implementing `*Aware`.

> [!warning] Unverified traps from the dump
> - Injecting `ApplicationContext` to call `getBean` is a service-locator smell dumps still mention.
> - `ApplicationEventPublisher` is how code publishes events without depending on the full context type.
