<!--
reps: 0
priority: 0
-->
#Networking/OSI #SRS
# How do the TCP IP model layers map to the OSI model

> [!abstract] Short answer
> The TCP/IP model (RFC 1122 defines its lower layers) has four layers: Link, Internet, Transport and Application. Link ≈ OSI 1–2, Internet ≈ OSI 3, Transport ≈ OSI 4, Application ≈ OSI 5–7: the three upper OSI layers (Session, Presentation, Application) collapse into one TCP/IP Application layer, because real protocols absorb those duties.

## The mapping table

| TCP/IP layer (RFC 1122) | OSI layers | What lives there |
|---|---|---|
| Link (network access) | 1 Physical, 2 Data Link | Ethernet/Wi-Fi frames, MAC, NICs, drivers |
| Internet | 3 Network | IP (v4/v6), ICMP, routing |
| Transport | 4 Transport | TCP, UDP (+ QUIC operating over UDP) |
| Application | 5 Session, 6 Presentation, 7 Application | HTTP, TLS, DNS, DHCP, FTP, SMTP |

```d2
direction: down
l7: "OSI 7-5\nApplication, Presentation, Session" { width: 320; height: 80; style.fill: "#e8f5e9" }
app: "TCP/IP Application\nHTTP, TLS, DNS..." { width: 320; height: 80; style.fill: "#fff3e0" }
osi4: "OSI 4 Transport" { width: 240; height: 60; style.fill: "#fff3e0" }
trans: "TCP/IP Transport\nTCP, UDP" { width: 320; height: 80; style.fill: "#fff3e0" }
osi3: "OSI 3 Network" { width: 240; height: 60; style.fill: "#e3f2fd" }
inet: "TCP/IP Internet\nIP, ICMP" { width: 320; height: 80; style.fill: "#e3f2fd" }
osi21: "OSI 2-1\nData Link, Physical" { width: 280; height: 70; style.fill: "#f3e5f5" }
link: "TCP/IP Link\nEthernet, Wi-Fi, drivers" { width: 320; height: 80; style.fill: "#f3e5f5" }
l7 -> app
osi4 -> trans
osi3 -> inet
osi21 -> link
```

**Fig. 1.** One-to-one in the middle, collapsed at the top: 7 OSI layers become 4 TCP/IP layers.

## Why the top collapses

The Internet suite was built around two insights: the network does best-effort packet delivery (IP), and the edges run applications. Anything between — dialog management, representation, encryption — is the application's business. In practice the split is visible: HTTP is application semantics, TLS is a security shim doing presentation/session-style work, cookies implement dialog state — all inside one "Application" tier. [[Why do many dumps place HTTPS encryption at the Presentation layer]] works through the most popular example.

> [!warning] The TCP/IP model has variant counts — know both
> Textbooks differ: RFC 1122 literally names Link, Internet, Transport, Application (4 layers); other books insert Physical as a separate 5th layer. What is *not* negotiable: TCP/IP does not have a standalone Session or Presentation layer. Answering "TCP/IP has 7 layers like OSI" is the failure mode; "4 by RFC 1122, sometimes taught as 5 with Physical split" shows the literature awareness ([[How many layers does the TCP IP model have]]).

Contrast: [[What is the difference between the OSI model and the TCP IP model]]; drill anchor: [[What is the correct order of OSI layers from Layer 7 to Layer 1]] for the OSI side, [[What is the TCP IP protocol suite]] for the real protocols at each TCP/IP layer.

> [!tip] Interview answer
> Mapping: Link ≈ OSI 1–2, Internet ≈ 3, Transport ≈ 4, Application ≈ 5–7 — RFC 1122's four layers with the top three OSI layers collapsed. The reason: TCP/IP pushes dialogs, encodings and encryption into the application (TLS, cookies, serialization), so no dedicated session or presentation protocols exist. If asked about variants, I mention the 5-layer presentation that splits Physical out.
