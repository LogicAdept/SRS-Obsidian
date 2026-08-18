<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #Java/Language/Wrappers #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps show `xxxValue` instance methods as the explicit conversion from wrapper to primitive:

```java
Integer seven = Integer.valueOf(57);
int primitive = seven.intValue();
float primitiveFloat = seven.floatValue();

Float floatWrapper = Float.valueOf(57.0f);
int floatToInt = floatWrapper.intValue();
float floatToFloat = floatWrapper.floatValue();
```

Autounboxing (`int y = seven;`) is the implicit form of the same conversion.

> [!warning] Unverified traps from the dump
> - Calling `intValue()` on a `null` wrapper is `NullPointerException`, same as unboxing.
> - `floatValue()` on an `Integer` is a conversion, not a reinterpretation of bits.
