<!--
reps: 0
priority: 0
-->
#Networking #SRS
# What is DHCP and how does it work

> [!abstract] Short answer
> DHCP (Dynamic Host Configuration Protocol, RFC 2131) automatically hands a joining host its network configuration: IP address, subnet mask, default gateway, DNS servers, lease duration. A new client broadcasts a DHCPDISCOVER, servers answer with DHCPOFFER, the client broadcasts DHCPREQUEST for the offer it accepts, and the chosen server confirms with DHCPACK — the DORA exchange, carried over UDP (server 67, client 68).

## DORA, step by step

1. **Discover (client → broadcast):** the client has no address yet, so everything is broadcast at L2 (`ff:ff:ff:ff:ff:ff`); the packet carries the client MAC and a transaction id.
2. **Offer (server → client):** each server on the link proposes an address + lease time + options. Multiple servers may offer; the client picks one.
3. **Request (client → broadcast):** the client requests the chosen offer (echoing the server id) — broadcast so *rejected* servers also learn they lost.
4. **ACK (server → client):** the winner confirms, and the client may ARP-probe the address before fully using it (duplicate detection). On renewal (typically at 50% of the lease), the client unicast-requests the same address from the original server.

```d2
direction: right
c: "Client (no IP)" { width: 200; height: 70; style.fill: "#e3f2fd" }
bc: "broadcast ff:ff:..." { width: 200; height: 70; style.fill: "#fff3e0" }
s: "DHCP server (UDP 67)" { width: 230; height: 80; style.fill: "#e8f5e9" }
d1: "1 DISCOVER" { width: 160; height: 50; style.fill: "#fff3e0" }
d2: "2 OFFER\naddr + lease + options" { width: 220; height: 70; style.fill: "#fff3e0" }
d3: "3 REQUEST" { width: 150; height: 50; style.fill: "#fff3e0" }
d4: "4 ACK -> client configured" { width: 210; height: 60; style.fill: "#e8f5e9" }
c -> d1 -> bc -> s
s -> d2 -> bc -> c
c -> d3 -> bc -> s
s -> d4 -> bc -> c
```

**Fig. 1.** The DORA exchange; broadcast at L2 is unavoidable because the client has no usable address yet.

## What the lease actually contains

Beyond the address: subnet mask, default gateway (router option), DNS server list (the reason a broken DHCP makes "everything resolve slowly" — [[What is DNS and how does DNS resolution work]]), domain name, NTP servers, MTU hints, and vendor-specific options. The **lease duration** defines re-renewal (T1 = 50%: unicast renewal; T2 = 87.5%: rebroadcast to any server) and reclaim: after expiry the server may hand the address to someone else.

> [!warning] DHCP is a UDP LAN protocol — it cannot set up itself across routers
> A DISCOVER broadcast does not cross a router, so a central DHCP server for many subnets needs **DHCP relay agents** on each router (they convert broadcast to unicast toward the server). People also conflate DHCP with DNS ("DHCP gave me a name") — DHCP hands out *configuration* (including which DNS servers to use); it does not resolve names. And static-reservation ≠ static config: reservations bind an address to a MAC, still managed by the server ([[How does ARP relate to the OSI layers]] is how that MAC binding gets used).

Wire view: [[What does a Layer 2 broadcast look like in a packet capture]]; where the client goes after DORA: [[What is the TCP IP protocol suite]].

> [!tip] Interview answer
> DHCP automates host configuration: address, mask, gateway, DNS, lease time — over UDP 67/68. The exchange is DORA: broadcast Discover, Offer, broadcast Request, Ack, with lease renewal at half the lease. Details I add: everything starts broadcast because the client has no IP; relays are needed across subnets; and a DHCP-provided DNS list is why a dead DHCP server breaks more than addressing.
