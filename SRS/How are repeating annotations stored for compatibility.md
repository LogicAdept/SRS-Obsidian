<!--
reps: 0
priority: 0
-->
#Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps (Java 8): repeating annotations are stored in a container annotation the compiler generates. `@Repeatable(Container.class)` marks the repeatable type. The container must have a `value` element whose type is an array of the repeatable type.

```java
@interface Schedules { Schedule[] value(); }

@Repeatable(Schedules.class)
@interface Schedule { String time() default "morning"; }
```

Multiple `@Schedule` on one element become one `@Schedules`. Reflection APIs that understand repeating types unwrap the container; older `getAnnotation(Schedule.class)` may miss repeats unless you read the container or use `getAnnotationsByType`.
> [!warning] Unverified traps from the dump
> - Declaring @Repeatable without a matching container with Schedule[] value() does not compile.
> - Dumps say container and repeatable should share retention and @Inherited; a mismatch is a compiler error.
