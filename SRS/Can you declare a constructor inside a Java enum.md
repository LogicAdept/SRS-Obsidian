<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. An enum may declare constructors, fields, and methods. The constructor must be `private` or package-private; `public` and `protected` constructors are not permitted.

```java
public enum Currency {
    PENNY(1), NICKLE(5), DIME(10), QUARTER(25);
    private final int value;
    private Currency(int value) { this.value = value; }
    public int getValue() { return value; }
}
```

`PENNY(1)` is a constructor call. A semicolon after the constant list is required once you add members.

> [!warning] Unverified traps from the dump
> - One dump says “any other access modifier than private is a compile error”; another allows package-private. Verify which the language actually permits.
