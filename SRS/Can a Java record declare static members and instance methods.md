<!--
reps: 0
priority: 0
-->
#Java/Language/Records #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. Records may have static fields, static methods, instance methods, and private methods. They may not have extra non-static instance fields beyond the header components.

```java
record Temperature(double celsius) {
    static final double ABSOLUTE_ZERO = -273.15;

    static Temperature ofFahrenheit(double f) {
        return new Temperature((f - 32) * 5.0 / 9.0);
    }

    double toFahrenheit() {
        return celsius * 9.0 / 5.0 + 32;
    }
}
```

Static members do not participate in `equals`, `hashCode`, `toString`, or the canonical constructor.

Dumps also allow nested records and static factories (`User.anonymous()`).

> [!warning] Unverified traps from the dump
> - Any extra instance field is a compile error, even `private` / `volatile` intended as a hash cache.
> - Mutable static state on a record is called out as an anti-pattern (thread-safety).
