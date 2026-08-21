<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

ARP maps a known IP address to a MAC address on the local network so a host can build a Layer 2 frame for a Layer 3 next hop. Interview dumps place ARP at the Layer 2/3 boundary: it serves Network-layer delivery using Data-Link addressing.
> [!warning] Unverified traps from the dump
> - ARP is not DNS; DNS maps names to IPs at the Application layer in OSI teaching.
> - Strict layer purists argue about ARP's layer; exam answers usually accept Layer 2/3 boundary wording.
