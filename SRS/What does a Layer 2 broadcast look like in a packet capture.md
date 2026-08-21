<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS #New

> [!warning] Untrusted draft
> Copied from an external question dump. Not checked against official documentation. Do not treat this as a review answer.

In Ethernet captures, a Layer 2 broadcast frame uses destination MAC `FF:FF:FF:FF:FF:FF`. It is relevant at the Data Link layer and is flooded within the broadcast domain (typically a VLAN/LAN segment).
> [!warning] Unverified traps from the dump
> - Do not confuse L2 broadcast MAC with L3 broadcast IP addresses; both can appear together in ARP/DHCP examples.
