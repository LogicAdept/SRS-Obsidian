<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: yes, under the same catch-or-specify rule as methods. A checked exception that leaves a constructor must appear in that constructor's throws. Callers of new C() must catch or declare those types.

If the constructor body calls a method that throws IOException, the constructor must catch it or declare throws IOException.
> [!warning] Unverified traps from the dump
> - A subclass constructor that calls super(...) must handle or declare checked exceptions the superclass constructor declares.
> - Declaring throws on a constructor is legal even when this particular body never throws; dumps treat it as API contract.
