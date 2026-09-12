<!--
reps: 0
priority: 0
-->
#Networking #SRS
# What is VRRP

> [!abstract] Short answer
> VRRP (Virtual Router Redundancy Protocol) lets several physical routers share one virtual gateway IP and MAC address, so hosts keep a single default gateway while a standby router transparently takes over if the master fails. The protocol is defined for IPv4 and IPv6 in RFC 5798 (VRRP version 3; version 2 was IPv4-only).

## How failover works

A VRRP setup has one **virtual router** (configured VRID, virtual IPvX address), one **Master**, and one or more **Backups**:

1. Every participant owns a real interface address; the router whose real IP equals the virtual IP is the IP address owner and announces **priority 255**. Other routers are configured with a priority from 1–254.
2. The Master periodically multicasts VRRP advertisements (IPv4: multicast group `224.0.0.18`, IP protocol 112; IPv6: `ff02::12`). Backups run a timer — Master_Down_Interval is derived from the advertisement interval and skew time, so a higher-priority Backup expires sooner.
3. When advertisements stop arriving within Master_Down_Interval, the highest-priority Backup switches to Master, sends a gratuitous ARP (IPv4) or unsolicited Neighbor Advertisement (IPv6) claiming the virtual MAC, and starts forwarding.
4. Hosts never change configuration: their default gateway (virtual IP) and its virtual MAC (`00:00:5E:00:01:{VRID}` for IPv4) stay the same. A failed master's traffic is interrupted only for the time to detect and advertise.

```d2
direction: right
hosts: "Hosts\ngateway = virtual IP" { width: 240; height: 90; style.fill: "#e3f2fd" }
master: "Router A (Master)\npriority 200\nadvertisements every interval" { width: 300; height: 100; style.fill: "#e8f5e9" }
backup: "Router B (Backup)\npriority 150\nlistens, timer runs" { width: 280; height: 100; style.fill: "#fff3e0" }
hosts -> master: "traffic to default gateway"
master -> backup: "VRRP advertisement (multicast)"
backup -> hosts: "on A failure: claim virtual MAC, forward"
```

**Fig. 1.** Only the Master forwards traffic; Backups keep the election state and take the virtual address over when the advertisement stream stops.

> [!warning] Preemption and asymmetry
> With preemption enabled (the default in VRRPv3), a router coming back online with a higher priority takes mastership immediately — brief disruption again. With `no preempt`, it waits even though it is "better". Also VRRP does not by itself synchronize state beyond the gateway role: it protects the default-route hop, not firewall session tables or DHCP leases, which need their own mechanisms.

VRRP answers "what happens if the default gateway dies" in any LAN with [[What is the difference between private and public IP addresses]] addressing — hosts on private subnets point at the virtual IP. It is the layer-3 counterpart of keeping [[At which OSI layer does a router primarily operate]] highly available, and complements link-level redundancy like LACP. Related layer-4+ balancing is a different problem: [[What is the difference between L3 L4 and L7]].

> [!tip] Interview answer
> VRRP gives a group of routers a virtual IP/MAC that hosts use as default gateway. The Master multicasts advertisements; when Backups stop hearing them they expire a timer, the highest-priority one becomes Master and gratuitous ARP re-maps the virtual MAC. Hosts notice nothing. Mention RFC 5798 (VRRPv3, IPv4+IPv6), priority 0–255, and that preemption causes a second, deliberate failover.
