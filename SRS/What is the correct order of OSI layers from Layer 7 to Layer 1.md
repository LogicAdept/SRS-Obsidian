<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# What is the correct order of OSI layers from Layer 7 to Layer 1

> [!abstract] Short answer
> Layer 7 → 1: Application, Presentation, Session, Transport, Network, Data Link, Physical. The standard mnemonics: "All People Seem To Need Data Processing" (top-down) or "Please Do Not Throw Sausage Pizza Away" (bottom-up).

## The order with one anchor per layer

| # | Layer | Anchor example | Unit |
|---|---|---|---|
| 7 | Application | HTTP request/response | data/message |
| 6 | Presentation | UTF-8, JPEG, TLS record encryption | data |
| 5 | Session | dialog setup, TLS session resumption | data |
| 4 | Transport | TCP segment, UDP datagram | segment/datagram |
| 3 | Network | IP packet, routing decision | packet |
| 2 | Data Link | Ethernet frame, MAC, switch forwarding | frame |
| 1 | Physical | bits, cables, radio, voltages | bit/symbol |

```d2
direction: right
l7: "7 Application" { width: 150; height: 60; style.fill: "#e8f5e9" }
l6: "6 Presentation" { width: 150; height: 60; style.fill: "#e8f5e9" }
l5: "5 Session" { width: 130; height: 60; style.fill: "#e8f5e9" }
l4: "4 Transport" { width: 140; height: 60; style.fill: "#fff3e0" }
l3: "3 Network" { width: 130; height: 60; style.fill: "#fff3e0" }
l2: "2 Data Link" { width: 140; height: 60; style.fill: "#e3f2fd" }
l1: "1 Physical" { width: 130; height: 60; style.fill: "#e3f2fd" }
l7 -> l6 -> l5 -> l4 -> l3 -> l2 -> l1
```

**Fig. 1.** Descending order 7 → 1; sending data follows this direction, receiving reverses it (de-encapsulation).

> [!warning] Do not shuffle Presentation and Session
> Interviewers probe the middle of the stack. Presentation is about *representation* of data (encoding, compression, encryption of the message itself); Session is about *managing dialogs* (who may talk, checkpointing, resuming). A fast check: TLS record encryption is usually presented as a layer-6 style duty, while a TLS session identifier or resumption ticket is a layer-5 style idea.

More depth per layer: [[What is the purpose of each OSI layer]], individual-layer cards such as [[What is the importance of the OSI Physical layer]] and [[What is the function of the OSI Presentation layer]], and the machinery of moving between layers in [[How does encapsulation work in the OSI model]].

> [!tip] Interview answer
> Top-down: Application, Presentation, Session, Transport, Network, Data Link, Physical — "All People Seem To Need Data Processing". I keep one anchor per layer to stay accurate: HTTP at 7, encodings and TLS encryption at 6, dialogs at 5, TCP/UDP at 4, IP at 3, MAC and frames at 2, bits on the wire at 1.
