<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`double` is a floating-point type, which means it is subject to precision errors in decimal calculations. `BigDecimal` is a class that provides arbitrary precision decimal arithmetic. Dumps say it is more suitable for financial and precise calculations where accuracy is crucial.

Related dump example: `0.1 + 0.2` is not exactly `0.3` with `double`, while `new BigDecimal("0.1").add(new BigDecimal("0.2"))` is exact.

> [!warning] Unverified traps from the dump
> - Do not build `BigDecimal` from a `double` if you need the decimal you typed; use a `String`.
> - `double` is a primitive; `BigDecimal` is an object with different operators (methods, not `+`).
