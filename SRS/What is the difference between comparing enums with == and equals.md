<!--
reps: 0
priority: 0
-->
#Java/Language/Enum #Java/HashCodeEquals #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: enum constants are unique instances, so `==` is allowed and often preferred.

- `==` does not throw NPE on a null left operand (`s1 == s3` is false).
- `equals` on a null reference throws NPE.
- `==` of two different enum types is a compile error.
- `equals` of two different enum types compiles and returns false.
- `compareTo` / `==` across two enum types do not compile.

Because constants are `final` instances, dumps also say `==` is a safe equality check.

`equals` on `Enum` is described as `final` and identity-based (`super.equals`).

> [!warning] Unverified traps from the dump
> - The filled vault card [[When should you override equals in Java]] already says enum `equals` is `final`.
