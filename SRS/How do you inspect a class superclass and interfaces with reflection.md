<!--
reps: 0
priority: 0
-->
#Java/Language/Reflection #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

```java
Class<?> superclass = clazz.getSuperclass();
Class<?>[] interfaces = clazz.getInterfaces();
```

Is-a checks: `MyInterface.class.isAssignableFrom(MyClass.class)` and `SuperClass.class.isAssignableFrom(SubClass.class)`.

Walking only `getSuperclass()` once is not a full hierarchy walk — dumps mention comparing the returned class or using `isAssignableFrom`.

> [!warning] Unverified traps from the dump
> - `getInterfaces()` is direct interfaces, not a deep flatten of the whole graph, unless you recurse (not shown).
