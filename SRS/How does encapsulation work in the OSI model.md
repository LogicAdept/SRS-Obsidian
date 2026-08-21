<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

On the sending host, as data moves down the OSI stack, each layer wraps the PDU from the layer above with its own header (and sometimes trailer), producing a new PDU for the layer below. That wrapping is encapsulation. Example teaching chain: application data → transport segment → network packet → data-link frame → physical bits.
> [!warning] Unverified traps from the dump
> - Encapsulation is not fragmentation or MTU handling by itself; dumps sometimes conflate them.
> - Not every layer always adds a visible header in every capture (depends on protocol and tooling).
