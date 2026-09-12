<!--
reps: 0
priority: 0
-->
#Networking #SRS
# What is the difference between IPv4 and IPv6

> [!abstract] Short answer
> IPv4 (RFC 791) uses 32-bit addresses (~4.3 billion) written dotted-decimal; IPv6 (RFC 8200) uses 128-bit addresses written as eight hex groups, was created because IPv4 space ran out, and comes with a fixed 40-byte header, no header checksum, no in-flight fragmentation (path MTU discovery instead), extension headers, built-in SLAAC autoconfiguration, and mandatory support for IPsec-style security models.

## The comparison that matters

| Aspect | IPv4 (RFC 791) | IPv6 (RFC 8200) |
|---|---|---|
| Address size | 32 bit — 4.3×10^9 | 128 bit — effectively unlimited |
| Notation | 192.168.1.10 | 2001:0db8:0000:0000:0000:ff00:0042:8329 (compressed: 2001:db8::ff00:42:8329) |
| Header | 20–60 B, variable, checksum | fixed 40 B + extension headers, **no checksum** |
| Fragmentation | routers may fragment (DF flag off) | senders only (PMTUD); routers drop "too big" with ICMPv6 |
| Broadcast | yes (e.g. ARP requests) | none — multicast + anycast instead |
| Autoconfig | DHCP | SLAAC (RA-based) or DHCPv6 |
| NAT | ubiquitous necessity | designed to restore end-to-end (but NAT66 exists anyway) |
| Notation traps | leading zeros matter | leading zeros may be dropped; `::` may appear once |

```d2
direction: down
v4: "IPv4 header\n20-60B, checksum,\nfrag fields, options" { width: 260; height: 100; style.fill: "#e3f2fd" }
v6: "IPv6 header\nfixed 40B, no checksum,\nNext Header chain" { width: 260; height: 100; style.fill: "#e8f5e9" }
v4 -> v6: "same job, leaner plumbing"
```

**Fig. 1.** The header slimming: IPv6 moves rarely-used machinery (fragmentation, options) into extension headers so routers process a fixed fast path.

## What IPv6 actually changed operationally

- **Address abundance:** every device can have globally routable addresses; subnets are /64 by habit; the ISP gets a prefix and delegates.
- **Neighbor Discovery (ICMPv6)** replaces ARP ([[What is ARP and how does it work]]), adds router/prefix discovery and duplicate address detection.
- **Dual stack** is the deployment reality: IPv4 and IPv6 run side by side, with transition helpers (tunnels, NAT64/DNS64 for IPv6-only clients reaching IPv4-only servers).
- **No broadcast** — NDP and mDNS-equivalents use multicast groups; storm behavior changes ([[What does a Layer 2 broadcast look like in a packet capture]]).

> [!warning] IPv6 is not "IPv4 with longer addresses"
> The header redesign matters: removing the checksum shifts integrity duty to link layers and transports (TCP/UDP checksums now cover pseudo-headers); removing router fragmentation makes PMTUD mandatory — firewalls that block all ICMPv6 break IPv6 fundamentally, because "packet too big" *is* part of the protocol. And zone IDs (fe80::1%eth0) exist only on-link; link-local addresses are not routable. Saying "IPv6 has no NAT, so NAT is gone" ignores that operators still deploy NAT66 for address management.

Related: [[What is the difference between private and public IP addresses]] for the scarcity mechanics IPv4 lives with, [[What is NAT and how does it work]] for the patch IPv6 reduces the need for, [[What is a packet at the Network layer]] for header mechanics.

> [!tip] Interview answer
> IPv4: 32-bit addresses, variable header with checksum, routers may fragment, broadcast exists. IPv6: 128-bit, fixed 40-byte header without checksum, extension headers, no router fragmentation (PMTUD), multicast instead of broadcast, SLAAC autoconfig, ICMPv6/NDP replacing ARP. Deployment is dual stack; the detail I always add: blocking ICMPv6 breaks IPv6 because PMTUD depends on it.
