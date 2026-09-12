<!--
reps: 0
priority: 0
-->
#Networking #SRS
# What is NAT and how does it work

> [!abstract] Short answer
> NAT (Network Address Translation, RFC 3022) rewrites IP addresses — usually also ports — on packets crossing a boundary between address realms, letting many hosts with private RFC 1918 addresses share one or few public addresses. The router keeps a translation table of (private IP:port ↔ public IP:port) pairs, so reply packets are mapped back to the right internal host; that dominant variant is NAPT ("port address translation"), what everyone simply calls NAT.

## The outbound/inbound mechanics

1. Host `192.168.1.10:51234` sends to `93.184.216.34:443`.
2. The NAT gateway allocates a mapping: `192.168.1.10:51234 ↔ 203.0.113.5:40001`, rewrites source address and port, recomputes IP (and TCP/UDP) checksums, and forwards.
3. The reply comes to `203.0.113.5:40001`; the table reverses the rewrite and delivers to the host. The mapping lives as long as traffic flows (UDP timeouts, TCP teardown/FIN or idle expiry).
4. **Inbound** connections have no table entry — that is why servers behind NAT need explicit **port forwarding** (static mapping) or a relay/broker (STUN/TURN in WebRTC, UPnP/PMP in home gear).

```d2
direction: right
h: "Host 192.168.1.10:51234" { width: 240; height: 80; style.fill: "#e3f2fd" }
nat: "NAT gateway\n203.0.113.5\n51234 <-> 40001" { width: 260; height: 100; style.fill: "#fff3e0" }
srv: "Server 93.184.216.34:443\nsees 203.0.113.5:40001" { width: 280; height: 90; style.fill: "#e8f5e9" }
h -> nat -> srv
srv -> nat -> h: "reply maps back"
```

**Fig. 1.** The server never learns the private address; the translation table is the entire trick.

## Variants and consequences

- **SNAT / masquerade** (many-to-one, outbound) — the home/office default; **DNAT / port forwarding** (one-to-one or port-mapped, inbound); **full-cone vs symmetric** NAT differ in who may reuse the mapping — symmetric breaks naive P2P, hence STUN/TURN/ICE.
- **CGNAT** (RFC 6598, 100.64/10): ISPs NAT their customers too, so the "public" address you see may still be shared.
- **NAT as firewall-by-accident:** unsolicited inbound is dropped for lack of mapping — useful, but it is address scarcity engineering, not security design ([[What is the difference between private and public IP addresses]]).
- **NAT66/NPTv6** exists even though IPv6 was designed to restore end-to-end addressing ([[What is the difference between IPv4 and IPv6]]).

> [!warning] NAT breaks protocols that carry addresses in the payload
> FTP's active mode announces an IP:port inside the control channel — a pure packet-rewriting NAT cannot fix that, which is why passive mode won ([[What is FTP]]). Similar pain: SIP/SDP, some games, EIH protocols. Also, NAT halves the natural web symmetry: servers see the gateway's address, so [[How do you get the client IP address in a servlet]] needs X-Forwarded-For/PROXY protocol trust chains — and IP-based rate limiting punishes whole offices sharing one public IP. Saying "NAT improves security because addresses are hidden" is the interview lie: hiding is a side effect; stateful firewall rules do the security.

Related mechanics: [[What is a socket in networking]] (the 4-tuple NAT rewrites), [[What is the TCP three-way handshake]] (mapping tied to connection state).

> [!tip] Interview answer
> NAT lets many private hosts share public addresses: the edge router rewrites source IP and port, keeps a mapping table, and translates replies back — that is NAPT, or "masquerade". Inbound needs static port forwarding or helpers (STUN/TURN), because there is no mapping to reuse. I flag the side effects: address-carrying protocols like active FTP break, servers no longer see real client IPs, and "NAT is a firewall" is a myth — mapping is scarcity engineering, not security.
