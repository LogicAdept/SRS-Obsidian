<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A dump: in JavaBeans, properties are typically wrappers so they can represent unset values.

```java
public class Customer {
    private Integer age;  // can be null if age is unknown
    public Integer getAge() { return age; }
    public void setAge(Integer age) { this.age = age; }
}
```

A primitive `int age` would default to `0`, which may be a real age and cannot mean “unknown.”

> [!warning] Unverified traps from the dump
> - Nullable wrappers help “unknown”; they also make unboxing NPEs possible in callers.
