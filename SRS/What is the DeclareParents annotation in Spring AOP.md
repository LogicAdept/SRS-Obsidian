<!--
reps: 0
priority: 0
-->
#Java/Spring/Framework/AOP #Java/Annotations #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`@DeclareParents` is the AspectJ-style **introduction**: add an interface (and a default implementation) to matching types.

```java
@DeclareParents(value = "com.example.service.*+", defaultImpl = AdditionalFunctionalityImpl.class)
public static AdditionalFunctionality additionalFunctionality;
```

> [!warning] Unverified traps from the dump
> - Callers must use the introduced interface; a dump example forgets the cast.
