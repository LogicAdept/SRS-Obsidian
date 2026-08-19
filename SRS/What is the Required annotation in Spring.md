<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@Required` on a JavaBean **setter** means that property must be configured (XML/`<property>` or equivalent injection). If it is missing, the container throws `BeanInitializationException`. `RequiredAnnotationBeanPostProcessor` enforces it. `context:annotation-config` and `context:component-scan` register that processor by default.

> [!warning] Unverified traps from the dump
> - It checks that a value was **configured**, not that the value is non-null.
> - It does not replace an init method. The annotation is widely treated as obsolete next to constructor injection and `@Autowired` on a required setter.
