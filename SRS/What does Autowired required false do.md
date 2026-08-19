<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Autowired` is required by default: if no matching bean exists, context startup fails. `@Autowired(required = false)` makes that injection optional; the field/parameter stays `null` (or unused) when nothing matches.

Dumps contrast this with `@Resource` / `@Inject`, which do not have Spring’s `required` flag.

Since Spring 4.3 a **single** constructor does not need `@Autowired` at all.

> [!warning] Unverified traps from the dump
> - Optional constructor parameters still interact with Kotlin/`Optional`/`@Nullable` — dumps only mention `required = false` on `@Autowired`.
> - `required = false` on one of several constructors is how you mark which constructor is optional to use, not “this dependency may be missing” in every case — verify at fill time.
