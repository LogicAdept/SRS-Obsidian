<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

XML `autowire` on a `<bean>` (or default-autowire) has these modes:

- `no` — default; you write explicit `ref` / constructor-arg.
- `byName` — match property name to a bean id.
- `byType` — match property type; more than one candidate is fatal. Dumps mention `autowire-candidate="false"` to exclude a bean.
- `constructor` — like `byType` for constructor arguments.
- `autodetect` — try constructor, then byType (older lists).

Annotation wiring (`@Autowired` by type, plus `@Qualifier`) is a separate mechanism.

> [!warning] Unverified traps from the dump
> - `byType` with two beans of the same type fails unless you disambiguate.
> - `autodetect` is legacy; do not treat it as a Boot-era default.
