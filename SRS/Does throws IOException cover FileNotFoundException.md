<!--
reps: 0
priority: 0
-->
#Java/Exceptions/Checked #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Dumps: yes. FileNotFoundException extends IOException, so a method that throws FileNotFoundException may declare throws IOException. Callers then catch or declare IOException.

The reverse is false: throws FileNotFoundException does not cover a thrown IOException.
> [!warning] Unverified traps from the dump
> - If both types appear as catch parameters, FileNotFoundException must come before IOException or the child catch is unreachable.
