<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `NumberFormatException` is the unchecked exception when converting a string to a number fails because the text has the wrong format, e.g. `Integer.parseInt("abc")`. It shows up in lists of common runtime exceptions next to NPE and `ArithmeticException`.
> [!warning] Unverified traps from the dump
> - NumberFormatException extends IllegalArgumentException, so catch (IllegalArgumentException e) also matches a parse failure.
> - parseInt vs valueOf both throw it on bad text; they differ in return type (int vs Integer), not in the exception.
