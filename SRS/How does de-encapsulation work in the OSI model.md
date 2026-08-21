<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

On the receiving host, headers (and trailers) are removed from the bottom up as data moves up the stack: Physical → Data Link → Network → Transport → (Session/Presentation) → Application. Each layer strips its own PDU framing and passes the payload upward. Interview dumps call this de-encapsulation.
> [!warning] Unverified traps from the dump
> - Order on receive is bottom-up; confusing it with send-side top-down order is a common exam trap.
