<!--
reps: 0
priority: 0
-->
#Networking/TCP #SRS
# What is the TCP IP protocol suite

> [!abstract] Short answer
> The TCP/IP protocol suite is the family of protocols the Internet is built on, organized in four layers: Link (Ethernet, Wi-Fi), Internet (IP, ICMP), Transport (TCP, UDP — and QUIC over UDP), Application (HTTP, DNS, DHCP, TLS, SMTP). Its two eponymous protocols — IP, which delivers datagrams best-effort across networks, and TCP, which adds reliable ordered streams on top — define its defining tradeoff: a simple, dumb network core with intelligence at the endpoints (the end-to-end principle).

## The layers and their load-bearing protocols

1. **Link** — move frames over one physical network: Ethernet (802.3), Wi-Fi (802.11), PPP; MAC addressing, ARP as the IPv4 glue.
2. **Internet** — move packets host-to-host across networks: IPv4/IPv6 addressing and forwarding, ICMP diagnostics (ping, traceroute), router behavior per RFC 1812.
3. **Transport** — move data process-to-process: TCP (RFC 9293: ordered, reliable, flow- and congestion-controlled byte streams), UDP (RFC 768: minimal datagrams), QUIC (RFC 9000: TLS-integrated multiplexed streams over UDP).
4. **Application** — semantic protocols: DNS (names), DHCP (configuration), HTTP/1.1-2-3 (the web), TLS (channel security), FTP, SMTP/IMAP, SSH.

```d2
direction: down
app: "Application\nHTTP, DNS, SMTP, DHCP" { width: 300; height: 80; style.fill: "#e8f5e9" }
tr: "Transport\nTCP reliable | UDP fast | QUIC" { width: 320; height: 90; style.fill: "#fff3e0" }
net: "Internet\nIP best-effort datagrams, ICMP" { width: 320; height: 90; style.fill: "#e3f2fd" }
ln: "Link\nEthernet, Wi-Fi, ARP" { width: 300; height: 80; style.fill: "#f3e5f5" }
app -> tr -> net -> ln
```

**Fig. 1.** The suite in one column; every arrow is an encapsulation ([[How does encapsulation work in the OSI model]]).

## The design decisions worth naming

- **Best-effort core.** IP promises almost nothing — routers drop, reorder, duplicate. Everything an app relies on is implemented at the edge: reliability in TCP, integrity in TLS, dedup in application logic ([[How do you prevent duplicate message or packet delivery]]).
- **Narrow waist.** Thousands of applications above, many link technologies below, one protocol in the middle (IP) — that is why the Internet scales across decades of hardware change.
- **Ports + sockets.** Transport multiplexes thousands of conversations per host onto one address.

> [!warning] "TCP/IP" is not "the OSI model", and TCP is not the only transport
> The suite predates OSI and maps to 4 layers, not 7 ([[How many layers does the TCP IP model have]]). And "Internet = TCP" is now half-true: media streaming, DNS, games and QUIC-based HTTP/3 increasingly ride UDP, because retransmitting a dropped video frame is worse than skipping it ([[What is the difference between TCP and UDP]]).

Model-level contrast: [[What is the difference between the OSI model and the TCP IP model]]; deep dives: [[What is TCP]], [[What is UDP]], [[What is DNS and how does DNS resolution work]].

> [!tip] Interview answer
> TCP/IP is the four-layer Internet suite: Link, Internet, Transport, Application. IP gives best-effort packet delivery, TCP adds reliable ordered byte streams with flow and congestion control, UDP keeps datagrams cheap, and QUIC rebuilds reliability over UDP for HTTP/3. The design point I stress: dumb network core, smart endpoints — that is the end-to-end principle, and it explains why the suite scaled.
