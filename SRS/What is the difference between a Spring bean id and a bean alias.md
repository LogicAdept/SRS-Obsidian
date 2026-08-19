<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

In XML, `id` is the unique bean identifier used as the map key in the factory. `name` can hold extra **aliases** (a string array in dumps): first token is the id, the rest are aliases for the same definition.

`getBean` and `ref` can use either the id or an alias. Annotation beans use the `@Component("name")` / `@Bean` method name as the id; aliases are less common (`@Bean(name = {…})`).

> [!warning] Unverified traps from the dump
> - Two beans with the same id still clash; aliases do not create a second instance.
> - Autowire `byName` matches property name to id/alias, not to the Java type name.
