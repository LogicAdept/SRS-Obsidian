<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

Many Network+ style dumps map encryption and decryption to the Presentation layer (Layer 6), so HTTPS in-transit encryption is answered as Layer 6. Separately they still call HTTPS an Application-layer protocol. Treat this as exam taxonomy, then verify against how TLS actually sits relative to HTTP in real stacks.
> [!warning] Unverified traps from the dump
> - Popular lie / oversimplification: Presentation owns all crypto; in practice TLS is negotiated around the application protocol and is not a pure Layer-6 module.
> - Some materials answer HTTPS as Layer 7 only — know which curriculum you are being tested on.
