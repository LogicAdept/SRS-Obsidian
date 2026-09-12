<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What does a Layer 2 broadcast look like in a packet capture

> [!abstract] Short answer
> In a capture, a Layer 2 broadcast is an Ethernet frame whose destination MAC is all ones — `ff:ff:ff:ff:ff:ff` — so every station on the link (or VLAN) accepts and processes it. The most common real example is an ARP request: dst `ff:ff:ff:ff:ff:ff`, EtherType `0x0806`, with the question "who has 10.0.0.7?" in its payload.

## Reading it in Wireshark

```text
Frame 12: 42 bytes on wire
Ethernet II:
    Destination: Broadcast (ff:ff:ff:ff:ff:ff)
    Source: Apple_11:22:33 (9c:b6:d0:11:22:33)
    Type: ARP (0x0806)
Address Resolution Protocol:
    Opcode: request (1)
    Sender MAC: 9c:b6:d0:11:22:33   Sender IP: 10.0.0.5
    Target MAC: 00:00:00:00:00:00   Target IP: 10.0.0.7
```

**Listing 1.** A textbook ARP request: broadcast at L2, question about an IPv4 address, unknown target MAC left as zeros.

How to interpret each part:

1. **Destination `ff:ff:ff:ff:ff:ff`** — the layer-2 broadcast address. Switches flood it to all ports of the VLAN; NICs pass it up because it matches their broadcast accept filter.
2. **EtherType `0x0806`** — the payload is ARP, not IP (`0x0800`). This is the dispatch key [[How does ARP relate to the OSI layers]] talks about.
3. **Unicast reply follows** — the ARP answer comes back only to the requester's MAC, so captures show one broadcast + one unicast per resolution.

Other everyday L2 broadcasts: DHCP `DHCPDISCOVER` (broadcast because the client has no address yet — [[What is DHCP and how does it work]]), mDNS/LLMNR name queries on Windows/macOS LANs, and periodic announcements (e.g. VRRP advertisements are *multicast* `224.0.0.18`, the directed-group cousin of broadcast).

```d2
direction: right
src: "Sender\nframe dst = ff:ff:..." { width: 250; height: 80; style.fill: "#e3f2fd" }
sw: "Switch\nflood to all VLAN ports" { width: 260; height: 90; style.fill: "#fff3e0" }
p1: "Host 1 accepts\n(processes ARP)" { width: 220; height: 80; style.fill: "#e8f5e9" }
p2: "Host 2 accepts\nthen drops (not me)" { width: 220; height: 80; style.fill: "#e8f5e9" }
src -> sw
sw -> p1
sw -> p2
```

**Fig. 1.** Everyone receives; only the relevant peer keeps it. Broadcasts stop at router interfaces — one broadcast domain per subnet/VLAN.

> [!warning] Broadcast is not multicast, and "everyone" means the broadcast domain
> Multicast frames use reserved MACs (e.g. `01:00:5e:...` for IPv4 multicast) and reach only group members that subscribed; broadcast reaches *everyone in the L2 domain*. A router (or VLAN boundary) is what stops both — an internetwork-wide "broadcast" does not exist. Wi-Fi broadcasts are airtime-hungry because every radio must wake and process them, which is why broadcast storms and chatty mDNS are real performance problems.

Related: [[What is a frame at the Data Link layer]] for the frame anatomy, [[At which OSI layer does a switch primarily operate]] for flooding behavior, and [[What is VRRP]] for a protocol that deliberately uses multicast instead.

> [!tip] Interview answer
> A Layer 2 broadcast is a frame with dst MAC ff:ff:ff:ff:ff:ff — switches flood it within the VLAN and every NIC accepts it. The canonical capture is an ARP request: EtherType 0x0806, sender's IP/MAC filled, target MAC zeros. DHCPDISCOVER is the other classic. I contrast it with multicast (group MACs, subscribers only) and note routers are the broadcast boundary.
