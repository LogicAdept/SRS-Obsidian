<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Autowired` on an array, `List`, or `Set` of a type injects **every** bean of that type in the context.

`Map<String, T>` injects the same beans with **bean names as keys** (key type must be `String`).

Order of a `List` can be influenced by `@Order` / `Ordered` (mentioned for processors and runners in dumps).

> [!warning] Unverified traps from the dump
> - An empty list vs a missing single bean: `required = false` on a single `T` is not the same as injecting `List<T>`.
> - Map keys are bean names, not `@Qualifier` values unless those match the name.
