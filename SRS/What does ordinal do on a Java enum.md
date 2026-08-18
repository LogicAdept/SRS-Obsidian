<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

`ordinal()` returns the zero-based declaration index of the constant. `DayOfWeek.MONDAY.ordinal()` is 0 if `MONDAY` is listed first.

It is inherited from `java.lang.Enum`. The compiler is said to pass `name` and `ordinal` into the protected `Enum(String name, int ordinal)` constructor.

Compilations warn not to use ordinal in business logic: inserting or reordering constants changes the numbers.

> [!warning] Unverified traps from the dump
> - Default `compareTo` is described as following this same declaration order.
