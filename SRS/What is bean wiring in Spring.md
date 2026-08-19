<!--
reps: 0
priority: 0
-->
#Java/Spring/Core/IoC #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

**Bean wiring** is the container creating associations between beans (injecting collaborators). Explicit wiring names the other bean (`ref`, constructor-arg, `@Autowired` + `@Qualifier`). Autowiring infers the link by name or type.

Dumps treat “good practice” as making those links explicit when ambiguity is possible.

> [!warning] Unverified traps from the dump
> - Wiring is not the same as `BeanDefinition` parsing; it happens when the instance is populated.
> - XML `autowire` modes and `@Autowired` are both wiring, different configuration styles.
