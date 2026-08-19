<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

No. `@Qualifier` is not limited to echoing the `value` of `@Component("name")`. Dumps say you can put `@Qualifier` **on the class** (or on each bean) to give injection points a qualifier name, instead of encoding that name only in `@Component`.

Together with `@Primary`: if two beans share a type, `@Primary` picks a default; `@Qualifier` lets you keep **both** and choose at the injection point.

> [!warning] Unverified traps from the dump
> - Custom qualifier annotations (meta-annotated with `@Qualifier`) show up in senior interviews; many dumps only show the string form.
> - `@Resource(name=…)` is by-name lookup, not the same as `@Qualifier`.
