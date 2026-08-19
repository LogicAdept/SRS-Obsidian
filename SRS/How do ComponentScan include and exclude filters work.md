<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC/Configuration #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@ComponentScan` / `<context:component-scan>` can **include** or **exclude** candidates. XML filter types dumps list:

- `annotation` — presence of a given annotation
- `assignable` — assignable to a given class
- `regex` — class name pattern
- `aspectj` — AspectJ type pattern

Java config: `@ComponentScan.Filter` with `FilterType.ASSIGNABLE_TYPE` (and friends), often with `useDefaultFilters = false` so only the include list is scanned.

> [!warning] Unverified traps from the dump
> - `@ComponentScan` always assumes default annotation-config processing (`@Autowired` and friends). There is no `annotation-config` attribute like the XML element.
> - On `AnnotationConfigApplicationContext`, processors are always registered; trying to turn them off at the `@ComponentScan` level is ignored in dump wording.
