<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

On the receiving host, headers are removed starting at the bottom of the stack: Physical → Data Link → Network → Transport → Application (with Session/Presentation folded into Application in TCP/IP teaching).
> [!warning] Unverified traps from the dump
> - Choosing Application-first order describes send-side thinking, not receive-side de-encapsulation.
