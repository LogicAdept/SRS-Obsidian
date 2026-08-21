<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Unchecked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: `ArrayIndexOutOfBoundsException` is an unchecked exception when an array is accessed with an illegal index — negative, or greater than or equal to the length. Interview example: `int[] list = new int[4]; list[4]` throws (valid indexes are 0..3).
> [!warning] Unverified traps from the dump
> - A new int[4] is filled with zeros; the failure is the index, not an uninitialized slot.
> - It is a subclass of IndexOutOfBoundsException, not a sibling of RuntimeException.
