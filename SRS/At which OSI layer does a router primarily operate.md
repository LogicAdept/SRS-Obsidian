<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# At which OSI layer does a router primarily operate

> [!abstract] Short answer
> A router primarily operates at Layer 3 (Network): it reads the destination IP address of each packet, looks up the longest-prefix match in its routing table and forwards the packet toward the next hop, re-encapsulating it into a new layer-2 frame for the outgoing link.

## Why it is Layer 3

1. **Decision input is the IP header.** A router does not need the payload or transport headers — destination IP plus its own routing table is enough to decide.
2. **It crosses network boundaries.** Switches forward inside one LAN; routers connect distinct IP subnets, which is exactly the Network layer's job.
3. **It participates in the routing control plane.** OSPF, BGP or static routes build the table — all layer-3 concepts.
4. **Hop-by-hop behavior.** Each router decrements TTL (IPv4) or Hop Limit (IPv6) and rewrites the frame addresses: MACs change on every hop, IP addresses stay end-to-end (unless NAT intervenes — [[What is NAT and how does it work]]).

```d2
direction: right
in: "Packet in a frame\nfrom interface eth0" { width: 250; height: 80; style.fill: "#e3f2fd" }
lu: "Routing table\nlongest-prefix match\non destination IP" { width: 280; height: 100; style.fill: "#fff3e0" }
out: "Same packet\nin a NEW frame\n(new src/dst MAC, TTL-1)" { width: 280; height: 100; style.fill: "#e8f5e9" }
in -> lu -> out
```

**Fig. 1.** The router strips the incoming frame, inspects the IP packet, and builds a fresh frame for the next link — the packet (layer-3 PDU) survives, the frame does not.

## What routers do beyond pure L3

Real routers also act as hosts for management (SNMP, SSH) and support layer-2 functions on their interfaces. "Primarily" in the question covers this: a home Wi-Fi router is actually a router + switch + AP + NAT device. An L3 switch is a switch with routing ASICs, so "switch vs router" is about the primary forwarding function, not the chassis.

> [!warning] A router is not a firewall and does not read URLs
> A plain router forwards by IP prefix — it does not terminate TLS, read host headers, or balance by path; those are L7 proxy duties ([[What is the difference between L3 L4 and L7]]). Another classic trap: "routers work with frames" — they *emit* frames, but decide on packets; the frame is disposable, rebuilt per hop.

Compare with the Layer 2 device: [[At which OSI layer does a switch primarily operate]], the Layer 1 device: [[At which OSI layer does a hub operate]], and the layer's own description in [[What is the job of the Network layer under the OSI model]].

> [!tip] Interview answer
> Router — Layer 3. It makes forwarding decisions on destination IP with longest-prefix match, decrements TTL, and re-encapsulates the packet into a new frame per hop, which is why MAC addresses change hop by hop while IPs persist end to end. I add the caveat that a home "router" is a multi-function box (router + switch + NAT + AP), but its routing function is squarely Network layer.
