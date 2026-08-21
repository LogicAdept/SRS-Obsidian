<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps (polymorphism): an override must not declare checked exceptions that a caller using the superclass type is not already forced to handle.

- Parent declares no checked throws: the override cannot declare a checked exception. It may declare unchecked types (IllegalArgumentException, ArithmeticException).
- Parent declares checked throws: the override may declare the same types, subtypes (IOException to FileNotFoundException, SocketException, or EOFException), a subset, or none.
- Extra unchecked throws on the override are allowed even when the parent listed none.
> [!warning] Unverified traps from the dump
> - Order of types in throws does not matter.
> - A Super ref still forces callers to handle Super's checked throws even if the runtime override declares none.
