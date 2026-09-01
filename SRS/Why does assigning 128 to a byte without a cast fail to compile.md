<!--
reps: 0
priority: 0
-->
#Java/Language/Primitives #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

A dump puzzle: `byte large = 128;` does not compile because 128 is an `int` literal outside the `byte` range (-128 to 127). `byte large = (byte) 128;` compiles and truncates (wraps to -128).

A literal that is in range, such as `byte b = 5;`, is accepted with an implicit narrowing of the `int` constant.
> [!warning] Unverified traps from the dump
> - The compile-time range check applies to constant int literals assigned to byte, short, or char.
> - A non-constant int always needs an explicit cast, even if the runtime value would fit.
