<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Configurable` marks types whose properties should be injected **even when Spring did not instantiate the object** (domain objects created with `new`). Dumps file it with Core annotations as “inject properties of domain objects.”

> [!warning] Unverified traps from the dump
> - This is AspectJ / load-time weaving territory, not ordinary `@Component` scanning. Without weaving, the annotation does nothing.
> - Do not stretch it into “another stereotype like `@Service`.”
