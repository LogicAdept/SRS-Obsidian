<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Three annotations inject a dependency. Resolution order differs.

`@Resource` (Jakarta/Java EE): name first, then type, then qualifier. The name comes from the `name` attribute or from the field/setter name. No extra annotation is required just to pick a bean by name.

`@Autowired` (Spring) and `@Inject` (JSR-330): type first, then qualifier/descriptor, then name. A field name that does not match the bean id still injects if the type is unique.

`@Autowired(required = false)` can mark an injection optional. `@Resource` / `@Inject` do not have that Spring-specific flag in the dump.

If several candidates exist, dumps say add `@Qualifier` (or `@Named` with `@Inject`).

> [!warning] Unverified traps from the dump
> - Mixing `@Resource` with Spring `@Qualifier` is shown in dumps; official matching rules for JSR-250 vs Spring `@Qualifier` are a follow-up to verify.
> - `@Resource` is claimed to be more portable if you leave Spring; `@Autowired` is Spring-only.
