<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is a frame at the Data Link layer

> [!abstract] Short answer
> A frame is the Data Link (Layer 2) protocol data unit: the packet from above wrapped with a header carrying source and destination MAC addresses (plus a type/length field and optional VLAN tag) and a trailer with a checksum (FCS) used to detect corrupted frames. Frames are what actually flows on one physical link; their addresses are rewritten on every hop.

## Ethernet frame anatomy (802.3 / Ethernet II)

| Field | Size | Purpose |
|---|---|---|
| Preamble + SFD | 8 B | signal/clock alignment (often not counted as part of the frame) |
| Destination MAC | 6 B | where on this link; `ff:ff:ff:ff:ff:ff` = broadcast |
| Source MAC | 6 B | who sent it on this link |
| 802.1Q tag | 4 B (optional) | VLAN id + priority |
| EtherType | 2 B | payload protocol: `0x0800` IPv4, `0x86DD` IPv6, `0x0806` ARP |
| Payload | 46–1500 B (classic MTU) | usually an IP packet |
| FCS | 4 B | 32-bit CRC trailer — corrupted frames are dropped |

```d2
direction: right
pkt: "IP packet\n(layer 3 PDU)" { width: 200; height: 70; style.fill: "#fff3e0" }
hdr: "Frame header\ndst MAC | src MAC | EtherType" { width: 300; height: 90; style.fill: "#e3f2fd" }
fcs: "FCS trailer\nCRC-32" { width: 180; height: 70; style.fill: "#e8f5e9" }
hdr -> pkt -> fcs
```

**Fig. 1.** Encapsulation at Layer 2: header and trailer around the packet. The trailer exists only at this layer — checksums above (IP, TCP) live in headers.

## What makes frames special

- **Link-local validity.** MAC addresses make sense only on the current link; each router hop strips the old frame and builds a new one, so source/destination MACs change hop by hop while IP addresses persist end to end.
- **Size bounds.** Classic Ethernet MTU is 1500 bytes of payload; jumbo frames raise it (often 9000) only inside one LAN — never across the Internet. A link with a smaller MTU forces fragmentation or path MTU discovery above.
- **Error detection, not correction.** FCS detects bit corruption and the receiver drops bad frames silently; recovery belongs to upper layers (TCP retransmission) or specialized links.

> [!warning] A frame is not a packet
> The packet is the layer-3 PDU carried inside the frame. Saying "the router forwards the frame to another network" is wrong: the frame dies at the router; the packet continues in a new frame. [[What is a packet at the Network layer]] and [[What PDU is associated with each OSI layer]] pin this down.

Related: [[At which OSI layer does a switch primarily operate]] for the device that forwards frames, and [[What does a Layer 2 broadcast look like in a packet capture]] for the broadcast special case.

> [!tip] Interview answer
> A frame is the layer-2 PDU: header with destination/source MAC and EtherType, payload up to the MTU (1500 on classic Ethernet), and a CRC-32 FCS trailer for error detection. Key behaviors: frames live on one link only — MACs are rewritten per hop; corrupted frames are dropped, not repaired; and the packet inside is the layer-3 PDU, which is the level a router actually reads.
