<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# How does de-encapsulation work in the OSI model

> [!abstract] Short answer
> De-encapsulation is the receiver's upward walk: as the data rises from Physical to Application, each layer consumes and strips the header its peer added on the sender — NIC and driver drop the Ethernet header/trailer after checking the FCS, the IP layer validates and removes the IP header, TCP reassembles the stream from segments, and the application finally receives the bytes it can parse.

## The upward steps, in strict order

1. **Physical (1):** the receiver recovers bits from the signal and hands up a frame.
2. **Data Link (2):** the NIC checks the FCS (bad frames are dropped silently), reads destination MAC (is it mine / broadcast / promiscuous?), then strips the Ethernet header and trailer; the EtherType field says who gets the payload (e.g. `0x0800` → IPv4).
3. **Network (3):** the IP layer checks version, header checksum (IPv4), TTL > 0, matches the destination address to the host, and reads Protocol (6 = TCP, 17 = UDP) to demultiplex upward.
4. **Transport (4):** the port number selects the socket; TCP uses sequence numbers to reorder, filter duplicates, and acknowledge; data waits in the receive buffer until the application reads it.
5. **Session (5)–Presentation (6)–Application (7):** TLS decrypts/verifies (if present), the application parses the message — HTTP request, DNS answer, etc.

```d2
direction: down
bits: "bits from the wire" { width: 220; height: 60; style.fill: "#ffebee" }
d: "L2: check FCS, read dst MAC ->\nstrip Ethernet header/trailer" { width: 340; height: 90; style.fill: "#e3f2fd" }
n: "L3: check dst IP, TTL ->\nstrip IP header" { width: 340; height: 90; style.fill: "#fff3e0" }
t: "L4: port -> socket,\nreorder/ACK by seq -> strip TCP header" { width: 360; height: 100; style.fill: "#fff3e0" }
app: "Application parses the message" { width: 300; height: 70; style.fill: "#e8f5e9" }
bits -> d -> n -> t -> app
```

**Fig. 1.** Headers are consumed strictly in reverse of the sending order; the EtherType and Protocol fields are the dispatch keys between layers.

> [!warning] Demultiplexing has fixed checkpoints
> The order is not negotiable: EtherType decides L2→L3 dispatch, IP Protocol decides L3→L4, port decides L4→socket. A NIC cannot "see" ports, and TCP cannot dispatch by URL — the URL exists only after the application parses the payload. Interviewees who claim "the switch can route by port number" have missed exactly this chain ([[At which OSI layer does a switch primarily operate]]).

The mirror process is [[How does encapsulation work in the OSI model]]; the unit at each level is in [[What PDU is associated with each OSI layer]], and where the bytes go next is [[What is the function of the OSI Application layer]].

> [!tip] Interview answer
> De-encapsulation is the receiver peeling headers bottom-up: FCS check and MAC handling at L2, IP validation and Protocol dispatch at L3, port-to-socket demultiplexing plus reordering/ACKs at L4, then TLS and the application. The dispatch fields — EtherType, IP Protocol, port — are the clean way to answer "how does each layer know who hands it the payload".
