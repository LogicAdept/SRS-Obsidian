<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: for a forbidden null argument, the usual JDK convention is `NullPointerException`, often via `Objects.requireNonNull`. Some lists still throw `IllegalArgumentException` for any bad argument including null. Interview answers that follow Effective Java / JDK style pick NPE for null and IAE for other illegal values.
> [!warning] Unverified traps from the dump
> - Objects.requireNonNull always throws NullPointerException, never IllegalArgumentException.
> - Using IAE for null is not illegal; it just diverges from the JDK parameter-validation idiom.
