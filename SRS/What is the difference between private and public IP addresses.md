<!--
reps: 0
priority: 0
-->
#Networking #SRS
# What is the difference between private and public IP addresses

> [!abstract] Short answer
> Public IP addresses are globally unique and routable on the Internet — assigned by registries and ISPs. Private addresses (RFC 1918) are reserved blocks — `10/8`, `172.16/12`, `192.168/16` — that are free to use inside any organization, are not routed on the public Internet, and are reused by millions of networks simultaneously; connectivity between private and public space happens through NAT (or proxies).

## The reserved blocks and their logic

RFC 1918 sets aside, in IPv4:

- `10.0.0.0 – 10.255.255.255` (10/8) — 16.7M addresses, the classic enterprise block;
- `172.16.0.0 – 172.31.255.255` (172.16/12) — 1M, popular in defaults (Docker's 172.17.0.0/16 lives in this range — [[How do containers find each other by name on a Docker network]]);
- `192.168.0.0 – 192.168.255.255` (192.168/16) — 65k, every home router.

Routers on the public Internet drop packets carrying these sources/destinations; the same `192.168.1.10` exists in countless offices at once — uniqueness is only *per site*. The boundary between private and public is where NAT rewrites addresses ([[What is NAT and how does it work]]).

```d2
direction: right
lan: "Office LAN 10.0.0.0/8\nhosts, printers, laptops\nfree reuse of 1918 space" { width: 300; height: 110; style.fill: "#e3f2fd" }
gw: "Border router / firewall\nNAT: private <-> public" { width: 280; height: 100; style.fill: "#fff3e0" }
net: "Internet\npublic IP only\nglobally unique" { width: 240; height: 100; style.fill: "#e8f5e9" }
lan -> gw -> net
```

**Fig. 1.** Private space gives every site the same cheap addresses; the NAT edge is the only place a globally unique identity is needed.

## Related special ranges worth one sentence each

- **Link-local** `169.254/16` (APIPA): self-assigned when DHCP fails — not routable even within a site by intent.
- **Loopback** `127/8`: "this host" only; `localhost` never leaves the machine.
- **CGNAT** `100.64/10`: carrier-grade NAT space between ISP and customer.
- **IPv6:** global unicast addresses are the "public" side; `fc00::/7` (ULA) is the private analogue; `fe80::/10` link-local is mandatory per interface.

> [!warning] "Private IP means more secure" conflates addressing with access control
> A private address is unROUTABLE from the Internet, but security comes from what the firewall at the border accepts (port forwarding punches holes through exactly this wall), plus host-level controls. Also classic traps: two merged companies both using `10.0.0.0/8` cannot talk until re-addressed or NAT-ed (address reuse has a price); and "my VM has 192.168.x.x, so it has no Internet" is false — outbound works fine via NAT; it is *inbound* unsolicited traffic that needs explicit mapping. Local echo of this: a socket bound to 127.0.0.1 is reachable neither from LAN nor Internet ([[What is a socket in networking]]).

Bigger picture: [[What is the difference between IPv4 and IPv6]] (why the scarcity exists), [[What is the difference between a MAC address and an IP address]] (logical vs physical identity).

> [!tip] Interview answer
> Public addresses are globally unique and Internet-routable; RFC 1918 reserves 10/8, 172.16/12 and 192.168/16 for free internal reuse — not routed publicly, unique only per site. The edge between them is where NAT lives. I add: link-local 169.254 and loopback 127/8 are other special blocks, merged 10/8 networks are the classic operations pain, and private ≠ secure — firewalls and NAT rules provide security, the address class itself does not.
