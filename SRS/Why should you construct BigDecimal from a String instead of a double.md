<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`float` and `double` cannot represent some decimals (like `0.1`) exactly. Dumps say: for money or exact decimals, use `BigDecimal` and construct it from a `String`, not a `double`:

```java
new BigDecimal("0.1").add(new BigDecimal("0.2")); // 0.3 exactly
```

Constructing from a `double` would bake in the already-rounded binary value.

> [!warning] Unverified traps from the dump
> - `new BigDecimal(0.1)` follows the `double` approximation, not the decimal `0.1`.
