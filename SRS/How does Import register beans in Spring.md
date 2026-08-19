<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Besides `@Bean` methods and stereotype + `@ComponentScan`, dumps list `@Import` as a way to put classes into the current container:

```java
@ComponentScan
@Import({Dog.class, Cat.class})
public class App { }
```

`@Import` can import `@Configuration` classes or regular component classes. `@Conditional` on a `@Configuration` class also applies to its `@Import`s and `@ComponentScan` (dump claim). `@ImportResource` is the XML sibling.

> [!warning] Unverified traps from the dump
> - `@Import` of a POJO is not the same as component-scanning a package; you name the classes explicitly.
> - Conditions on the importing `@Configuration` may skip the imported classes.
