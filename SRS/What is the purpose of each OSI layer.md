<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is the purpose of each OSI layer

> [!abstract] Short answer
> Each layer answers one delivery question: Physical — how to put a bit on a medium; Data Link — how to deliver a frame to the neighbor on this link; Network — how to route a packet across many links to a host; Transport — how to deliver to the right process on that host, reliably or fast; Session — how to organize a dialog; Presentation — how the bytes are represented; Application — what the software actually asks for.

## One job per layer, with the protocol that does it

1. **Physical (1):** transmit raw bits over copper, fiber or air — signal levels, line codes, connectors, timing. Ethernet PHY, RS-232, optical transceivers.
2. **Data Link (2):** frame the bits, address neighbors by MAC, detect bit errors (32-bit FCS checksum in the Ethernet trailer), arbitrate access to the medium; switches forward frames inside one LAN. Ethernet/802.3, ARP effectively works at this boundary.
3. **Network (3):** logical addressing and end-to-end path: IP gives each interface an address, routers forward packets hop by hop, ICMP reports problems, fragmentation deals with MTU. RFC 1812 defines the router's role.
4. **Transport (4):** process-to-process delivery: port numbers multiplex applications on one host; TCP adds ordering, retransmission, flow and congestion control; UDP adds only ports and a checksum.
5. **Session (5):** establish, manage and end dialogs, synchronize long transfers, recover from interruptions — in practice absorbed by TLS sessions and application-level session ids.
6. **Presentation (6):** common representation: character encodings (UTF-8), media formats (JPEG, MPEG), serialization, and message-level encryption/decryption.
7. **Application (7):** the semantics of what you do: fetch pages (HTTP), resolve names (DNS), lease an address (DHCP), move mail (SMTP).

```d2
direction: down
q: "Data the app wants to send" { width: 300; height: 70; style.fill: "#e8f5e9" }
r: "6 Presentation: agree on bytes\nencode / encrypt" { width: 320; height: 80; style.fill: "#e8f5e9" }
s: "5 Session: structure the dialog" { width: 320; height: 70; style.fill: "#e8f5e9" }
t: "4 Transport: deliver to process\nports, reliability" { width: 320; height: 90; style.fill: "#fff3e0" }
n: "3 Network: deliver to host\nIP, routing" { width: 320; height: 80; style.fill: "#fff3e0" }
d: "2 Data Link: deliver to neighbor\nMAC, frame check" { width: 320; height: 80; style.fill: "#e3f2fd" }
p: "1 Physical: put bits on the medium" { width: 320; height: 70; style.fill: "#e3f2fd" }
q -> r -> s -> t -> n -> d -> p
```

**Fig. 1.** The chain of delivery questions as data descends the stack on the sender.

> [!warning] Layers 5 and 6 look redundant on the Internet
> A truthful answer admits that TCP/IP has no dedicated session or presentation protocols; their jobs live in application code, serialization formats and TLS. Naming the purpose still matters because interviews test whether you know *what problem each layer solves*, not whether a box in Wireshark has that label.

Cross-checks: [[What PDU is associated with each OSI layer]] for the data-unit per layer, [[What is the job of the Network layer under the OSI model]] and [[What is a segment at the Transport layer]] for the two layers interviews drill hardest.

> [!tip] Interview answer
> I walk down the stack naming one purpose each: signals (1), neighbor delivery with MAC and error detection (2), host-to-host routing with IP (3), process-to-process delivery with ports plus TCP reliability or UDP speed (4), dialog management (5), common data representation (6), and application semantics (7). I then note that on real TCP/IP stacks layers 5–6 are absorbed by apps and TLS — showing I know the model and its limits.
