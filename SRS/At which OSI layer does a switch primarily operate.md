<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# At which OSI layer does a switch primarily operate

> [!abstract] Short answer
> A switch primarily operates at Layer 2 (Data Link): it forwards Ethernet frames by looking at destination MAC addresses and maintains a MAC address table (CAM table) that maps each MAC to the port where it was last seen. It creates separate collision domains per port and keeps one broadcast domain.

## The forwarding loop

1. A frame arrives; the switch records its **source MAC → ingress port** in the CAM table (learning).
2. It looks up the **destination MAC**:
   - known → forward only out of that port;
   - unknown → flood out of all ports in the VLAN (except ingress);
   - broadcast/multicast → flood within the broadcast domain.
3. The frame's FCS (32-bit CRC) is checked — frames with errors are dropped; the switch does not fix them.

```d2
direction: right
a: "A sends to C\nsrc MAC A, dst MAC C" { width: 250; height: 80; style.fill: "#e3f2fd" }
sw: "Switch\nCAM: A->p1, B->p2, C->p3\nforward out p3 only" { width: 300; height: 110; style.fill: "#fff3e0" }
c: "C receives the frame" { width: 220; height: 70; style.fill: "#e8f5e9" }
b: "B does NOT receive it\n(no flooding)" { width: 240; height: 80; style.fill: "#ffebee" }
a -> sw
sw -> c
sw -> b: "nothing"
```

**Fig. 1.** Unicast forwarding is selective — this is the defining difference from a hub, which duplicates bits to every port ([[At which OSI layer does a hub operate]]).

## Layer-2 vs layer-3 switches

A plain switch never touches IP. An **L3 switch** additionally routes between VLANs with hardware speed — it is a switch (L2) with a router (L3) inside. VLANs themselves are a layer-2 construct (802.1Q tags) that segments broadcast domains while keeping MAC-level forwarding. ARP is the glue between the layers: IP asks "who has this IPv4?" and the answer populates the switch's MAC world ([[How does ARP relate to the OSI layers]]).

> [!warning] "Switches forward broadcasts to all ports" — only within one broadcast domain
> Broadcasts are flooded within the VLAN/broadcast domain, not "everywhere"; routers (or VLAN boundaries) stop them, which is why a broadcast storm stays local. And a MAC table entry ages out — moving a laptop between ports temporarily causes flooding until re-learning. Saying "the switch learns IPs" confuses it with ARP caches — the CAM table maps **MACs**, not IPs.

Cross-views: the function-focused formulation of the same fact lives in [[How does ARP relate to the OSI layers]]; layer context in [[What is a frame at the Data Link layer]], and the routing counterpart in [[At which OSI layer does a router primarily operate]].

> [!tip] Interview answer
> Switch — Layer 2: it learns source MACs into a CAM table and forwards frames by destination MAC, flooding only unknown unicast and broadcast inside the VLAN. FCS errors are dropped, each port is its own collision domain, and broadcast stays inside one broadcast domain. If it also routes between VLANs, it is an L3 switch — switch plus router on the same silicon.
