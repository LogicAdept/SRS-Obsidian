<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Interview MCQs: `System.out.println(1/0)` throws `ArithmeticException`; `System.out.println(2.0/0)` prints `Infinity` and does not throw. Dumps treat `ArithmeticException` as an integer (`int`/`long`) condition, not IEEE-754 float/double division by zero.
> [!warning] Unverified traps from the dump
> - There is no DivideByZeroError in Java.
> - 0.0/0.0 is NaN, not ArithmeticException.
