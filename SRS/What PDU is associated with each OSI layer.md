<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Teaching mnemonic for PDUs by layer:

- Application / Presentation / Session: data (or message)
- Transport: segment (TCP) or datagram (UDP) — dumps often say segment
- Network: packet
- Data Link: frame
- Physical: bit

Memorize: bits → frames → packets → segments → data.
> [!warning] Unverified traps from the dump
> - UDP units are often called datagrams, not segments; dumps still say segment for Layer 4.
> - Some texts call Network-layer units datagrams interchangeably with packets.
