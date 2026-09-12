<!--
reps: 0
priority: 0
-->
#Networking #SRS
# What is ARP and how does it work

> [!abstract] Short answer
> ARP (Address Resolution Protocol, RFC 826) resolves an IPv4 address of a neighbor on the same link into a MAC address: the requester broadcasts "who has 10.0.0.7?", the owner unicasts back its MAC, both cache the pair in the ARP/neighbor table. Every IPv4 frame delivery on a LAN starts from this mapping — IP chose the destination, but Ethernet can only address MACs.

## The mechanics

1. **Need:** the IP stack wants to send to `10.0.0.7`; the routing decision says "on-link"; the neighbor cache has no entry.
2. **Request (broadcast):** an ARP request frame — dst MAC `ff:ff:ff:ff:ff:ff`, EtherType `0x0806` — asks "Who has 10.0.0.7? Tell 10.0.0.5", including the sender's own IP+MAC so everyone can pre-cache them.
3. **Reply (unicast):** the host owning `10.0.0.7` answers with its MAC directly to the requester.
4. **Cache:** both sides store the pair. Linux keeps a stateful neighbor table (REACHABLE → STALE → DELAY → PROBE states, not a single TTL); macOS uses a flat expiry. Stale entries get re-verified before use.

```d2
direction: right
a: "Host A (10.0.0.5)\nmiss in ARP cache" { width: 250; height: 80; style.fill: "#e3f2fd" }
req: "Request: broadcast\n'who has 10.0.0.7?'" { width: 260; height: 80; style.fill: "#fff3e0" }
b: "Host B (10.0.0.7)\nreply unicast: 'me, 9c:b6:..'" { width: 270; height: 90; style.fill: "#e8f5e9" }
a -> req -> b
b -> a: "reply"
```

**Fig. 1.** One broadcast question, one unicast answer, cached on both ends — and by eavesdroppers too, since the request carries the sender's mapping.

## Where ARP is used and where it is not

- **On-link only.** For an off-subnet destination, the host ARP-resolves *its default gateway* and ships the packet to the gateway's MAC — ARP never resolves remote addresses ([[What is the job of the Network layer under the OSI model]] shows the hop-by-hop rewriting).
- **Gratuitous ARP:** an unsolicited announcement ("I am 10.0.0.7 at this MAC") used after failover — this is exactly how VRRP-style mechanisms ([[What is VRRP]]) and NIC-team moves re-map traffic.
- **IPv6 replaced ARP with NDP** (Neighbor Discovery over ICMPv6), with the same purpose plus router discovery and duplicate address detection.

> [!warning] ARP has no authentication — that is the security story
> Anyone can answer an ARP request, and anyone can broadcast unsolicited replies: **ARP spoofing/poisoning** associates your IP with the attacker's MAC to intercept traffic (mitigate with dynamic ARP inspection, static entries where feasible, or 802.1X access control). Also, a flood of bogus entries can exhaust small ARP caches. And the classic wrong answer: "ARP resolves domain names" — that is DNS ([[What is DNS and how does DNS resolution work]]); ARP resolves IPv4 to MAC on one link, full stop.

Wire-level view: [[What does a Layer 2 broadcast look like in a packet capture]]; layer placement discussion: [[How does ARP relate to the OSI layers]]; address-family contrast: [[What is the difference between a MAC address and an IP address]].

> [!tip] Interview answer
> ARP maps on-link IPv4 addresses to MACs: broadcast request, unicast reply, neighbor-cache storage with staleness states. Key boundaries: it never crosses routers — you resolve the gateway for remote traffic; gratuitous ARP re-maps after failover; IPv6 uses NDP instead. I finish with the security note: unauthenticated ARP enables spoofing, which switches mitigate with dynamic ARP inspection.
