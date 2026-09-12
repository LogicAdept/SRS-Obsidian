<!--
reps: 0
priority: 0
-->
#Networking/OSI #Networking/TCP #SRS
# What is the difference between the OSI model and the TCP IP model

> [!abstract] Short answer
> OSI is a 7-layer *reference model* (ISO/IEC 7498-1 / ITU-T X.200) — vocabulary and teaching structure; TCP/IP is the actual *protocol suite* the Internet runs (Link, Internet, Transport, Application, per RFC 1122). OSI separates Presentation and Session; TCP/IP folds them into the application. OSI was descriptive-first and lost the protocol war; TCP/IP was implemented first and got the model named after it afterwards.

## Side by side

| Aspect | OSI model | TCP/IP model |
|---|---|---|
| Origin | ISO/IEC + ITU-T standard (1984) | DARPA/Internet engineering, codified in RFC 1122 |
| Layers | 7: App, Pres, Session, Transport, Network, Data Link, Physical | 4 (RFC 1122): Application, Transport, Internet, Link |
| Nature | reference model; the OSI protocol suite itself lost to TCP/IP | both model and running suite (IP, TCP, UDP...) |
| Session/Presentation | dedicated layers | absorbed by apps + TLS |
| Delivery philosophy | connection-oriented heritage (X.25 world) | best-effort datagram core (IP), reliability at the edges (TCP) |
| Practical use | vocabulary, troubleshooting grid, exams | how stacks are actually built |

```d2
direction: right
osi: "OSI: 7 layers\nApp | Pres | Session | Transport |\nNetwork | Data Link | Physical" { width: 340; height: 110; style.fill: "#e3f2fd" }
tip: "TCP/IP: 4 layers\nApplication | Transport | Internet | Link" { width: 340; height: 110; style.fill: "#e8f5e9" }
osi -> tip: "top 3 collapse\nbottom 2 collapse"
```

**Fig. 1.** The 7→4 collapse: middle layers map one-to-one (Transport↔Transport, Network↔Internet).

## How to use each in an answer

- Use **OSI** names when locating problems and devices: "L2 switch, L3 router, L7 proxy", "bottom-up check".
- Use **TCP/IP** names when describing real protocols and stacks: "DNS is application layer over UDP/TCP; QUIC merges transport security over UDP".
- Never mix the vocabularies in one sentence ("TCP is the OSI network layer protocol" is doubly wrong: TCP is transport, and the Internet layer is IP's).

> [!warning] "OSI is obsolete" is as wrong as "OSI is how networks work"
> Both halves of the statement matter: OSI protocols (X.400, X.25-lineage) indeed lost, but the *model* is alive — it is the shared language of every network course and certification. Conversely, claiming that a TCP/IP stack "implements the OSI model" misstates history: TCP/IP predates OSI standardization and never promised layer-by-layer conformance ([[What is the OSI model]], [[How many layers does the TCP IP model have]]).

Practical anchors: [[What is the TCP IP protocol suite]] for the suite itself, [[What PDU is associated with each OSI layer]] for terminology, [[How do the TCP IP model layers map to the OSI model]] for the mapping mechanics.

> [!tip] Interview answer
> OSI is a 7-layer reference model from ISO/ITU — a vocabulary; TCP/IP is the deployed 4-layer suite (Link, Internet, Transport, Application). The mapping collapses OSI 5–7 into Application and 1–2 into Link. I use OSI names to locate devices and problems, TCP/IP names to describe real protocols — and I avoid both extremes: OSI is not obsolete vocabulary, and it is also not how stacks are implemented.
