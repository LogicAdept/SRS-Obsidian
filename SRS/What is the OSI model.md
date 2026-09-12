<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is the OSI model

> [!abstract] Short answer
> The OSI model (Open Systems Interconnection) is a 7-layer reference model for network communication, standardized as ISO/IEC 7498-1 and ITU-T X.200. It splits the path from bits on a wire to an application message into Application, Presentation, Session, Transport, Network, Data Link and Physical layers, each with a narrow responsibility and a service interface to the layer above — so heterogeneous vendors can interoperate and people can localize where a problem or a protocol lives.

## The seven layers top-down

1. **Application (7)** — the network interface of actual software: HTTP, FTP, DNS, DHCP, SMTP; produces the data the user cares about.
2. **Presentation (6)** — representation: character encodings, media formats, serialization, (conceptually) encryption/decryption — so both sides agree how bytes are interpreted.
3. **Session (5)** — dialog management: establishing, structuring and tearing down sessions, checkpointing long exchanges.
4. **Transport (4)** — end-to-end delivery between processes: TCP/UDP/QUIC, ports, segmentation, reliability, flow control.
5. **Network (3)** — routing between networks: IP addressing, forwarding, fragmentation; the domain of routers.
6. **Data Link (2)** — delivery between neighbors on one link: MAC addressing, framing, error detection (FCS); switches and bridges live here.
7. **Physical (1)** — electrical, optical and radio signaling, connectors, bit timing.

```d2
direction: down
a: "7 Application\nHTTP, DNS" { width: 260; height: 70; style.fill: "#e8f5e9" }
p: "6 Presentation\nencodings, formats" { width: 260; height: 70; style.fill: "#e8f5e9" }
s: "5 Session\ndialogs" { width: 260; height: 70; style.fill: "#e8f5e9" }
t: "4 Transport\nTCP, UDP, ports" { width: 260; height: 70; style.fill: "#fff3e0" }
n: "3 Network\nIP, routing" { width: 260; height: 70; style.fill: "#fff3e0" }
d: "2 Data Link\nMAC, frames" { width: 260; height: 70; style.fill: "#e3f2fd" }
ph: "1 Physical\nsignals, bits" { width: 260; height: 70; style.fill: "#e3f2fd" }
a -> p -> s -> t -> n -> d -> ph
```

**Fig. 1.** The 7-layer stack. On the sender, data moves down gaining a header per layer; on the receiver it moves back up losing them.

## Why it exists and how it is used

OSI was designed as a protocol suite but lost that race to TCP/IP; what survived and dominates is OSI as a **vocabulary and teaching/troubleshooting model**. Its real value: it gives interviewers and network engineers a shared coordinate system ("that is a layer-2 problem, not DNS"), it explains encapsulation cleanly (see [[How does encapsulation work in the OSI model]]), and it contrasts instructively with the TCP/IP model that real implementations follow (see [[What is the difference between the OSI model and the TCP IP model]]).

> [!warning] Real stacks do not have clean OSI layers
> The Internet suite maps to 4–5 layers, not 7: TCP/IP has no separate session or presentation layer — their jobs are absorbed by applications (TLS acts like presentation+session and lives between TCP and HTTP) and by libraries. Also some devices cross layers: an L3 switch routes while switching frames, and NAT rewrites both addresses and ports. Treating OSI as a physical truth rather than a reference model is the classic mistake.

Layer-by-layer details: [[What is the purpose of each OSI layer]], [[What PDU is associated with each OSI layer]], and [[What is the correct order of OSI layers from Layer 7 to Layer 1]] for the drill order.

> [!tip] Interview answer
> OSI is a 7-layer reference model from ISO/IEC 7498-1 / ITU-T X.200: Application, Presentation, Session down to Transport, Network, Data Link, Physical. Each layer has one responsibility and offers a service to the layer above via encapsulation. Today it survives as vocabulary and a troubleshooting grid rather than a running protocol suite — real networks run TCP/IP, which folds 5–7 into the application layer.
