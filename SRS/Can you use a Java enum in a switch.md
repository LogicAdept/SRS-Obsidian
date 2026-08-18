<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Yes. Compilations call this a main advantage: constants are compile-time constants, so they are legal `case` labels.

```java
Currency usCoin = Currency.DIME;
switch (usCoin) {
    case PENNY: System.out.println("Penny coin"); break;
    case NICKLE: System.out.println("Nickle coin"); break;
}
```

A dump notes that from JDK 7 you can also `switch` on `String`.

> [!warning] Unverified traps from the dump
> - Constant-specific methods / interface implementations are offered as an alternative to a large `switch` on the enum.
