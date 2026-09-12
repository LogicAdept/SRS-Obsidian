<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# How do you use a bottom-up OSI approach when troubleshooting

> [!abstract] Short answer
> Bottom-up troubleshooting starts at Layer 1 and climbs only after the layer below is proven healthy: first the link and medium (cable, NIC lights, autonegotiation), then MAC/L2 reachability, then IP and routing, then transport ports, then the application protocol itself. Each green light narrows the search space, so you never debug DNS on a machine whose interface is down.

## The climb, with its quickest probes

1. **Physical:** link LEDs, cable swap, `ethtool`/`ip link` — is the interface UP with expected speed/duplex? Wi-Fi: signal, band.
2. **Data Link:** can it see neighbors? ARP table (`ip neigh`) has entries; VLANs correct; switch port shows the MAC.
3. **Network:** is there an address and a default route (`ip addr`, `ip route`)? Can you `ping` the gateway, then an external IP (8.8.8.8)? TTL and `traceroute` localize where paths break.
4. **Transport:** is the port reachable? `nc -vz host 443`, `telnet`; TCP SYN sent but no SYN-ACK usually means firewall, not routing.
5. **Application/Session:** DNS resolves (`dig`, `getent hosts`), TLS completes (`openssl s_client`), then the actual protocol — HTTP status, timeouts, 5xx.

```d2
direction: down
l1: "L1 link up?" { width: 180; height: 60; style.fill: "#e3f2fd" }
l2: "L2 neighbors (ARP)?" { width: 220; height: 60; style.fill: "#e3f2fd" }
l3: "L3 address, route, ping?" { width: 250; height: 60; style.fill: "#fff3e0" }
l4: "L4 port open?" { width: 200; height: 60; style.fill: "#fff3e0" }
l7: "L7 DNS/TLS/HTTP fine?" { width: 230; height: 60; style.fill: "#e8f5e9" }
stop: "Fix found at the failing layer" { width: 280; height: 60; style.fill: "#ffebee" }
l1 -> l2 -> l3 -> l4 -> l7
l1 -> stop: "no"
l2 -> stop: "no"
l3 -> stop: "no"
l4 -> stop: "no"
l7 -> stop: "no"
```

**Fig. 1.** Each layer is checked only after the previous one passes; the first failing layer is the fix location.

## When to flip the direction

Bottom-up shines on "cannot reach anything" incidents. The reverse (top-down) fits "one page is slow but the network is fine": start with the application/DNS/TLS, descend only if those pass. Experienced engineers mix both from the symptom: intermittent Wi-Fi drops smell like L1/L2; "resolves at work but not at the café" smells like L3/DNS config.

> [!warning] Do not skip layers you "trust"
> The classic time sink: debugging nginx config for an hour while the server NIC was flapping. If you did not personally verify the lower layer in this incident, verify it — a single command is cheaper than an hour of wrong-layer spelunking. Symmetric trap: stopping at the first symptom ("ping works, so the network is fine") when ICMP is allowed but TCP 443 is firewalled — that is an L4 failure below an L7 symptom ([[At which OSI layer does a router primarily operate]] vs [[At which OSI layer does a switch primarily operate]] are the hardware analogues of this layer discipline).

Related method cards: [[What is the OSI model]] for the layer ladder, [[How does ARP relate to the OSI layers]] for the L2/L3 boundary that bottom-up checks often trip on.

> [!tip] Interview answer
> Bottom-up means proving each layer before the next: link and autonegotiation, ARP and switching, IP address/route/ping to gateway and beyond, then TCP ports with nc, then DNS, TLS and the application protocol. The first failing layer is where the fix lives. I mention I flip to top-down for app-only symptoms — the point is the discipline of not debugging a layer above an unverified one.
