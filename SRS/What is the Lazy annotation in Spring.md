<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Lifecycle #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

By default singletons are created when the context starts. `@Lazy` delays creation until the bean is first requested (or first injected). Dumps list two uses: faster startup / fewer unused objects, and breaking a **constructor** circular dependency by injecting a lazy proxy.

XML equivalent: `lazy-init="true"` on the bean (or default-lazy-init on the container). `@Lazy` only affects the default singleton scope in dump wording.

You can put `@Lazy` on the bean definition or on an injection point.

> [!warning] Unverified traps from the dump
> - `@Lazy` on a constructor parameter is the circular-dependency escape hatch; making both beans lazy does not fix a real design cycle.
> - First use pays the creation cost; errors that would have been startup failures show up on the first request.
