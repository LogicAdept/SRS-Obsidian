<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# How does ARP relate to the OSI layers

> [!abstract] Short answer
> ARP (Address Resolution Protocol, RFC 826) is the glue between Layer 3 and Layer 2: it answers "which MAC address has this IPv4 address on this link?" so that IP packets can actually be delivered inside frames. It is not a layer-3 routing protocol and not pure layer 2 either — it straddles the boundary, which is why its placement is a classic interview discussion.

## What ARP does, step by step

1. The IP stack has a packet for `10.0.0.7` on the local subnet (same prefix — otherwise it goes to the gateway instead) but no cache entry for its MAC.
2. The host broadcasts an **ARP request** to `ff:ff:ff:ff:ff:ff`: "Who has 10.0.0.7? Tell 10.0.0.5."
3. Every host on the link receives the broadcast; the owner replies **unicast**: "10.0.0.7 is at 9c:b6:d0:11:22:33."
4. Both sides cache the pair (the requester and even eavesdroppers update their ARP caches) with a timeout (Linux uses a stateful neighbor table with reachable/failed states rather than a single flat TTL).

```d2
direction: right
a: "Host A\nneeds MAC of 10.0.0.7" { width: 250; height: 80; style.fill: "#e3f2fd" }
bc: "ARP request\nbroadcast ff:ff:ff:ff:ff:ff\n'Who has 10.0.0.7?'" { width: 300; height: 100; style.fill: "#fff3e0" }
b: "Host B (10.0.0.7)\nARP reply unicast\n'MAC is 9c:b6:...'" { width: 280; height: 100; style.fill: "#e8f5e9" }
a -> bc
bc -> b
b -> a: "reply"
```

**Fig. 1.** Broadcast question, unicast answer; both hosts cache the result to avoid repeating the dance per packet.

## Layer placement — the honest answer

- **Functionally it serves Layer 2 delivery:** the output is a MAC address used to build the frame.
- **Informationally it speaks about Layer 3:** its payloads are IPv4 addresses, and it runs *because* IP needs neighbor mapping.
- **In Ethernet terms it rides as its own EtherType** (`0x0806`), not inside IP — so it is not "an IP protocol" either. Textbooks place it "between L2 and L3"; RFC 826 predates the tidy mapping and simply fills the gap.

> [!warning] ARP only resolves on-link addresses
> ARP never crosses a router: a host ARP-resolves *the gateway's* MAC for any off-subnet destination, never the remote server's. Claiming "ARP resolves the MAC of google.com" mixes up DNS with ARP — name resolution across the Internet is DNS ([[What is DNS and how does DNS resolution work]]). Also note IPv6 replaced ARP with NDP (ICMPv6 Neighbor Discovery); ARP is IPv4 machinery.

Deeper: [[What is the difference between a MAC address and an IP address]] for why the two address families exist at all, [[What does a Layer 2 broadcast look like in a packet capture]] for the wire view, and [[At which OSI layer does a switch primarily operate]] for how switches treat the broadcast frame.

> [!tip] Interview answer
> ARP maps an on-link IPv4 address to a MAC: broadcast request, unicast reply, cached in the neighbor table. Its placement: it serves layer-2 delivery but speaks layer-3 addresses and has its own EtherType, so it sits between the layers. The two facts that impress: it never crosses routers — you ARP the gateway, not the destination — and IPv6 uses ICMPv6 NDP instead.
