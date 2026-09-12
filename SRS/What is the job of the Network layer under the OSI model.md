<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is the job of the Network layer under the OSI model

> [!abstract] Short answer
> The Network layer (Layer 3) delivers packets from a source host to a destination host across multiple, possibly dissimilar links. It does that with logical addressing (IP addresses), routing (choosing next hops), forwarding (moving packets through routers), and packetization (MTU-aware fragmentation in IPv4, forbidden in IPv6). Best effort by default — no guarantees of delivery, order or duplication-freedom.

## Responsibilities in detail

1. **Logical addressing.** IP gives every interface a hierarchical address independent of the physical NIC (a MAC address follows hardware; an IP follows the network the host is attached to — [[What is the difference between a MAC address and an IP address]]).
2. **Routing.** Routers run protocols (OSPF, BGP) to build the path knowledge, then make a per-packet next-hop decision on the destination address (RFC 1812 specifies the router's job).
3. **Forwarding across heterogeneous links.** A packet may travel Ethernet → fiber → radio; layer 3 hides that, because each hop re-encapsulates the packet into a fresh frame for the next link.
4. **Fragmentation and MTU.** IPv4 routers may fragment packets that exceed the next link's MTU; IPv6 dropped in-flight fragmentation — the sender must discover the path MTU.
5. **Control plane.** ICMP reports errors and diagnostics (echo/reply for ping, TTL exceeded for traceroute).

```d2
direction: right
h1: "Host A\nIP: 10.1.0.5" { width: 200; height: 90; style.fill: "#e8f5e9" }
r1: "Router 1\nreads dst IP -> next hop" { width: 240; height: 100; style.fill: "#fff3e0" }
r2: "Router 2\nreads dst IP -> next hop" { width: 240; height: 100; style.fill: "#fff3e0" }
h2: "Host B\nIP: 10.4.0.9" { width: 200; height: 90; style.fill: "#e8f5e9" }
h1 -> r1: "frame (LAN 1)"
r1 -> r2: "frame (link 2, new MACs)"
r2 -> h2: "frame (LAN 3)"
```

**Fig. 1.** IP addresses stay end-to-end (modulo NAT) while MAC addresses are rewritten on every hop — the visual proof of what "network layer" means.

> [!warning] The Network layer is not the Transport layer
> Layer 3 gets a packet *to the destination host*; it knows nothing about processes or ports. Choosing the socket (ports), reliability and ordering are layer-4 duties — [[What is a segment at the Transport layer]] and [[Which OSI layer provides end-to-end delivery flow control and error recovery]] cover that boundary. Another popular mix-up: "routers route, switches switch" is true, but L3 switches do both — see [[At which OSI layer does a router primarily operate]] and [[At which OSI layer does a switch primarily operate]].

On the real Internet IP *is* the network layer — [[What is the TCP IP protocol suite]] shows how it fits, and [[What PDU is associated with each OSI layer]] names its unit, the packet.

> [!tip] Interview answer
> Layer 3 moves packets host-to-host across many links: logical IP addressing, routing decisions in routers, per-hop re-encapsulation, MTU handling — IPv4 can fragment in flight, IPv6 forces path MTU discovery. It is best-effort: no delivery or ordering promises — reliability is layer 4. And the classic proof of layering: MACs change every hop, IPs persist end to end except when NAT rewrites them.
