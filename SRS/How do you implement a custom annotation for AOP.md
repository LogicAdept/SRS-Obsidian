<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

1. Declare a runtime method annotation.
2. Pointcut with `@annotation(MyCustomAnnotation)`.
3. Put the annotation on target methods.

```java
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface MyCustomAnnotation {}

@Before("@annotation(MyCustomAnnotation)")
public void beforeAdvice(JoinPoint joinPoint) { ... }
```

> [!warning] Unverified traps from the dump
> - Retention must be RUNTIME or the pointcut cannot see it.
> - The annotated method still has to go through the Spring proxy (public, not self-invoked).
