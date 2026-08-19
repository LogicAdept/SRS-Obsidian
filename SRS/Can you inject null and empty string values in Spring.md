<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. XML (and equivalent Java config) can inject an empty string or `null` into a property. Dumps answer this as a one-liner: it is allowed.

Typical XML from the same era of lists: `<property name="x" value=""/>` for empty string, and `<property name="x"><null/></property>` for null.

> [!warning] Unverified traps from the dump
> - XML autowiring still cannot autowire primitives, `String`, and `Class`; explicit `null`/empty is not autowiring.
> - `@Autowired` on an object type will not inject null unless `required=false` (or `Optional` / `@Nullable` in later Spring). That is a different rule than XML `<null/>`.
