<!--
reps: 0
priority: 0
-->
#Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps show `Integer` static converters:

```java
Integer.toBinaryString(42);
Integer.toHexString(wrapperEight);   // example value 8 -> "8"
Integer.toOctalString(wrapperEight); // 8 -> "10"
Integer.toString(wrapperEight, 2);   // radix overload, 8 -> "1000"
```

Related utilities in the same lists: `Integer.MAX_VALUE`, `Character.isDigit('7')`.

> [!warning] Unverified traps from the dump
> - These methods take the numeric value, not a bit-pattern object.
> - `toString(value, radix)` is the general form; `toBinaryString` is radix 2.
