<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: from Java 14, helpful NPE messages can name the exact expression that was null, for example `Cannot invoke "String.length()" because "s" is null`, instead of a bare `NullPointerException` with no clue which dereference failed.
> [!warning] Unverified traps from the dump
> - The extra detail is a JVM message feature; it does not change when NPE is thrown.
> - Deserialized NullPointerException objects may lack the verbose reconstructed message.
