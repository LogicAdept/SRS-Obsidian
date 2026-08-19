<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

When a bean is used **only as a property (or constructor argument) of another bean**, XML can nest a `<bean>` inside `<property>` or `<constructor-arg>`. That nested definition is an **inner bean**: usually anonymous (no id you can look up), and dumps say the scope is typically **prototype**.

It cannot be injected or referenced from elsewhere in the container.

> [!warning] Unverified traps from the dump
> - Giving an inner bean an `id` does not make it a first-class shared singleton in dump wording; treat it as private to the outer bean.
> - Java config has no inner-bean XML trick; you just call a `@Bean` method or `new` inside the factory method.
