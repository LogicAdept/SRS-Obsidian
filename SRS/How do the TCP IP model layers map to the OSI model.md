<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Common four-layer TCP/IP mapping:

- Network Interface / Link → OSI Physical + Data Link
- Internet → OSI Network
- Transport → OSI Transport
- Application → OSI Session + Presentation + Application

Do not map TCP/IP Network Interface to Network + Data Link + Physical; Internet alone maps to OSI Network.
> [!warning] Unverified traps from the dump
> - Vendor slides disagree on Link vs Network Access naming and on 4 vs 5 layer TCP/IP diagrams.
